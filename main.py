from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

# Import project modules
from src.patient_manager import PatientManager
from src.persistence import StorageManager
from src.auth import hash_password
from src.utility import clear_screen, validate_age, validate_phone

console = Console()
storage = StorageManager()

# Load existing data from file using StorageManager
initial_data = storage.load_data()
if initial_data and "patients" in initial_data:
    patient_mgr = PatientManager.from_dict(initial_data["patients"])
else:
    patient_mgr = PatientManager()


def display_menu():
    """Display the main system menu using Rich formatting."""
    clear_screen()
    console.print(
        Panel.fit(
            "[bold cyan]🏥 MEDIFLOW CLINIC MANAGEMENT SYSTEM[/bold cyan]\n"
            "[dim]Interactive Command-Line Application[/dim]",
            border_style="cyan",
        )
    )
    console.print("[1] 👤 Register Patient")
    console.print("[2] 📋 List All Patients")
    console.print("[3] 🔍 Search Patient Record")
    console.print("[4] ❌ Delete Patient")
    console.print("[5] 💾 Save & Exit\n")


def register_patient_ui():
    """Interactive screen to register a new patient with input validation."""
    console.print("\n[bold cyan]--- Register New Patient ---[/bold cyan]")
    username = Prompt.ask("Enter patient username").strip()
    if not username:
        console.print("[bold red]Username cannot be empty![/bold red]")
        return

    password = Prompt.ask("Enter password", password=True)
    age = IntPrompt.ask("Enter age")
    while not validate_age(str(age)):
        console.print("[bold red]Age must be between 1 and 120.[/bold red]")
        age = IntPrompt.ask("Enter age")

    contact = Prompt.ask("Enter contact number")
    while not validate_phone(contact):
        console.print(
            "[bold red]Invalid phone format. Please enter a valid number (e.g., 0712345678 or +254...).[/bold red]"
        )
        contact = Prompt.ask("Enter contact number")

    # Uses create_patient from PatientManager
    patient = patient_mgr.create_patient(
        username=username,
        password_hash=hash_password(password),
        age=age,
        contact=contact,
    )
    if patient:
        console.print(
            f"\n[bold green]✓ Patient '{username}' registered successfully![/bold green]"
        )
    else:
        console.print(
            f"\n[bold red]✗ Registration failed. Username '{username}' already exists.[/bold red]"
        )


def list_patients_ui():
    """Display all registered patients in a styled table."""
    # Uses get_all_patients from PatientManager
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
        table.add_row(p.username, str(p.age), getattr(p, "contact", "N/A"), getattr(p, "role", "patient"))

    console.print("\n")
    console.print(table)


def search_patient_ui():
    """Search and display a single patient's details."""
    username = Prompt.ask("\nEnter username to search").strip()
    patient = patient_mgr.get_patient(username)

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
            f"\n[bold red]✗ Patient '{username}' not found.[/bold red]"
        )


def delete_patient_ui():
    """Remove a patient from the system."""
    username = Prompt.ask("\nEnter username to delete").strip()
    if patient_mgr.delete_patient(username):
        console.print(
            f"\n[bold green]✓ Patient '{username}' removed successfully.[/bold green]"
        )
    else:
        console.print(
            f"\n[bold red]✗ Patient '{username}' not found.[/bold red]"
        )


def main_menu():
    """Main application control loop."""
    while True:
        display_menu()
        choice = IntPrompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])

        if choice == 1:
            register_patient_ui()
        elif choice == 2:
            list_patients_ui()
        elif choice == 3:
            search_patient_ui()
        elif choice == 4:
            delete_patient_ui()
        elif choice == 5:
            # Export patient dict and save via StorageManager
            data_to_save = {"patients": patient_mgr.to_dict()}
            if storage.save_data(data_to_save):
                console.print(
                    "\n[bold green]✓ Clinic data saved successfully. Goodbye![/bold green]"
                )
            else:
                console.print("\n[bold red]✗ Failed to save clinic data.[/bold red]")
            break

        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")


if __name__ == "__main__":
    main_menu()