from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from abc import ABC
from django.db import connection
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.urls import reverse #for cookies


class User(ABC):
    def __init__(self, id, name, surname):
        self._id = id
        self._name = name 
        self._surname = surname 

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value


class Admin(User):
    def __init__(self, id, password, name, surname):
        super().__init__(id, password, name, surname)


class Doctor(User):
    def __init__(self, id, password, name, surname, specialization):
        super().__init__(id, password, name, surname)
        self._specialization = specialization

    @property
    def specialization(self):
        return self._specialization

    @specialization.setter
    def specialization(self, value):
        self._specialization = value


class Patient(User):
    def __init__(self, id, password, name, surname):
        super().__init__(id, password, name, surname)

from django.contrib import messages

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  # Bu kısmı HTML formunuza eklemeniz gerekecek

        user = None
        if user_type == 'admin':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_page')
            else:
                messages.error(request, 'Invalid admin credentials.')
        elif user_type == 'doctor':
             user = authenticate(request, username=username, password=password)
             if user is not None:
                login(request, user)
                return redirect('doctor_page')
        elif user_type == 'patient':
              user = authenticate(request, username=username, password=password)
              if user is not None:
                login(request, user)
                return redirect('patient_page')

    return render(request, 'home.html')


def admin_page(request):
    username = request.COOKIES.get('username')
    if username:
        # If the username cookie exists, pass it to the template
        context = {'username': username}
        return render(request, 'admin.html', context)
    else:
        # Handle cases where the cookie is not set
        # For example, redirect to login page or show an error message
        context = {'error': 'No username found. Please log in.'}
        return render(request, 'admin.html',context)

def doctor_page(request):
    username = request.COOKIES.get('username')
    if username:
        # If the username cookie exists, pass it to the template
        context = {'username': username}
        return render(request, 'doctor.html', context)
    else:
        # Handle cases where the cookie is not set
        # For example, redirect to login page or show an error message
        context = {'error': 'No username found. Please log in.'}
        return render(request, 'doctor.html',context)
    
def patient_page(request):
    return render(request, 'patient.html')


