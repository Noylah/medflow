from django.urls import path
from . import views

urlpatterns = [
    # --- CRUD VIEWS ---
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/<int:id>", views.patient_detail, name="patient_detail"),
    path("encounters/", views.encounter_list, name="encounter_list"),
    path("encounters/<int:id>", views.encounter_detail, name="encounter_detail"),
    path("triages/", views.triage_list, name="triage_list"),
    path("triages/<int:id>", views.triage_detail, name="triage_detail"),
    path("vitalsigns/", views.vitalsign_list, name="vitalsign_list"),
    path("vitalsigns/<int:id>", views.vitalsign_detail, name="vitalsign_detail"),
    path("clinicalnotes/", views.clinicalnote_list, name="clinicalnote_list"),
    path("clinicalnotes/<int:id>", views.clinicalnote_detail, name="clinicalnote_detail"),
    path("users/", views.user_list, name="user_list"),
    path("users/<int:id>", views.user_detail, name="user_detail"),
    # --- AUTH VIEWS ---
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('changepassword/', views.change_password, name='change_password'),
    # --- OTHER VIEWS ---
    path('encounters/<int:encounter_id>/discharge', views.discharge_patient, name='discharge_patient'),
    path('patients/<int:patient_id>/timeline', views.patient_timeline, name='patient_timeline'),
    path('patients/<int:patient_id>/latest_encounter', views.patient_latest_encounter, name='patient_latest_encounter'),

]