from __future__ import annotations
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from src.auth import hash_password, verify_password, Authenticator
from src.model import Admin
from src.patient_manager import PatientManager
from src.doctor_manager import DoctorManager
from src.appointment_manager import AppointmentManager
from src.persistence import StorageManager
from src.utility import clear_screen, validate_age, validate_phone

console = Console()
storage = StorageManager()

patient_mgr = PatientManager(user_storage=storage)
doctor_mgr = DoctorManager(user_storage=storage)
appt_mgr = AppointmentManager(clinic_storage=storage)
authenticator = Authenticator(patient_manager=patient_mgr)


def display_menu():
    clear_screen()
    console.print(
        Panel.fit(
            "[bold cyan]MEDIFLOW CLINIC MANAGEMENT SYSTEM[/bold cyan]\n"
            "[dim]Interactive Command-Line Application[/dim]",
            border_style="cyan",
        )
    )
    console.print("[1] Login")
    console.print("[2] Register Patient")
    console.print("[3] List All Patients")
    console.print("[4] Search Patient Record")
    console.print("[5] Delete Patient")
    console.print("[6] Register Doctor")
    console.print("[7] Book Appointment")
    console.print("[8] List Appointments")
    console.print("[9] Register Admin")
    console.print("[10] Save & Exit\n")


def register_patient_ui():
    console.print("\n[bold cyan]--- Register New Patient ---[/bold cyan]")
    username = Prompt.ask("Enter patient username").strip()
    if not username:
        console.print("[bold red]Username cannot be empty![/bold red]")
        return

    password = Prompt.ask("Enter password", password=True)
    age = IntPrompt.ask("Enter age")
    while not validate_age(str(age)):
        console.print("[bold red]Age must be between 0 and 120.[/bold red]")
        age = IntPrompt.ask("Enter age")

    contact = Prompt.ask("Enter contact number")
    while not validate_phone(contact):
        console.print(
            "[bold red]Invalid phone format. Please enter a valid number (e.g., 0712345678 or +254...).[/bold red]"
        )
        contact = Prompt.ask("Enter contact number")

    password_hash, salt = hash_password(password)

    patient = patient_mgr.create_patient(
        username=username,
        password_hash=password_hash,
        salt=salt,
        age=age,
        contact=contact,
    )
    if patient:
        console.print(
            f"\n[bold green]Patient '{username}' registered successfully![/bold green]"
        )
    else:
        console.print(
            f"\n[bold red]Registration failed. Username '{username}' already exists.[/bold red]"
        )


def list_patients_ui():
    patients = patient_mgr.get_all_patients()
    if not patients:
        console.print("\n[yellow]No patient records found.[/yellow]")
        return

    table = Table(title="Registered Patients", border_style="blue")
    table.add_column("Username", style="cyan", no_wrap=True)
    table.add_column("Age", style="magenta")
    table.add_column("Contact", style="green")
    table.add_column("Role", style="yellow")

    for p in patients:
        table.add_row(
            p.username,
            str(p.age) if p.age is not None else "N/A",
            getattr(p, "contact", "N/A") or "N/A",
            getattr(p, "role", "patient"),
        )

    console.print("\n")
    console.print(table)


def search_patient_ui():
    username = Prompt.ask("\nEnter username to search").strip()
    patient = patient_mgr.get_patient_by_username(username)

    if patient:
        console.print(
            Panel(
                f"[bold]Username:[/bold] {patient.username}\n"
                f"[bold]Age:[/bold] {patient.age}\n"
                f"[bold]Contact:[/bold] {getattr(patient, 'contact', 'N/A')}\n"
                f"[bold]Role:[/bold] {getattr(patient, 'role', 'patient')}",
                title=f"Record: {patient.username}",
                border_style="green",
            )
        )
    else:
        console.print(
            f"\n[bold red]Patient '{username}' not found.[/bold red]"
        )


def delete_patient_ui():
    username = Prompt.ask("\nEnter username to delete").strip()
    if patient_mgr.delete_patient(username):
        console.print(
            f"\n[bold green]Patient '{username}' removed successfully.[/bold green]"
        )
    else:
        console.print(
            f"\n[bold red]Patient '{username}' not found.[/bold red]"
        )