#login methods
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('admin-username')
        password = request.POST.get('admin-password')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM admin WHERE id = %s AND sifre = %s", [username, password])
                row = cursor.fetchone()

            if row:
                # Assuming you handle session or authentication here
                
                return JsonResponse({'status': 'success', 'message': 'Login successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid admin credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def doctor_login(request):
     if request.method == 'POST':
        username = request.POST.get('doctor-username')
        password = request.POST.get('doctor-password')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM doctor WHERE doctor_id = %s AND sifre = %s", [username, password])
                row = cursor.fetchone()

            if row:
                # Assuming you handle session or authentication here
        
                return JsonResponse({'status': 'success', 'message': 'Login successful'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid admin credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('patient-username')
        password = request.POST.get('patient-password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM patient WHERE patient_id = %s AND sifre = %s", [username, password])
            row = cursor.fetchone()

        if row:  # Kullanıcı bulunduysa
            # Burada gerekli işlemleri yapın, örneğin kullanıcıyı oturum açmış olarak işaretleyin
            # ve ynlendirin
            return redirect('patient')
        else:
            messages.error(request, 'Invalid patient credentials.')

    return render(request, 'home.html')

#admin methods

# patient add
def add_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Patient (Patient_ID, Sifre, Ad, Soyad, "Doğum Tarihi", Cinsiyet, Tel, Adres)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [patient_id, password, name, surname, birth_date, gender, phone, address])

        return render(request, 'admin.html', {'message': 'Patient added successfully.'})

    return render(request, 'admin.html')

#doctor add
def add_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        specialization = request.POST.get('specialization')
        hospital = request.POST.get('hospital')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Doctor (Doctor_ID, Sifre, Ad, Soyad, Uzmanlık, Hastane)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [doctor_id, password, name, surname, specialization, hospital])

        return render(request, 'admin.html', {'message': 'Doctor added successfully.'})

    return render(request, 'admin.html')

# delete patient
def delete_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Patient WHERE Patient_ID = %s", [patient_id])
            cursor.execute("DELETE FROM randevu WHERE Patient_ID = %s", [patient_id])
            cursor.execute("DELETE FROM rapor WHERE Patient_ID = %s", [patient_id])
            
        return render(request, 'admin.html', {'message': 'Patient deleted successfully.'})

    return render(request, 'admin.html')

#delete doctor
def delete_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')

        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Doctor WHERE Doctor_ID = %s", [doctor_id])
            cursor.execute("DELETE FROM randevu WHERE Doctor_ID = %s", [doctor_id])
            cursor.execute("DELETE FROM rapor WHERE Doctor_ID = %s", [doctor_id])  

        return render(request, 'admin.html', {'message': 'Doctor deleted successfully.'})

    return render(request, 'admin.html')

#update patient
def update_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        new_password = request.POST.get('new_password')
        new_name = request.POST.get('new_name')
        new_surname = request.POST.get('new_surname')
        new_birth_date = request.POST.get('new_birth_date')
        new_gender = request.POST.get('new_gender')
        new_phone = request.POST.get('new_phone')
        new_address = request.POST.get('new_address')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Patient
                SET Sifre = %s, Ad = %s, Soyad = %s, "Doğum Tarihi" = %s, Cinsiyet = %s, Tel = %s, Adres = %s
                WHERE Patient_ID = %s
            """, [new_password, new_name, new_surname, new_birth_date, new_gender, new_phone, new_address, patient_id])

        return render(request, 'admin.html', {'message': 'patient updated successfully.'})

    return render(request, 'admin.html')

#update doctor
def update_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        new_password = request.POST.get('new_password')
        new_name = request.POST.get('new_name')
        new_surname = request.POST.get('new_surname')
        new_specialization = request.POST.get('new_specialization')
        new_hospital = request.POST.get('new_hospital')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Doctor
                SET Sifre = %s, Ad = %s, Soyad = %s, Uzmanlık = %s, Hastane = %s
                WHERE Doctor_ID = %s
            """, [new_password, new_name, new_surname, new_specialization, new_hospital, doctor_id])

        return render(request, 'admin.html', {'message': 'Doctor updated successfully.'})

    return render(request, 'admin.html')

def update_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_date = request.POST.get('new_date')
        new_time = request.POST.get('new_time')
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Randevu
                SET Tarih = %s, Saat = %s
                WHERE Randevu_ID = %s
            """, [new_date, new_time, appointment_id])

        return render(request, 'admin.html', {'message': 'Appointment updated successfully.'})

    return render(request, 'admin.html')


def delete_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Rapor
                WHERE Rapor_ID = %s
            """, [report_id])

        return render(request, 'admin.html', {'message': 'Report deleted successfully.'})

    return render(request, 'admin.html')

# Rapor Ekleme
def add_report(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')
        report_date = request.POST.get('report_date')
        report_content = request.POST.get('report_content')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Rapor (Randevu_ID, Doctor_ID, Patient_ID, Rapor_Tarihi, Rapor_Icerigi)
                VALUES (%s, %s, %s, %s, %s)
            """, [appointment_id, doctor_id, patient_id, report_date, report_content])

        return render(request, 'admin.html', {'message': 'Report added successfully.'})

    return render(request, 'admin.html')

# Rapor Güncelleme
def update_report(request):
    if request.method == 'POST':
        report_id = request.POST.get('report_id')
        new_report_date = request.POST.get('new_report_date')
        new_report_content = request.POST.get('new_report_content')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Rapor
                SET Rapor_Tarihi = %s, Rapor_Icerigi = %s
                WHERE Rapor_ID = %s
            """, [new_report_date, new_report_content, report_id])

        return render(request, 'admin.html', {'message': 'Report updated successfully.'})

    return render(request, 'admin.html')

def list_patients(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM patient")
        patients = cursor.fetchall()

    patient_list = []
    for patient in patients:
        patient_dict = {
            'patient_id': patient[0],
            'sifre': patient[1],
            'ad': patient[2],
            'soyad': patient[3],
            'Doğum Tarihi': patient[4],
            'cinsiyet': patient[5],
            'tel': patient[6],
            'adres': patient[7],
        }
        patient_list.append(patient_dict)

    return JsonResponse({'patients': patient_list})

# Doktorları Listeleme API
def list_doctors(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM doctor")
        doctors = cursor.fetchall()

    doctor_list = []
    for doctor in doctors:
        doctor_dict = {
            'doctor_id': doctor[0],
            'sifre': doctor[1],
            'ad': doctor[2],
            'soyad':doctor[3],
            'uzmanlık':doctor[4],
            'hastane':doctor[5],



        }
        doctor_list.append(doctor_dict)

    return JsonResponse({'doctors': doctor_list})

def list_appointments(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Randevu")
        appointments = cursor.fetchall()

    appointment_list = []
    for appointment in appointments:
        appointment_dict = {
            'randevu_id': appointment[0],
            'tarih': appointment[1],
            'saat': appointment[2],
            'doctor_id':appointment[3],
            'patient_id':appointment[4],
        }
        appointment_list.append(appointment_dict)

    return JsonResponse({'appointments': appointment_list})

def list_reports(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Rapor")
        reports = cursor.fetchall()

    report_list = []
    for report in reports:
        report_dict = {
            'Rapor_ID': report[0],
            'Randevu_ID': report[1],
            'Doctor_ID': report[2],
            'Patient_ID': report[3],
            'Rapor_Tarihi': report[4],
            'Rapor_Icerigi': report[5]
        }
        report_list.append(report_dict)

    return JsonResponse({'reports': report_list})


def patient_show_randevu(request, pid):
    print("View called with pid:", pid)  # Debugging output
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM randevu WHERE patient_id = %s", [int(pid)])
        randevu = cursor.fetchall()
    print("Appointments fetched:", randevu)  # Debugging output

    # Randevuları JSON uyumlu bir formata dnştr
    randevu_list = [
        {
            'randevu_id': row[0],
            'tarih': row[1],
            'saat': row[2],
            'doctor_id': row[3],
            'patient_id': row[4]
        } for row in randevu
    ]

    return JsonResponse({'randevu': randevu_list})


#profil bilgisi
def patient_profil(request, pid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Patient WHERE Patient_ID = %s", [pid])
        profil = cursor.fetchone()
        
    if profil:
        profil_dict = {
            'patient_id': profil[0],
            'ad': profil[2],
            'soyad': profil[3],
            'Doğum Tarihi': profil[4],
            'cinsiyet': profil[5],
            'tel': profil[6],
            'adres': profil[7]
        }
        return JsonResponse({'profil': profil_dict})
    else:
        return JsonResponse({'error': 'Profil bulunamadı'}, status=404)

#randevu alma
def patient_add_randevu(request, pid):
    if request.method == 'POST':
        date = request.POST.get('tarih')
        time = request.POST.get('saat')
        doctor_id = request.POST.get('doctor_id')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Randevu (Tarih, Saat, Doctor_ID, Patient_ID)
                VALUES (%s, %s, %s, %s)
            """, [date, time, doctor_id, pid])

        return render(request, 'patient.html', {'message': 'Appointment successfully booked.'})

    return render(request, 'patient.html')

#randevu silme
def patient_delete_randevu(request, rid):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM Randevu
                WHERE Randevu_ID = %s
            """, [rid])

        return JsonResponse({'success': True, 'message': 'Appointment successfully deleted.'})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Add a new view function in views.py to handle adding reports
def patient_add_reports(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')
        report_date = request.POST.get('report_date')
        report_content = request.POST.get('report_content')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Rapor (Randevu_ID, Doctor_ID, Patient_ID, Rapor_Tarihi, Rapor_Icerigi)
                VALUES (%s, %s, %s, %s, %s)
            """, [appointment_id, doctor_id, patient_id, report_date, report_content])

        return render(request, 'patient.html', {'message': 'Report added successfully.'})

    return render(request, 'patient.html')

def patient_show_reports(request, pid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Rapor WHERE Patient_ID = %s", [pid])
        reports = cursor.fetchall()

    report_list = []
    for report in reports:
        report_dict = {
            'Rapor_ID': report[0],
            'Randevu_ID': report[1],
            'Doctor_ID': report[2],
            'Patient_ID': report[3],
            'Rapor_Tarihi': report[4],
            'Rapor_Icerigi': report[5]
        }
        report_list.append(report_dict)

    return JsonResponse({'reports': report_list})
#doctor methods

def doctor_show_randevu(request, did):
    print("View called with did:", did)  # Debugging output
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM randevu WHERE doctor_id = %s", [int(did)])
        randevu = cursor.fetchall()
    print("Appointments fetched:", randevu)  # Debugging output

    # Randevuları JSON uyumlu bir formata dönüştür
    randevu_list = [
        {
            'randevu_id': row[0],
            'tarih': row[1],
            'saat': row[2],
            'doctor_id': row[3],
            'patient_id': row[4]
        } for row in randevu
    ]

    return JsonResponse({'randevu': randevu_list})



#doctor got patients method
def doctor_got_patients(request, did):
    with connection.cursor() as cursor:

        cursor.execute("SELECT Patient_ID FROM Randevu WHERE Doctor_ID = %s", [did])
        patient_ids = cursor.fetchall()
        
        patients_list = []
        for pid in patient_ids:
            cursor.execute("SELECT * FROM Patient WHERE Patient_ID = %s", [pid[0]])
            patient = cursor.fetchone()
            if patient:
                patients_list.append({
                    'id': patient[0], 
                    'name': patient[2], 
                    'surname': patient[3], 
                    'birthday': patient[4], 
                    'gender': patient[5], 
                    'phone': patient[6], 
                    'address': patient[7]
                })

    return JsonResponse({'patients': patients_list})

def doctor_show_reports(request, did):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rapor WHERE doctor_id = %s", [did])
        reports = cursor.fetchall()

    report_list = []
    for report in reports:
        report_dict = {
            'Rapor_ID': report[0],
            'Randevu_ID': report[1],
            'Doctor_ID': report[2],
            'Patient_ID': report[3],
            'Rapor_Tarihi': report[4],
            'Rapor_Icerigi': report[5]
        }
        report_list.append(report_dict)

    return JsonResponse({'reports': report_list})


def doctor_add_report(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')  # Doctor ID'sini al
        appointment_id = request.POST.get('appointment_id')
        patient_id = request.POST.get('patient_id')
        report_date = request.POST.get('report_date')
        report_content = request.POST.get('report_content')
        
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Rapor (Randevu_ID, Doctor_ID, Patient_ID, Rapor_Tarihi, Rapor_Icerigi)
                VALUES (%s, %s, %s, %s, %s)
            """, [appointment_id, doctor_id, patient_id, report_date, report_content])

        return render(request, 'doctor.html', {'message': 'Report added successfully.'})

    return render(request, 'doctor.html')