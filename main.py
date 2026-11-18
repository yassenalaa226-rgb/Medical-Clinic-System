# ==========================================================
# Medical Clinic System - Main GUI
# ==========================================================

import tkinter as tk
from tkinter import messagebox

from backend import *


# ==========================================================
# Main Window
# ==========================================================

window = tk.Tk()
window.title("Medical Clinic System")
window.state("zoomed")
window.minsize(1000, 650)


# ==========================================================
# Themes
# ==========================================================

LIGHT = {
    "background": "#F4F7FB", "card": "#FFFFFF", "text": "#102A43",
    "muted": "#627D98", "header": "#1976D2", "sidebar": "#172B4D",
    "entry": "#FFFFFF", "list": "#FFFFFF"
}

DARK = {
    "background": "#101820", "card": "#1B2733", "text": "#F5F7FA",
    "muted": "#B8C4CE", "header": "#1565C0", "sidebar": "#0B1320",
    "entry": "#243342", "list": "#18232E"
}

colors = LIGHT.copy()
current_theme = "light"
window.configure(bg=colors["background"])


# ==========================================================
# Main Layout
# ==========================================================

main_frame = tk.Frame(window, bg=colors["background"])
main_frame.pack(fill="both", expand=True)

header = tk.Frame(main_frame, bg=colors["header"], height=80)
header.pack(fill="x")
header.pack_propagate(False)

header_title = tk.Label(
    header, text="Medical Clinic System", bg=colors["header"], fg="white",
    font=("Arial", 24, "bold")
)
header_title.pack(side="left", padx=25, pady=10)

header_subtitle = tk.Label(
    header, text="Clinic Management Dashboard", bg=colors["header"], fg="white",
    font=("Arial", 12)
)
header_subtitle.pack(side="left", padx=10)

body = tk.Frame(main_frame, bg=colors["background"])
body.pack(fill="both", expand=True)