def register_doctor_ui():
    console.print("\n[bold cyan]--- Register New Doctor ---[/bold cyan]")
    username = Prompt.ask("Enter doctor username").strip()
    if not username:
        console.print("[bold red]Username cannot be empty![/bold red]")
        return

    password = Prompt.ask("Enter password", password=True)
    specialization = Prompt.ask("Enter specialization", default="General")
    days_input = Prompt.ask("Enter available days (comma separated, e.g. Monday,Wednesday)")
    available_days = [d.strip() for d in days_input.split(",") if d.strip()]

    password_hash, salt = hash_password(password)

    doctor = doctor_mgr.create_doctor(
        username=username,
        password_hash=password_hash,
        salt=salt,
        specialization=specialization,
        available_days=available_days,
    )
    if doctor:
        console.print(f"\n[bold green]Doctor '{username}' registered successfully![/bold green]")
    else:
        console.print(f"\n[bold red]Registration failed. Username '{username}' already exists.[/bold red]")


def book_appointment_ui(patient_username: str = None):
    console.print("\n[bold cyan]--- Book Appointment ---[/bold cyan]")
    if not patient_username:
        patient_username = Prompt.ask("Enter patient username").strip()
    if not patient_mgr.get_patient_by_username(patient_username):
        console.print(f"[bold red]Patient '{patient_username}' not found.[/bold red]")
        return

    doctor_username = Prompt.ask("Enter doctor username").strip()
    if not doctor_mgr.get_doctor_by_id(doctor_username):
        console.print(f"[bold red]Doctor '{doctor_username}' not found.[/bold red]")
        return

    reason = Prompt.ask("Reason for visit")

    appt = appt_mgr.create_appointment(
        doctor_username=doctor_username,
        patient_username=patient_username,
        when=datetime.now(),
        reason=reason,
    )
    if appt:
        console.print(f"\n[bold green]Appointment booked for '{patient_username}' with Dr. {doctor_username}.[/bold green]")
    else:
        console.print("\n[bold red]Could not book appointment (conflict or error).[/bold red]")


def list_appointments_ui():
    appointments = appt_mgr.get_all_appointments()
    if not appointments:
        console.print("\n[yellow]No appointments found.[/yellow]")
        return

    table = Table(title="Appointments", border_style="blue")
    table.add_column("Patient", style="cyan")
    table.add_column("Doctor", style="magenta")
    table.add_column("When", style="green")
    table.add_column("Reason", style="yellow")
    table.add_column("Status", style="white")

    for a in appointments:
        table.add_row(
            a.patient_username,
            a.doctor_username,
            a.when.strftime("%Y-%m-%d %H:%M"),
            a.reason,
            a.status.value,
        )

    console.print("\n")
    console.print(table)


def register_admin_ui():
    console.print("\n[bold cyan]--- Register New Admin ---[/bold cyan]")
    username = Prompt.ask("Enter admin username").strip()
    if not username:
        console.print("[bold red]Username cannot be empty![/bold red]")
        return

    clinic_data = storage.load_data()
    admins_dict = clinic_data.setdefault("admins", {})
    if username in admins_dict:
        console.print(f"[bold red]Username '{username}' already exists.[/bold red]")
        return

    password = Prompt.ask("Enter password", password=True)
    password_hash, salt = hash_password(password)

    admin = Admin(username=username, password_hash=password_hash, salt=salt)
    admins_dict[username] = admin.to_dict()
    storage.save_data(clinic_data)
    console.print(f"\n[bold green]Admin '{username}' registered successfully![/bold green]")


def login_ui():
    console.print("\n[bold cyan]--- Login ---[/bold cyan]")
    console.print("[1] Patient")
    console.print("[2] Doctor")
    console.print("[3] Admin")
    role_choice = IntPrompt.ask("Login as", choices=["1", "2", "3"])

    username = Prompt.ask("Enter username").strip()
    password = Prompt.ask("Enter password", password=True)

    if role_choice == 1:
        patient = authenticator.login(username, password)
        if patient:
            console.print(f"\n[bold green]Login successful. Welcome, {patient.username}![/bold green]")
            patient_dashboard(patient)
        else:
            console.print("\n[bold red]Invalid username or password.[/bold red]")

    elif role_choice == 2:
        doctor = doctor_mgr.get_doctor_by_id(username)
        if doctor and verify_password(doctor.get_password_hash(), doctor.salt, password):
            console.print(f"\n[bold green]Login successful. Welcome, Dr. {doctor.username}![/bold green]")
            doctor_dashboard(doctor)
        else:
            console.print("\n[bold red]Invalid username or password.[/bold red]")

    elif role_choice == 3:
        clinic_data = storage.load_data()
        admin_data = clinic_data.get("admins", {}).get(username)
        if admin_data:
            admin = Admin.from_dict(admin_data)
            if verify_password(admin.get_password_hash(), admin.salt, password):
                console.print(f"\n[bold green]Login successful. Welcome, {admin.username}![/bold green]")
                admin_dashboard()
            else:
                console.print("\n[bold red]Invalid username or password.[/bold red]")
        else:
            console.print("\n[bold red]Invalid username or password.[/bold red]")


