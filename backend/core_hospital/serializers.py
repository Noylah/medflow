from rest_framework import serializers
from .models import Patient, Encounter, Triage, VitalSign, ClinicalNote, HospitalUser

# --- SERIALIZER USER ---

class HospitalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = HospitalUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']

    def create(self, validated_data): # Funzione per creare un nuovo utente senza lasciare la password nei dati
        password = validated_data.pop('password')
        user = HospitalUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data): # Funzione per aggiornare un nuovo utente senza lasciare la password nei dati
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

# --- SERIALIZER PATIENT ---

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

# --- SERIALIZER ENCOUNTER ---

# Serializer per metodi POST e PUT (Il paziente viene espresso unicamente con l'id)
class EncounterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = '__all__'

# Serializer per metodo GET (Il paziente viene espresso con tutte le informazioni)
class EncounterReadSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True) 
    primary_doctor = HospitalUserSerializer(read_only=True)

    class Meta:
        model = Encounter
        fields = '__all__'

# --- SERIALIZER TRIAGE ---
class TriageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = '__all__'

class TriageReadSerializer(serializers.ModelSerializer):
    encounter = EncounterReadSerializer(read_only=True) 
    author = HospitalUserSerializer(read_only=True)

    class Meta:
        model = Triage
        fields = '__all__'

# --- SERIALIZER VITALSIGN ---
class VitalSignWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSign
        fields = '__all__'

class VitalSignReadSerializer(serializers.ModelSerializer):
    encounter = EncounterReadSerializer(read_only=True) 
    author = HospitalUserSerializer(read_only=True)

    class Meta:
        model = VitalSign
        fields = '__all__'

# --- SERIALIZER CLINICALNOTE ---
class ClinicalNoteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalNote
        fields = '__all__'

class ClinicalNoteReadSerializer(serializers.ModelSerializer):
    encounter = EncounterReadSerializer(read_only=True) 
    author = HospitalUserSerializer(read_only=True)

    class Meta:
        model = ClinicalNote
        fields = '__all__'

