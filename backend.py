# ==========================================================
# Medical Clinic System - Backend
# ==========================================================

import sqlite3
from datetime import datetime, date
from pathlib import Path

# ==========================================================
# Database Setup
# ==========================================================

APP_FOLDER = Path.home() / "MedicalClinicSystem"
APP_FOLDER.mkdir(parents=True, exist_ok=True)
DATABASE_FILE = APP_FOLDER / "medical_clinic.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            doctor TEXT NOT NULL,
            appointment_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            doctor_id TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()


# ==========================================================
# Patient Class and Functions
# ==========================================================

class patient:
    def __init__(self, patient_id, name, age, phone, doctor, appointment_date):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.phone = phone
        self.doctor = doctor
        self.appointment_date = appointment_date


def add_patient(new_patient):
    try:
        connection = get_connection()
        connection.execute("""
            INSERT INTO patients
            (patient_id, name, age, phone, doctor, appointment_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (new_patient.patient_id, new_patient.name, new_patient.age,
              new_patient.phone, new_patient.doctor, new_patient.appointment_date))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False


def search_patient_by_id(patient_id):
    connection = get_connection()
    row = connection.execute("""
        SELECT patient_id, name, age, phone, doctor, appointment_date
        FROM patients WHERE patient_id = ?
    """, (patient_id,)).fetchone()
    connection.close()
    return patient(*row) if row else None


def get_all_patients():
    connection = get_connection()
    rows = connection.execute("""
        SELECT patient_id, name, age, phone, doctor, appointment_date
        FROM patients ORDER BY patient_id
    """).fetchall()
    connection.close()
    return [patient(*row) for row in rows]


def delete_patient_by_id(patient_id):
    connection = get_connection()
    cursor = connection.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
    connection.commit()
    result = cursor.rowcount > 0
    connection.close()
    return result


def edit_patient_by_id(patient_id, name=None, age=None, phone=None, doctor=None, appointment_date=None):
    old = search_patient_by_id(patient_id)
    if not old:
        return False
    name = old.name if name is None else name
    age = old.age if age is None else age
    phone = old.phone if phone is None else phone
    doctor = old.doctor if doctor is None else doctor
    appointment_date = old.appointment_date if appointment_date is None else appointment_date

    connection = get_connection()
    connection.execute("""
        UPDATE patients SET name=?, age=?, phone=?, doctor=?, appointment_date=?
        WHERE patient_id=?
    """, (name, age, phone, doctor, appointment_date, patient_id))
    connection.commit()
    connection.close()
    return True


def patient_id_exists(patient_id):
    return search_patient_by_id(patient_id) is not None


# ==========================================================
# Doctor Class and Functions
# ==========================================================

class doctor:
    def __init__(self, doctor_id, name, specialty, phone):
        self.doctor_id = doctor_id
        self.name = name
        self.specialty = specialty
        self.phone = phone


def add_doctor(new_doctor):
    try:
        connection = get_connection()
        connection.execute("""
            INSERT INTO doctors (doctor_id, name, specialty, phone)
            VALUES (?, ?, ?, ?)
        """, (new_doctor.doctor_id, new_doctor.name,
              new_doctor.specialty, new_doctor.phone))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False


def search_doctor_by_id(doctor_id):
    connection = get_connection()
    row = connection.execute("""
        SELECT doctor_id, name, specialty, phone
        FROM doctors WHERE doctor_id = ?
    """, (doctor_id,)).fetchone()
    connection.close()
    return doctor(*row) if row else None


def get_all_doctors():
    connection = get_connection()
    rows = connection.execute("""
        SELECT doctor_id, name, specialty, phone
        FROM doctors ORDER BY doctor_id
    """).fetchall()
    connection.close()
    return [doctor(*row) for row in rows]


def delete_doctor_by_id(doctor_id):
    connection = get_connection()
    cursor = connection.execute("DELETE FROM doctors WHERE doctor_id = ?", (doctor_id,))
    connection.commit()
    result = cursor.rowcount > 0
    connection.close()
    return result


def edit_doctor_by_id(doctor_id, name=None, specialty=None, phone=None):
    old = search_doctor_by_id(doctor_id)
    if not old:
        return False
    name = old.name if name is None else name
    specialty = old.specialty if specialty is None else specialty
    phone = old.phone if phone is None else phone

    connection = get_connection()
    connection.execute("""
        UPDATE doctors SET name=?, specialty=?, phone=? WHERE doctor_id=?
    """, (name, specialty, phone, doctor_id))
    connection.commit()
    connection.close()
    return True


def doctor_id_exists(doctor_id):
    return search_doctor_by_id(doctor_id) is not None


# ==========================================================
# Appointment Class and Functions
# ==========================================================

class appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, date, time):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time


def add_appointment(new_appointment):
    try:
        connection = get_connection()
        connection.execute("""
            INSERT INTO appointments (appointment_id, patient_id, doctor_id, date, time)
            VALUES (?, ?, ?, ?, ?)
        """, (new_appointment.appointment_id, new_appointment.patient_id,
              new_appointment.doctor_id, new_appointment.date, new_appointment.time))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False


def search_appointment_by_id(appointment_id):
    connection = get_connection()
    row = connection.execute("""
        SELECT appointment_id, patient_id, doctor_id, date, time
        FROM appointments WHERE appointment_id = ?
    """, (appointment_id,)).fetchone()
    connection.close()
    return appointment(*row) if row else None


def get_all_appointments():
    connection = get_connection()
    rows = connection.execute("""
        SELECT appointment_id, patient_id, doctor_id, date, time
        FROM appointments ORDER BY date, time
    """).fetchall()
    connection.close()
    return [appointment(*row) for row in rows]


def delete_appointment_by_id(appointment_id):
    connection = get_connection()
    cursor = connection.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
    connection.commit()
    result = cursor.rowcount > 0
    connection.close()
    return result


def edit_appointment_by_id(appointment_id, patient_id=None, doctor_id=None, date=None, time=None):
    old = search_appointment_by_id(appointment_id)
    if not old:
        return False
    patient_id = old.patient_id if patient_id is None else patient_id
    doctor_id = old.doctor_id if doctor_id is None else doctor_id
    date = old.date if date is None else date
    time = old.time if time is None else time

    try:
        connection = get_connection()
        connection.execute("""
            UPDATE appointments SET patient_id=?, doctor_id=?, date=?, time=?
            WHERE appointment_id=?
        """, (patient_id, doctor_id, date, time, appointment_id))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        return False


def appointment_id_exists(appointment_id):
    return search_appointment_by_id(appointment_id) is not None


# ==========================================================
# Validation Functions
# ==========================================================

def validate_name(name):
    return bool(name.strip())


def validate_age(age):
    return isinstance(age, int) and age > 0


def validate_phone(phone):
    return phone.isdigit() and len(phone) == 11


def validate_doctor(doctor_name):
    return bool(doctor_name.strip())


def validate_specialty(specialty):
    return bool(specialty.strip())


def validate_appointment_date(appointment_date):
    """Accept only a real DD/MM/YYYY date that is today or later."""
    try:
        selected_date = datetime.strptime(appointment_date.strip(), "%d/%m/%Y").date()
        return selected_date >= date.today()
    except ValueError:
        return False


def validate_appointment_time(appointment_time):
    """Accept only a real 24-hour HH:MM time."""
    try:
        datetime.strptime(appointment_time.strip(), "%H:%M")
        return True
    except ValueError:
        return False


def validate_patient_data(patient_id, name, age, phone, doctor_name, appointment_date, check_id=True):
    if not patient_id.strip():
        return False, "Patient ID is required."
    if check_id and patient_id_exists(patient_id):
        return False, "Patient ID already exists."
    if not validate_name(name):
        return False, "Invalid name."
    if not validate_age(age):
        return False, "Age must be greater than 0."
    if not validate_phone(phone):
        return False, "Phone must contain exactly 11 digits."
    if not validate_doctor(doctor_name):
        return False, "Doctor name is required."
    if not validate_appointment_date(appointment_date):
        return False, "Invalid appointment date. Use DD/MM/YYYY and choose today or a future date."
    return True, "All data is valid."


# ==========================================================
# Clear Database
# ==========================================================

def clear_all_data():
    connection = get_connection()
    connection.execute("DELETE FROM appointments")
    connection.execute("DELETE FROM patients")
    connection.execute("DELETE FROM doctors")
    connection.commit()
    connection.close()


# ==========================================================
# Initialize Database
# ==========================================================

initialize_database()