def patient_dashboard(patient):
    while True:
        console.print(f"\n[bold cyan]--- Patient Dashboard: {patient.username} ---[/bold cyan]")
        console.print("[1] View My Appointments")
        console.print("[2] Book Appointment")
        console.print("[3] View My Doctor")
        console.print("[4] Logout")

        choice = IntPrompt.ask("Select an option", choices=["1", "2", "3", "4"])

        if choice == 1:
            view_my_appointments_ui(patient)
        elif choice == 2:
            book_appointment_ui(patient_username=patient.username)
        elif choice == 3:
            view_my_doctor_ui(patient)
        elif choice == 4:
            console.print("\n[bold green]Logged out.[/bold green]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


def view_my_appointments_ui(patient):
    appointments = appt_mgr.get_appointments_by_patient(patient.username)
    if not appointments:
        console.print("\n[yellow]You have no appointments.[/yellow]")
        return

    table = Table(title="My Appointments", border_style="blue")
    table.add_column("Doctor", style="cyan")
    table.add_column("When", style="green")
    table.add_column("Reason", style="yellow")
    table.add_column("Status", style="magenta")
    for a in appointments:
        table.add_row(
            a.doctor_username,
            a.when.strftime("%Y-%m-%d %H:%M"),
            a.reason,
            a.status.value,
        )
    console.print("\n")
    console.print(table)


def view_my_doctor_ui(patient):
    if not patient.assigned_doctor:
        console.print("\n[yellow]You have not been assigned a doctor yet.[/yellow]")
        return
    doctor = doctor_mgr.get_doctor_by_id(patient.assigned_doctor)
    if not doctor:
        console.print(f"\n[bold red]Assigned doctor '{patient.assigned_doctor}' not found.[/bold red]")
        return
    console.print(
        Panel(
            f"[bold]Name:[/bold] Dr. {doctor.username}\n"
            f"[bold]Specialization:[/bold] {doctor.specialization}\n"
            f"[bold]Available Days:[/bold] {', '.join(doctor.available_days) if doctor.available_days else 'N/A'}",
            title="My Doctor",
            border_style="green",
        )
    )


def doctor_dashboard(doctor):
    while True:
        console.print(f"\n[bold cyan]--- Doctor Dashboard: Dr. {doctor.username} ---[/bold cyan]")
        console.print("[1] View My Patients")
        console.print("[2] Search Patient Record")
        console.print("[3] Add Patient Medical Record")
        console.print("[4] View My Appointments")
        console.print("[5] Accept Appointment")
        console.print("[6] Logout")

        choice = IntPrompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])

        if choice == 1:
            view_my_patients_ui(doctor)
        elif choice == 2:
            search_patient_ui()
        elif choice == 3:
            add_patient_record_ui()
        elif choice == 4:
            view_doctor_appointments_ui(doctor)
        elif choice == 5:
            accept_appointment_ui(doctor)
        elif choice == 6:
            console.print("\n[bold green]Logged out.[/bold green]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


def view_my_patients_ui(doctor):
    patients = patient_mgr.get_patients_by_doctor(doctor.username)
    if not patients:
        console.print("\n[yellow]No patients assigned to you yet.[/yellow]")
        return
    table = Table(title=f"Patients assigned to Dr. {doctor.username}", border_style="blue")
    table.add_column("Username", style="cyan")
    table.add_column("Age", style="magenta")
    table.add_column("Contact", style="green")
    for p in patients:
        table.add_row(
            p.username,
            str(p.age) if p.age is not None else "N/A",
            p.contact or "N/A",
        )
    console.print("\n")
    console.print(table)


def add_patient_record_ui():
    username = Prompt.ask("\nEnter patient username").strip()
    if not patient_mgr.get_patient_by_username(username):
        console.print(f"[bold red]Patient '{username}' not found.[/bold red]")
        return
    entry = Prompt.ask("Enter medical record entry")
    if patient_mgr.update_patient(username, new_medical_entry=entry):
        console.print(f"\n[bold green]Record added to '{username}'.[/bold green]")
    else:
        console.print("\n[bold red]Failed to update record.[/bold red]")


def view_doctor_appointments_ui(doctor):
    appointments = appt_mgr.get_appointments_by_doctor(doctor.username)
    if not appointments:
        console.print("\n[yellow]No appointments found.[/yellow]")
        return
    table = Table(title=f"Appointments for Dr. {doctor.username}", border_style="blue")
    table.add_column("Patient", style="cyan")
    table.add_column("When", style="green")
    table.add_column("Reason", style="yellow")
    table.add_column("Status", style="magenta")
    for a in appointments:
        table.add_row(
            a.patient_username,
            a.when.strftime("%Y-%m-%d %H:%M"),
            a.reason,
            a.status.value,
        )
    console.print("\n")
    console.print(table)


def accept_appointment_ui(doctor):
    pending = [
        a for a in appt_mgr.get_appointments_by_doctor(doctor.username)
        if a.status.value == "pending"
    ]
    if not pending:
        console.print("\n[yellow]No pending appointments to accept.[/yellow]")
        return
    for i, a in enumerate(pending, start=1):
        console.print(f"[{i}] {a.patient_username} - {a.when.strftime('%Y-%m-%d %H:%M')} - {a.reason}")
    index = IntPrompt.ask(
        "Select appointment number to accept",
        choices=[str(i) for i in range(1, len(pending) + 1)],
    )
    selected = pending[index - 1]
    if appt_mgr.update_status(selected.id, "confirmed"):
        console.print(f"\n[bold green]Appointment with {selected.patient_username} confirmed.[/bold green]")
    else:
        console.print("\n[bold red]Failed to update appointment.[/bold red]")


def admin_dashboard():
    while True:
        console.print("\n[bold cyan]--- Admin Dashboard ---[/bold cyan]")
        console.print("[1] Register Patient")
        console.print("[2] Register Doctor")
        console.print("[3] Register Admin")
        console.print("[4] List All Patients")
        console.print("[5] List All Appointments")
        console.print("[6] Assign Patient to Doctor")
        console.print("[7] Logout")

        choice = IntPrompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"])

        if choice == 1:
            register_patient_ui()
        elif choice == 2:
            register_doctor_ui()
        elif choice == 3:
            register_admin_ui()
        elif choice == 4:
            list_patients_ui()
        elif choice == 5:
            list_appointments_ui()
        elif choice == 6:
            assign_patient_to_doctor_ui()
        elif choice == 7:
            console.print("\n[bold green]Logged out.[/bold green]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


def assign_patient_to_doctor_ui():
    console.print("\n[bold cyan]--- Assign Patient to Doctor ---[/bold cyan]")
    patient_username = Prompt.ask("Enter patient username").strip()
    if not patient_mgr.get_patient_by_username(patient_username):
        console.print(f"[bold red]Patient '{patient_username}' not found.[/bold red]")
        return
    doctor_username = Prompt.ask("Enter doctor username").strip()
    if not doctor_mgr.get_doctor_by_id(doctor_username):
        console.print(f"[bold red]Doctor '{doctor_username}' not found.[/bold red]")
        return
    if patient_mgr.assign_doctor(patient_username, doctor_username):
        console.print(f"\n[bold green]Assigned {patient_username} to Dr. {doctor_username}.[/bold green]")
    else:
        console.print("\n[bold red]Failed to assign doctor.[/bold red]")


def main_menu():
    while True:
        display_menu()
        choice = IntPrompt.ask(
            "Select an option",
            choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        )

        if choice == 1:
            login_ui()
        elif choice == 2:
            register_patient_ui()
        elif choice == 3:
            list_patients_ui()
        elif choice == 4:
            search_patient_ui()
        elif choice == 5:
            delete_patient_ui()
        elif choice == 6:
            register_doctor_ui()
        elif choice == 7:
            book_appointment_ui()
        elif choice == 8:
            list_appointments_ui()
        elif choice == 9:
            register_admin_ui()
        elif choice == 10:
            console.print("\n[bold green]Clinic data saved successfully. Goodbye![/bold green]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


if __name__ == "__main__":
    main_menu()