sidebar = tk.Frame(body, bg=colors["sidebar"], width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

sidebar_title = tk.Label(
    sidebar, text="MENU", bg=colors["sidebar"], fg="white",
    font=("Arial", 16, "bold")
)
sidebar_title.pack(pady=25)

content = tk.Frame(body, bg=colors["background"])
content.pack(side="right", fill="both", expand=True)

# Pages

dashboard_frame = tk.Frame(content, bg=colors["background"])
patients_frame = tk.Frame(content, bg=colors["background"])
doctors_frame = tk.Frame(content, bg=colors["background"])
appointments_frame = tk.Frame(content, bg=colors["background"])
settings_frame = tk.Frame(content, bg=colors["background"])


# ==========================================================
# Helper Functions
# ==========================================================

def hide_all_frames():
    for frame in [dashboard_frame, patients_frame, doctors_frame,
                  appointments_frame, settings_frame]:
        frame.pack_forget()


def field(parent, text, row, column):
    tk.Label(
        parent, text=text, bg=colors["card"], fg=colors["text"],
        font=("Arial", 10, "bold")
    ).grid(row=row, column=column, padx=10, pady=10)

    entry = tk.Entry(
        parent, width=25, font=("Arial", 10),
        bg=colors["entry"], fg=colors["text"],
        insertbackground=colors["text"], relief="solid", bd=1
    )
    entry.grid(row=row, column=column + 1, padx=10, pady=10)
    return entry


def clear_entries(entries):
    for entry in entries:
        entry.delete(0, tk.END)


# ==========================================================
# DASHBOARD
# ==========================================================

dashboard_title = tk.Label(
    dashboard_frame, text="Dashboard", bg=colors["background"], fg=colors["text"],
    font=("Arial", 26, "bold")
)
dashboard_title.pack(anchor="w", padx=30, pady=30)

stats = tk.Frame(dashboard_frame, bg=colors["background"])
stats.pack(fill="x", padx=30)

patient_count_label = tk.Label(
    stats, text="Patients: 0", bg=colors["card"], fg=colors["text"],
    font=("Arial", 18, "bold"), width=18, height=4, relief="groove", bd=2
)
patient_count_label.pack(side="left", padx=10)

doctor_count_label = tk.Label(
    stats, text="Doctors: 0", bg=colors["card"], fg=colors["text"],
    font=("Arial", 18, "bold"), width=18, height=4, relief="groove", bd=2
)
doctor_count_label.pack(side="left", padx=10)

appointment_count_label = tk.Label(
    stats, text="Appointments: 0", bg=colors["card"], fg=colors["text"],
    font=("Arial", 18, "bold"), width=20, height=4, relief="groove", bd=2
)
appointment_count_label.pack(side="left", padx=10)


def update_dashboard():
    patient_count_label.config(text=f"Patients: {len(get_all_patients())}")
    doctor_count_label.config(text=f"Doctors: {len(get_all_doctors())}")
    appointment_count_label.config(text=f"Appointments: {len(get_all_appointments())}")


# ==========================================================
# PATIENTS
# ==========================================================

patients_title = tk.Label(
    patients_frame, text="Patients", bg=colors["background"], fg=colors["text"],
    font=("Arial", 26, "bold")
)
patients_title.pack(anchor="w", padx=30, pady=20)

patient_form = tk.Frame(patients_frame, bg=colors["card"], bd=2, relief="groove")
patient_form.pack(fill="x", padx=30, pady=10)

patient_id_entry = field(patient_form, "Patient ID", 0, 0)
patient_name_entry = field(patient_form, "Name", 0, 2)
patient_age_entry = field(patient_form, "Age", 1, 0)
patient_phone_entry = field(patient_form, "Phone", 1, 2)
patient_doctor_entry = field(patient_form, "Doctor", 2, 0)
patient_date_entry = field(patient_form, "Appointment Date", 2, 2)


def clear_patient_form():
    clear_entries([patient_id_entry, patient_name_entry, patient_age_entry,
                   patient_phone_entry, patient_doctor_entry, patient_date_entry])


def add_patient_gui():
    patient_id = patient_id_entry.get().strip()
    name = patient_name_entry.get().strip()
    age_text = patient_age_entry.get().strip()
    phone = patient_phone_entry.get().strip()
    doctor_name = patient_doctor_entry.get().strip()
    appointment_date = patient_date_entry.get().strip()

    if not all([patient_id, name, age_text, phone, doctor_name, appointment_date]):
        messagebox.showerror("Error", "Please fill all patient fields.")
        return

    try:
        age = int(age_text)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    valid, message = validate_patient_data(
        patient_id, name, age, phone, doctor_name, appointment_date
    )
    if not valid:
        messagebox.showerror("Error", message)
        return

    if not add_patient(patient(patient_id, name, age, phone, doctor_name, appointment_date)):
        messagebox.showerror("Error", "Could not add patient.")
        return

    messagebox.showinfo("Success", "Patient added successfully.")
    show_all_patients()
    update_dashboard()
    clear_patient_form()


def search_patient_gui():
    patient_id = patient_id_entry.get().strip()
    if not patient_id:
        messagebox.showerror("Error", "Enter Patient ID first.")
        return

    p = search_patient_by_id(patient_id)
    if not p:
        messagebox.showerror("Error", "Patient not found.")
        return

    for entry, value in [
        (patient_name_entry, p.name), (patient_age_entry, p.age),
        (patient_phone_entry, p.phone), (patient_doctor_entry, p.doctor),
        (patient_date_entry, p.appointment_date)
    ]:
        entry.delete(0, tk.END)
        entry.insert(0, value)


def update_patient_gui():
    patient_id = patient_id_entry.get().strip()
    if not search_patient_by_id(patient_id):
        messagebox.showerror("Error", "Patient not found.")
        return

    name = patient_name_entry.get().strip()
    age_text = patient_age_entry.get().strip()
    phone = patient_phone_entry.get().strip()
    doctor_name = patient_doctor_entry.get().strip()
    appointment_date = patient_date_entry.get().strip()

    try:
        age = int(age_text)
    except ValueError:
        messagebox.showerror("Error", "Age must be a number.")
        return

    if not validate_name(name):
        messagebox.showerror("Error", "Invalid name.")
        return
    if not validate_age(age):
        messagebox.showerror("Error", "Age must be greater than 0.")
        return
    if not validate_phone(phone):
        messagebox.showerror("Error", "Phone must contain exactly 11 digits.")
        return
    if not validate_doctor(doctor_name):
        messagebox.showerror("Error", "Doctor name is required.")
        return
    if not validate_appointment_date(appointment_date):
        messagebox.showerror("Error", "Invalid appointment date. Use DD/MM/YYYY and choose today or a future date.")
        return

    edit_patient_by_id(patient_id, name, age, phone, doctor_name, appointment_date)
    messagebox.showinfo("Success", "Patient updated successfully.")
    show_all_patients()
    update_dashboard()


def delete_patient_gui():
    patient_id = patient_id_entry.get().strip()
    if not patient_id:
        messagebox.showerror("Error", "Enter Patient ID first.")
        return

    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?"):
        return

    if delete_patient_by_id(patient_id):
        messagebox.showinfo("Success", "Patient deleted successfully.")
        show_all_patients()
        update_dashboard()
        clear_patient_form()
    else:
        messagebox.showerror("Error", "Patient not found.")


patient_buttons = tk.Frame(patients_frame, bg=colors["background"])
patient_buttons.pack(pady=10)


def action_button(parent, text, command, bg, active_bg):
    tk.Button(
        parent, text=text, width=12, command=command, bg=bg, fg="white",
        activebackground=active_bg, activeforeground="white", relief="flat",
        font=("Arial", 10, "bold"), cursor="hand2"
    ).pack(side="left", padx=5)


action_button(patient_buttons, "Add", add_patient_gui, "#2E7D32", "#1B5E20")
action_button(patient_buttons, "Search", search_patient_gui, "#1976D2", "#1565C0")
action_button(patient_buttons, "Update", update_patient_gui, "#F9A825", "#F57F17")
action_button(patient_buttons, "Delete", delete_patient_gui, "#C62828", "#B71C1C")
action_button(patient_buttons, "Clear", clear_patient_form, "#607D8B", "#455A64")

patients_list = tk.Listbox(
    patients_frame, width=110, height=12, bg=colors["list"], fg=colors["text"],
    selectbackground="#1976D2", selectforeground="white", font=("Arial", 10)
)
patients_list.pack(padx=30, pady=10)


def show_all_patients():
    patients_list.delete(0, tk.END)
    for p in get_all_patients():
        patients_list.insert(
            tk.END,
            f"ID: {p.patient_id} | Name: {p.name} | Age: {p.age} | "
            f"Phone: {p.phone} | Doctor: {p.doctor} | Date: {p.appointment_date}"
        )


tk.Button(
    patients_frame, text="Show All Patients", command=show_all_patients,
    bg="#455A64", fg="white", activebackground="#37474F",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2"
).pack(pady=5)


# ==========================================================
# DOCTORS
# ==========================================================

doctors_title = tk.Label(
    doctors_frame, text="Doctors", bg=colors["background"], fg=colors["text"],
    font=("Arial", 26, "bold")
)
doctors_title.pack(anchor="w", padx=30, pady=20)

doctor_form = tk.Frame(doctors_frame, bg=colors["card"], bd=2, relief="groove")
doctor_form.pack(fill="x", padx=30, pady=10)

doctor_id_entry = field(doctor_form, "Doctor ID", 0, 0)
doctor_name_entry = field(doctor_form, "Name", 0, 2)
doctor_specialty_entry = field(doctor_form, "Specialty", 1, 0)
doctor_phone_entry = field(doctor_form, "Phone", 1, 2)


def clear_doctor_form():
    clear_entries([doctor_id_entry, doctor_name_entry, doctor_specialty_entry, doctor_phone_entry])


def add_doctor_gui():
    doctor_id = doctor_id_entry.get().strip()
    name = doctor_name_entry.get().strip()
    specialty = doctor_specialty_entry.get().strip()
    phone = doctor_phone_entry.get().strip()

    if not all([doctor_id, name, specialty, phone]):
        messagebox.showerror("Error", "Please fill all doctor fields.")
        return
    if doctor_id_exists(doctor_id):
        messagebox.showerror("Error", "Doctor ID already exists.")
        return
    if not validate_name(name) or not validate_specialty(specialty):
        messagebox.showerror("Error", "Name and Specialty are required.")
        return
    if not validate_phone(phone):
        messagebox.showerror("Error", "Phone must contain exactly 11 digits.")
        return

    if not add_doctor(doctor(doctor_id, name, specialty, phone)):
        messagebox.showerror("Error", "Could not add doctor.")
        return

    messagebox.showinfo("Success", "Doctor added successfully.")
    show_all_doctors()
    update_dashboard()
    clear_doctor_form()


def search_doctor_gui():
    doctor_id = doctor_id_entry.get().strip()
    if not doctor_id:
        messagebox.showerror("Error", "Enter Doctor ID first.")
        return

    d = search_doctor_by_id(doctor_id)
    if not d:
        messagebox.showerror("Error", "Doctor not found.")
        return

    for entry, value in [
        (doctor_name_entry, d.name), (doctor_specialty_entry, d.specialty),
        (doctor_phone_entry, d.phone)
    ]:
        entry.delete(0, tk.END)
        entry.insert(0, value)


def update_doctor_gui():
    doctor_id = doctor_id_entry.get().strip()
    if not search_doctor_by_id(doctor_id):
        messagebox.showerror("Error", "Doctor not found.")
        return

    name = doctor_name_entry.get().strip()
    specialty = doctor_specialty_entry.get().strip()
    phone = doctor_phone_entry.get().strip()

    if not validate_name(name) or not validate_specialty(specialty):
        messagebox.showerror("Error", "Name and Specialty are required.")
        return
    if not validate_phone(phone):
        messagebox.showerror("Error", "Phone must contain exactly 11 digits.")
        return

    edit_doctor_by_id(doctor_id, name, specialty, phone)
    messagebox.showinfo("Success", "Doctor updated successfully.")
    show_all_doctors()
    update_dashboard()


def delete_doctor_gui():
    doctor_id = doctor_id_entry.get().strip()
    if not doctor_id:
        messagebox.showerror("Error", "Enter Doctor ID first.")
        return
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
        return

    if delete_doctor_by_id(doctor_id):
        messagebox.showinfo("Success", "Doctor deleted successfully.")
        show_all_doctors()
        update_dashboard()
        clear_doctor_form()
    else:
        messagebox.showerror("Error", "Doctor not found.")


doctor_buttons = tk.Frame(doctors_frame, bg=colors["background"])
doctor_buttons.pack(pady=10)

action_button(doctor_buttons, "Add", add_doctor_gui, "#2E7D32", "#1B5E20")
action_button(doctor_buttons, "Search", search_doctor_gui, "#1976D2", "#1565C0")
action_button(doctor_buttons, "Update", update_doctor_gui, "#F9A825", "#F57F17")
action_button(doctor_buttons, "Delete", delete_doctor_gui, "#C62828", "#B71C1C")
action_button(doctor_buttons, "Clear", clear_doctor_form, "#607D8B", "#455A64")

doctors_list = tk.Listbox(
    doctors_frame, width=90, height=12, bg=colors["list"], fg=colors["text"],
    selectbackground="#1976D2", selectforeground="white", font=("Arial", 10)
)
doctors_list.pack(padx=30, pady=10)


def show_all_doctors():
    doctors_list.delete(0, tk.END)
    for d in get_all_doctors():
        doctors_list.insert(
            tk.END,
            f"ID: {d.doctor_id} | Name: {d.name} | "
            f"Specialty: {d.specialty} | Phone: {d.phone}"
        )


tk.Button(
    doctors_frame, text="Show All Doctors", command=show_all_doctors,
    bg="#455A64", fg="white", activebackground="#37474F",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2"
).pack(pady=5)


# ==========================================================
# APPOINTMENTS
# ==========================================================

appointments_title = tk.Label(
    appointments_frame, text="Appointments", bg=colors["background"], fg=colors["text"],
    font=("Arial", 26, "bold")
)
appointments_title.pack(anchor="w", padx=30, pady=20)

appointment_form = tk.Frame(appointments_frame, bg=colors["card"], bd=2, relief="groove")
appointment_form.pack(fill="x", padx=30, pady=10)

appointment_id_entry = field(appointment_form, "Appointment ID", 0, 0)
appointment_patient_id_entry = field(appointment_form, "Patient ID", 0, 2)
appointment_doctor_id_entry = field(appointment_form, "Doctor ID", 1, 0)
appointment_date_entry = field(appointment_form, "Date (DD/MM/YYYY)", 1, 2)
appointment_time_entry = field(appointment_form, "Time (HH:MM)", 2, 0)


def clear_appointment_form():
    clear_entries([
        appointment_id_entry, appointment_patient_id_entry,
        appointment_doctor_id_entry, appointment_date_entry,
        appointment_time_entry
    ])


def add_appointment_gui():
    appointment_id = appointment_id_entry.get().strip()
    patient_id = appointment_patient_id_entry.get().strip()
    doctor_id = appointment_doctor_id_entry.get().strip()
    appointment_date = appointment_date_entry.get().strip()
    appointment_time = appointment_time_entry.get().strip()

    if not all([appointment_id, patient_id, doctor_id, appointment_date, appointment_time]):
        messagebox.showerror("Error", "Please fill all appointment fields.")
        return
    if appointment_id_exists(appointment_id):
        messagebox.showerror("Error", "Appointment ID already exists.")
        return
    if not search_patient_by_id(patient_id):
        messagebox.showerror("Error", "Patient ID does not exist.")
        return
    if not search_doctor_by_id(doctor_id):
        messagebox.showerror("Error", "Doctor ID does not exist.")
        return
    if not validate_appointment_date(appointment_date):
        messagebox.showerror(
            "Error",
            "Invalid date.\n\nUse DD/MM/YYYY.\nExample: 25/12/2026.\n\n"
            "The date must be today or a future date."
        )
        return
    if not validate_appointment_time(appointment_time):
        messagebox.showerror("Error", "Invalid time.\n\nUse HH:MM.\nExample: 14:30.")
        return

    new_appointment = appointment(
        appointment_id, patient_id, doctor_id, appointment_date, appointment_time
    )
    if not add_appointment(new_appointment):
        messagebox.showerror("Error", "Could not add appointment.")
        return

    messagebox.showinfo("Success", "Appointment added successfully.")
    show_all_appointments()
    update_dashboard()
    clear_appointment_form()


def search_appointment_gui():
    appointment_id = appointment_id_entry.get().strip()
    if not appointment_id:
        messagebox.showerror("Error", "Enter Appointment ID first.")
        return

    a = search_appointment_by_id(appointment_id)
    if not a:
        messagebox.showerror("Error", "Appointment not found.")
        return

    for entry, value in [
        (appointment_patient_id_entry, a.patient_id),
        (appointment_doctor_id_entry, a.doctor_id),
        (appointment_date_entry, a.date),
        (appointment_time_entry, a.time)
    ]:
        entry.delete(0, tk.END)
        entry.insert(0, value)


def update_appointment_gui():
    appointment_id = appointment_id_entry.get().strip()
    if not search_appointment_by_id(appointment_id):
        messagebox.showerror("Error", "Appointment not found.")
        return

    patient_id = appointment_patient_id_entry.get().strip()
    doctor_id = appointment_doctor_id_entry.get().strip()
    appointment_date = appointment_date_entry.get().strip()
    appointment_time = appointment_time_entry.get().strip()

    if not search_patient_by_id(patient_id):
        messagebox.showerror("Error", "Patient ID does not exist.")
        return
    if not search_doctor_by_id(doctor_id):
        messagebox.showerror("Error", "Doctor ID does not exist.")
        return
    if not validate_appointment_date(appointment_date):
        messagebox.showerror("Error", "Invalid date. Use DD/MM/YYYY and choose today or a future date.")
        return
    if not validate_appointment_time(appointment_time):
        messagebox.showerror("Error", "Invalid time. Use HH:MM. Example: 14:30.")
        return

    if edit_appointment_by_id(
        appointment_id, patient_id, doctor_id, appointment_date, appointment_time
    ):
        messagebox.showinfo("Success", "Appointment updated successfully.")
        show_all_appointments()
        update_dashboard()
    else:
        messagebox.showerror("Error", "Could not update appointment.")


def delete_appointment_gui():
    appointment_id = appointment_id_entry.get().strip()
    if not appointment_id:
        messagebox.showerror("Error", "Enter Appointment ID first.")
        return
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?"):
        return

    if delete_appointment_by_id(appointment_id):
        messagebox.showinfo("Success", "Appointment deleted successfully.")
        show_all_appointments()
        update_dashboard()
        clear_appointment_form()
    else:
        messagebox.showerror("Error", "Appointment not found.")


appointment_buttons = tk.Frame(appointments_frame, bg=colors["background"])
appointment_buttons.pack(pady=10)

action_button(appointment_buttons, "Add", add_appointment_gui, "#2E7D32", "#1B5E20")
action_button(appointment_buttons, "Search", search_appointment_gui, "#1976D2", "#1565C0")
action_button(appointment_buttons, "Update", update_appointment_gui, "#F9A825", "#F57F17")
action_button(appointment_buttons, "Delete", delete_appointment_gui, "#C62828", "#B71C1C")
action_button(appointment_buttons, "Clear", clear_appointment_form, "#607D8B", "#455A64")

appointments_list = tk.Listbox(
    appointments_frame, width=90, height=12, bg=colors["list"], fg=colors["text"],
    selectbackground="#1976D2", selectforeground="white", font=("Arial", 10)
)
appointments_list.pack(padx=30, pady=10)


def show_all_appointments():
    appointments_list.delete(0, tk.END)
    for a in get_all_appointments():
        appointments_list.insert(
            tk.END,
            f"ID: {a.appointment_id} | Patient: {a.patient_id} | "
            f"Doctor: {a.doctor_id} | Date: {a.date} | Time: {a.time}"
        )


tk.Button(
    appointments_frame, text="Show All Appointments", command=show_all_appointments,
    bg="#455A64", fg="white", activebackground="#37474F",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2"
).pack(pady=5)


# ==========================================================
# SETTINGS
# ==========================================================

settings_title = tk.Label(
    settings_frame, text="Settings", bg=colors["background"], fg=colors["text"],
    font=("Arial", 26, "bold")
)
settings_title.pack(anchor="w", padx=30, pady=30)

settings_info = tk.Label(
    settings_frame, text="Program Settings", bg=colors["background"], fg=colors["muted"],
    font=("Arial", 12)
)
settings_info.pack(anchor="w", padx=30)


def toggle_theme():
    global current_theme, colors
    current_theme = "dark" if current_theme == "light" else "light"
    colors = DARK.copy() if current_theme == "dark" else LIGHT.copy()
    apply_theme()


def apply_theme():
    window.configure(bg=colors["background"])
    main_frame.configure(bg=colors["background"])
    body.configure(bg=colors["background"])
    content.configure(bg=colors["background"])

    header.configure(bg=colors["header"])
    header_title.configure(bg=colors["header"])
    header_subtitle.configure(bg=colors["header"])

    sidebar.configure(bg=colors["sidebar"])
    sidebar_title.configure(bg=colors["sidebar"])

    for frame in [dashboard_frame, patients_frame, doctors_frame,
                  appointments_frame, settings_frame]:
        frame.configure(bg=colors["background"])

    for title in [dashboard_title, patients_title, doctors_title,
                  appointments_title, settings_title]:
        title.configure(bg=colors["background"], fg=colors["text"])

    stats.configure(bg=colors["background"])
    for label in [patient_count_label, doctor_count_label, appointment_count_label]:
        label.configure(bg=colors["card"], fg=colors["text"])

    settings_info.configure(bg=colors["background"], fg=colors["muted"])

    for form in [patient_form, doctor_form, appointment_form]:
        form.configure(bg=colors["card"])
        for widget in form.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=colors["card"], fg=colors["text"])
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=colors["entry"], fg=colors["text"],
                    insertbackground=colors["text"]
                )

    for widget in [patients_list, doctors_list, appointments_list]:
        widget.configure(bg=colors["list"], fg=colors["text"])

    for frame in [patient_buttons, doctor_buttons, appointment_buttons]:
        frame.configure(bg=colors["background"])

    theme_button.configure(
        text="Switch to Dark Mode" if current_theme == "light" else "Switch to Light Mode"
    )


