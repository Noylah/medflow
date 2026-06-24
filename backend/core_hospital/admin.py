from django.contrib import admin
from .models import Patient, Encounter, Triage, VitalSign, ClinicalNote, HospitalUser

class HospitalUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'fiscal_code')

class EncounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient_first_name', 'get_patient_last_name', 'status')

    def get_patient_first_name(self, obj):
        return obj.patient.first_name
    get_patient_first_name.short_description = 'Patient First Name'

    def get_patient_last_name(self, obj):
        return obj.patient.last_name
    get_patient_last_name.short_description = 'Patient Last Name'

class TriageAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient_first_name', 'get_patient_last_name', 'get_color')

    def get_patient_first_name(self, obj):
        return obj.encounter.patient.first_name
    get_patient_first_name.short_description = 'Patient First Name'

    def get_patient_last_name(self, obj):
        return obj.encounter.patient.last_name
    get_patient_last_name.short_description = 'Patient Last Name'

    def get_color(self, obj):
        return obj.get_color_code_display()
    get_color.short_description = 'Color Code'

class VitalSignAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_patient_first_name', 'get_patient_last_name', 'get_formatted_time')

    def get_patient_first_name(self, obj):
        return obj.encounter.patient.first_name
    get_patient_first_name.short_description = 'Patient First Name'

    def get_patient_last_name(self, obj):
        return obj.encounter.patient.last_name
    get_patient_last_name.short_description = 'Patient Last Name'

    def get_formatted_time(self, obj):
        return obj.recorded_at.strftime("%H:%M") if obj.recorded_at else "-"
    get_formatted_time.short_description = 'Recorded At'

class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_type', 'get_patient_first_name', 'get_patient_last_name', 'get_author_name')

    def get_patient_first_name(self, obj):
        return obj.encounter.patient.first_name
    get_patient_first_name.short_description = 'Patient First Name'

    def get_patient_last_name(self, obj):
        return obj.encounter.patient.last_name
    get_patient_last_name.short_description = 'Patient Last Name'

    def get_author_name(self, obj):
        return obj.author.last_name if obj.author else "Unknown"
    get_author_name.short_description = 'Doctor'

admin.site.register(HospitalUser, HospitalUserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Encounter, EncounterAdmin)
admin.site.register(Triage, TriageAdmin)
admin.site.register(VitalSign, VitalSignAdmin)
admin.site.register(ClinicalNote, ClinicalNoteAdmin)