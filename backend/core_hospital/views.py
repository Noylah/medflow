from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, EncounterWriteSerializer, EncounterReadSerializer, TriageReadSerializer, TriageWriteSerializer, VitalSignReadSerializer, VitalSignWriteSerializer, ClinicalNoteReadSerializer, ClinicalNoteWriteSerializer, HospitalUserSerializer
from .models import Patient, Encounter, Triage, VitalSign, ClinicalNote, HospitalUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import OuterRef, Subquery, Q
from rest_framework.authtoken.models import Token

# --- VIEW CRUD PATIENT ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def patient_list(request):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        patients = Patient.objects.all().order_by('last_name')
        search_query = request.query_params.get('search', None)
        last_encounter_status = request.query_params.get('status', None)
        last_triage_color = request.query_params.get('color', None)
        
        if search_query:
            patients = patients.filter(
                Q(last_name__icontains=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(fiscal_code__icontains=search_query)
            ).order_by('last_name')
            
        if last_encounter_status:
            status_upper = last_encounter_status.upper()
            if status_upper in ["WAITING", "UNDER_VISIT", "DISCHARGED"]:
                latest_encounter = Encounter.objects.filter(
                    patient=OuterRef("pk")
                ).order_by('-admission_time').values('status')[:1]
                
                patients = patients.annotate(
                    latest_status=Subquery(latest_encounter)
                ).filter(latest_status=status_upper)

        if last_triage_color:
            color_upper = last_triage_color.upper()
            if color_upper in ["RED", "YELLOW", "GREEN", "WHITE"]:
                latest_color_subquery = Encounter.objects.filter(
                    patient=OuterRef('pk')
                ).order_by('-admission_time').values('triage__color_code')[:1]
                
                patients = patients.annotate(
                    latest_color=Subquery(latest_color_subquery)
                ).filter(latest_color=color_upper)   
                
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    elif request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def patient_detail(request, id):
    try:
        patient_obj = Patient.objects.get(pk=id)
    except Patient.DoesNotExist:
        return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PatientSerializer(patient_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = PatientSerializer(patient_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        patient_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)
        
# --- VIEW CRUD ENCOUNTER ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def encounter_list(request):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        search_query = request.query_params.get('search', None)
        status_query = request.query_params.get('status', None)
        encounters = Encounter.objects.all().select_related('patient', 'primary_doctor').order_by('patient__last_name', 'primary_doctor__last_name', '-admission_time')
        if search_query:
            encounters = encounters.filter(
                Q(patient__last_name__icontains=search_query) | Q(patient__first_name__icontains=search_query) | Q(patient__fiscal_code__icontains=search_query) | Q(primary_doctor__first_name__icontains=search_query) | Q(primary_doctor__last_name__icontains=search_query) 
            )
        if status_query:
            status_query_upper = status_query.upper()
            if status_query_upper in ["WAITING", "UNDER_VISIT", "DISCHARGED"]:
                encounters = encounters.filter(status=status_query_upper)
        serializer = EncounterReadSerializer(encounters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EncounterWriteSerializer(data=request.data)
        if serializer.is_valid():
            encounter = serializer.save()
            return Response(EncounterReadSerializer(encounter).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def encounter_detail(request, id):
    try:
        encounter_obj = Encounter.objects.select_related('patient', 'primary_doctor').get(pk=id)
    except Encounter.DoesNotExist:
        return Response({"detail": "Encounter not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EncounterReadSerializer(encounter_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = EncounterWriteSerializer(encounter_obj, data=request.data, partial=True)
        if serializer.is_valid():
            encounter = serializer.save()
            return Response(EncounterReadSerializer(encounter).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        encounter_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- VIEW CRUD TRIAGE ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def triage_list(request):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        search_query = request.query_params.get('search', None)
        color_query = request.query_params.get('color', None)
        triages = Triage.objects.all().select_related('encounter__patient', 'author').order_by('encounter__patient__last_name', 'author__last_name', '-encounter__admission_time')
        if search_query:
            triages = triages.filter(
                Q(encounter__patient__last_name__icontains=search_query) | Q(encounter__patient__first_name__icontains=search_query) | Q(encounter__patient__fiscal_code__icontains=search_query) | Q(author__first_name__icontains=search_query) | Q(author__last_name__icontains=search_query)
            )
        if color_query:
            color_query_upper = color_query.upper()
            if color_query_upper in ["GREEN", "YELLOW", "RED", "WHITE"]:
                triages = triages.filter(color_code=color_query_upper)
        serializer = TriageReadSerializer(triages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TriageWriteSerializer(data=request.data)
        if serializer.is_valid():
            triage = serializer.save(author=request.user)
            return Response(TriageReadSerializer(triage).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def triage_detail(request, id):
    try:
        triage_obj = Triage.objects.select_related('encounter__patient', 'author').get(pk=id)
    except Triage.DoesNotExist:
        return Response({"detail": "Triage not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TriageReadSerializer(triage_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TriageWriteSerializer(triage_obj, data=request.data, partial=True)
        if serializer.is_valid():
            triage = serializer.save()
            return Response(TriageReadSerializer(triage).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        triage_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- VIEW CRUD VITALSIGN ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def vitalsign_list(request):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        search_query = request.query_params.get('search', None)
        if search_query:
            vitalsigns = VitalSign.objects.filter(
                Q(encounter__patient__last_name__icontains=search_query) | Q(encounter__patient__first_name__icontains=search_query) | Q(encounter__patient__fiscal_code__icontains=search_query) | Q(author__first_name__icontains=search_query) | Q(author__last_name__icontains=search_query)
            ).select_related('encounter__patient', 'author').order_by('encounter__patient__last_name', 'author__last_name', '-recorded_at')
        else:
            vitalsigns = VitalSign.objects.all().select_related('encounter__patient', 'author').order_by('encounter__patient__last_name', 'author__last_name', '-recorded_at')
        serializer = VitalSignReadSerializer(vitalsigns, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = VitalSignWriteSerializer(data=request.data)
        if serializer.is_valid():
            vitalsign = serializer.save(author=request.user)
            return Response(VitalSignReadSerializer(vitalsign).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def vitalsign_detail(request, id):
    try:
        vitalsign_obj = VitalSign.objects.select_related('encounter__patient', 'author').get(pk=id)
    except VitalSign.DoesNotExist:
        return Response({"detail": "Vital Sign not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = VitalSignReadSerializer(vitalsign_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = VitalSignWriteSerializer(vitalsign_obj, data=request.data, partial=True)
        if serializer.is_valid():
            vitalsign = serializer.save()
            return Response(VitalSignReadSerializer(vitalsign).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        vitalsign_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- VIEW CRUD CLINICALNOTE ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def clinicalnote_list(request):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        search_query = request.query_params.get('search', None)
        if search_query:
            clinicalnotes = ClinicalNote.objects.filter(
                Q(encounter__patient__last_name__icontains=search_query) | Q(encounter__patient__first_name__icontains=search_query) | Q(encounter__patient__fiscal_code__icontains=search_query) | Q(author__first_name__icontains=search_query) | Q(author__last_name__icontains=search_query)
            ).select_related('encounter__patient', 'author').order_by('encounter__patient__last_name', '-created_at')
        else:
            clinicalnotes = ClinicalNote.objects.all().select_related('encounter__patient', 'author').order_by('encounter__patient__last_name', '-created_at')
        serializer = ClinicalNoteReadSerializer(clinicalnotes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClinicalNoteWriteSerializer(data=request.data)
        if serializer.is_valid():
            clinicalnote = serializer.save(author=request.user)
            return Response(ClinicalNoteReadSerializer(clinicalnote).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def clinicalnote_detail(request, id):
    try:
        clinicalnote_obj = ClinicalNote.objects.select_related('encounter__patient', 'author').get(pk=id)
    except ClinicalNote.DoesNotExist:
        return Response({"detail": "Clinical Note not found."}, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClinicalNoteReadSerializer(clinicalnote_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClinicalNoteWriteSerializer(clinicalnote_obj, data=request.data, partial=True)
        if serializer.is_valid():
            clinicalnote = serializer.save()
            return Response(ClinicalNoteReadSerializer(clinicalnote).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if not request.user.is_superuser:
            if request.user.role not in ["NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        clinicalnote_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- VIEW CRUD HOSPITALUSER ---

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_list(request):
    if not request.user.is_superuser:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    if request.method == "GET":
        users = HospitalUser.objects.all().order_by('last_name')
        search_query = request.query_params.get('search', None)
        role_query = request.query_params.get('role', None)
        if role_query:
            role_query = role_query.upper()
            if role_query not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                role_query = None
            users = users.filter(role=role_query)
        if search_query:
            from django.db.models import Q
            users = users.filter(
                Q(last_name__icontains=search_query) | Q(first_name__icontains=search_query) | Q(username__icontains=search_query) | Q(email__icontains=search_query)
            ).order_by('last_name', 'first_name', 'username')
        serializer = HospitalUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = HospitalUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    if not request.user.is_superuser:
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
    try:
        user_obj = HospitalUser.objects.get(pk=id)
    except HospitalUser.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = HospitalUserSerializer(user_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = HospitalUserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        if user_obj == request.user:
            return Response({"detail": "You cannot delete your own account."}, status=status.HTTP_400_BAD_REQUEST)
            
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- AUTHENTICATION VIEWS ---

@api_view(["POST"])
@permission_classes([])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    if user is not None:
        login(request, user)
        return Response({
            "detail": "Login successful.",
            "token": token.key,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_superuser": user.is_superuser
        }, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not old_password or not new_password or not confirm_password:
        return Response({"detail": "Old Password, New Password and Confirm Password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(old_password):
        return Response({"detail": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
    
    if new_password != confirm_password:
        return Response({"detail": "New password does not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    if old_password == new_password:
        return Response({"detail": "The new password must be different from the old one."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        validate_password(new_password)
    except ValidationError as e:
        return Response({"new_password": e.messages}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()

    from django.contrib.auth import update_session_auth_hash
    update_session_auth_hash(request, user)

    return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

# --- DISCHARGE PATIENT ---

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def discharge_patient(request, encounter_id):
    if request.method == "POST":
        if not request.user.is_superuser:
            if request.user.role not in ["DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        try:
            encounter_obj = Encounter.objects.get(pk=encounter_id)
        except Encounter.DoesNotExist:
            return Response({"detail": "Encounter not found."}, status=status.HTTP_404_NOT_FOUND)
        if encounter_obj.status == "DISCHARGED":
            return Response({"detail": "Encounter arleady discharged."})
        encounter_obj.status = "DISCHARGED"
        encounter_obj.discharge_time = timezone.now()
        encounter_obj.save()
        serializer = EncounterReadSerializer(encounter_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- PATIENT TIMELINE ---

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_timeline(request, patient_id):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        try:
            patient_obj = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        encounters = Encounter.objects.filter(patient=patient_obj).prefetch_related(
            'triage',      
            'vital_signs',   
            'notes'
        ).order_by('-admission_time')

        timeline_data = []

        for enc in encounters:
            vitals = enc.vital_signs.all().order_by("-recorded_at")
            notes = enc.notes.all().order_by("-created_at")

            encounter_data = {
            "encounter_id": enc.id,
            "status": enc.status,
            "admission_time": enc.admission_time,
            "discharge_time": enc.discharge_time,
            "primary_doctor": f"{enc.primary_doctor.first_name} {enc.primary_doctor.last_name}" if enc.primary_doctor else None,
            "triage": TriageReadSerializer(enc.triage).data if hasattr(enc, 'triage') and enc.triage else None,
            "vital_signs": VitalSignReadSerializer(vitals, many=True).data,
            "clinical_notes": ClinicalNoteReadSerializer(notes, many=True).data
            }
            timeline_data.append(encounter_data)
        
        return Response({"patient": PatientSerializer(patient_obj).data, "history": timeline_data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

# --- PATIENT LAST ENCOUNTER ---
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patient_latest_encounter(request, patient_id):
    if request.method == "GET":
        if not request.user.is_superuser:
            if request.user.role not in ["RECEPTIONIST", "NURSE", "DOCTOR"]:
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        try:
            patient_obj = Patient.objects.get(pk=patient_id)
        except Patient.DoesNotExist:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

        latest_encounter = Encounter.objects.filter(
            patient=patient_obj
        ).order_by('-admission_time').first()
        
        if not latest_encounter:
            return Response({"detail": "No encounters found for this patient."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EncounterReadSerializer(latest_encounter)
        
        return Response({"latest_encounter": serializer.data}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)