theme_button = tk.Button(
    settings_frame, text="Switch to Dark Mode", width=25, command=toggle_theme,
    bg="#1976D2", fg="white", activebackground="#1565C0",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2", relief="flat"
)
theme_button.pack(pady=15)


def clear_database_gui():
    if not messagebox.askyesno(
        "Confirm", "Are you sure you want to delete ALL patients, doctors and appointments?"
    ):
        return

    clear_all_data()
    show_all_patients()
    show_all_doctors()
    show_all_appointments()
    update_dashboard()
    clear_patient_form()
    clear_doctor_form()
    clear_appointment_form()

    messagebox.showinfo("Success", "All data has been cleared.")


tk.Button(
    settings_frame, text="Clear All Data", width=25, command=clear_database_gui,
    bg="#C62828", fg="white", activebackground="#B71C1C",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2", relief="flat"
).pack(pady=10)


def show_about():
    messagebox.showinfo(
        "About Medical Clinic System",
        "Medical Clinic System\n\n"
        "Patient Management\nDoctor Management\nAppointment Management\n"
        "SQLite Database\nBuilt with Python and Tkinter"
    )


tk.Button(
    settings_frame, text="About Program", width=25, command=show_about,
    bg="#455A64", fg="white", activebackground="#37474F",
    activeforeground="white", font=("Arial", 10, "bold"), cursor="hand2", relief="flat"
).pack(pady=10)


