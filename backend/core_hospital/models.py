from django.db import models
from django.contrib.auth.models import AbstractUser

class HospitalUser(AbstractUser):
    ROLE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('RECEPTIONIST', 'Receptionist'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_role_display()} {self.first_name} {self.last_name}"

class Patient(models.Model): 
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    fiscal_code = models.CharField(max_length=16, unique=True)
    birth_date = models.DateField()
    blood_type = models.CharField(max_length=3, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.fiscal_code})"

class Encounter(models.Model):
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'), 
        ('UNDER_VISIT', 'Under Visit'),
        ('DISCHARGED', 'Discharged'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    admission_time = models.DateTimeField(auto_now_add=True)
    discharge_time = models.DateTimeField(blank=True, null=True)
    primary_doctor = models.ForeignKey(HospitalUser, on_delete=models.SET_NULL, null=True, related_name="encounters")

    def __str__(self):
        return f"Encounter {self.id} - {self.patient.fiscal_code}"
    
class Triage(models.Model):
    COLOR_CHOICES = [
        ('RED', 'Red'),
        ('YELLOW', 'Yellow'),
        ('GREEN', 'Green'),
        ('WHITE', 'White'),
    ]

    encounter = models.OneToOneField(Encounter, on_delete=models.CASCADE, related_name="triage") # Per ogni encounter c'è uno e un solo triage e viceversa
    color_code = models.CharField(max_length=10, choices=COLOR_CHOICES)
    chief_complaint = models.TextField()
    author = models.ForeignKey(HospitalUser, on_delete=models.SET_NULL, null=True, related_name="triages")

    def __str__(self):
        return f"Triage  for Encounter {self.encounter.id} - {self.get_color_code_display()} Code"

class VitalSign(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name="vital_signs")
    recorded_at = models.DateTimeField(auto_now_add=True)
    systolic_pressure = models.IntegerField()
    diastolic_pressure = models.IntegerField()
    heart_rate = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    oxygen_saturation = models.IntegerField()
    author = models.ForeignKey(HospitalUser, on_delete=models.SET_NULL, null=True, related_name="vital_signs")

    def __str__(self):
        return f'Vitals for Encounter {self.encounter.id} at {self.recorded_at.strftime("%H:%M")}'

class ClinicalNote(models.Model):
    NOTE_TYPE_CHOICES = [
        ('ANAMNESIS', 'Anamnesis'),
        ('EXAMINATION', 'Objective Examination'),
        ('PRESCRIPTION', 'Prescription'),
        ('NURSING', 'Nursing Note'),
    ]

    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name="notes")
    author = models.ForeignKey(HospitalUser, on_delete=models.SET_NULL, null=True, related_name="clinical_notes")
    note_type = models.CharField(max_length=20, choices=NOTE_TYPE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.note_type} by {self.author.last_name} for Encounter {self.encounter.id}"