# ==========================================================
# Navigation
# ==========================================================

def show_dashboard():
    hide_all_frames()
    dashboard_frame.pack(fill="both", expand=True)
    update_dashboard()


def show_patients():
    hide_all_frames()
    patients_frame.pack(fill="both", expand=True)
    show_all_patients()


def show_doctors():
    hide_all_frames()
    doctors_frame.pack(fill="both", expand=True)
    show_all_doctors()


def show_appointments():
    hide_all_frames()
    appointments_frame.pack(fill="both", expand=True)
    show_all_appointments()


def show_settings():
    hide_all_frames()
    settings_frame.pack(fill="both", expand=True)


def sidebar_button(text, command):
    tk.Button(
        sidebar, text=text, width=20, height=2, command=command,
        bg=colors["header"], fg="white", activebackground="#1565C0",
        activeforeground="white", font=("Arial", 10, "bold"),
        relief="flat", cursor="hand2"
    ).pack(pady=5, padx=10)


sidebar_button("Dashboard", show_dashboard)
sidebar_button("Patients", show_patients)
sidebar_button("Appointments", show_appointments)
sidebar_button("Doctors", show_doctors)
sidebar_button("Settings", show_settings)


# ==========================================================
# Start Application
# ==========================================================

apply_theme()
show_dashboard()
window.mainloop()
