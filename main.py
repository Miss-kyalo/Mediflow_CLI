import hashlib
import sys
from pathlib import Path

# Ensure 'src' is in the module search path
sys.path.append(str(Path(__file__).parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from patient_manager import PatientManager
from persistence import StorageManager

console = Console()
storage = StorageManager()


def hash_password(password: str) -> str:
    """Hash password using SHA-256 for basic authentication."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def display_header():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]🏥 MEDIFLOW CLINIC MANAGEMENT SYSTEM[/bold cyan]\n"
            "[dim]Interactive Command-Line Application[/dim]",
            border_style="cyan",
        )
    )


def main_menu():
    patient_mgr = PatientManager()

    # Load stored state on startup
    raw_data = storage.load_data()
    if "patients" in raw_data:
        patient_mgr = PatientManager.from_dict(raw_data["patients"])

    while True:
        display_header()
        console.print("[1] 👤 Register Patient", style="bold green")
        console.print("[2] 📋 List All Patients", style="bold blue")
        console.print("[3] 🔍 Search Patient Record", style="bold yellow")
        console.print("[4] ❌ Delete Patient", style="bold red")
        console.print("[5] 💾 Save & Exit", style="bold white")

        choice = Prompt.ask(
            "\nSelect an option", choices=["1", "2", "3", "4", "5"], default="5"
        )

        if choice == "1":
            username = Prompt.ask("Enter patient username")
            password = Prompt.ask("Enter password", password=True)
            age = IntPrompt.ask("Enter age")
            contact = Prompt.ask("Enter contact number")

            pw_hash = hash_password(password)
            patient = patient_mgr.create_patient(username, pw_hash, age, contact)

            if patient:
                console.print(
                    f"\n[bold green]✓ Patient '{username}' registered successfully![/bold green]"
                )
            else:
                console.print(
                    f"\n[bold red]✗ Patient '{username}' already exists.[/bold red]"
                )
            Prompt.ask("\nPress Enter to continue...")

        elif choice == "2":
            patients = patient_mgr.get_all_patients()
            if not patients:
                console.print("\n[yellow]No patients registered yet.[/yellow]")
            else:
                table = Table(
                    title="Registered Patients", header_style="bold magenta"
                )
                table.add_column("Username", style="cyan")
                table.add_column("Age", style="green")
                table.add_column("Contact", style="yellow")

                for p in patients:
                    table.add_row(
                        p.username, str(p.age or "N/A"), p.contact or "N/A"
                    )

                console.print("\n", table)
            Prompt.ask("\nPress Enter to continue...")

        elif choice == "3":
            username = Prompt.ask("Enter username to search")
            patient = patient_mgr.get_patient(username)
            if patient:
                console.print(
                    f"\n[bold cyan]Patient Found:[/bold cyan] {patient.username}"
                )
                console.print(f"Age: {patient.age}")
                console.print(f"Contact: {patient.contact}")
                console.print(f"Medical History: {patient.medical_history}")
            else:
                console.print(
                    f"\n[bold red]Patient '{username}' not found.[/bold red]"
                )
            Prompt.ask("\nPress Enter to continue...")

        elif choice == "4":
            username = Prompt.ask("Enter username to delete")
            if patient_mgr.delete_patient(username):
                console.print(
                    f"\n[bold green]✓ Patient '{username}' deleted.[/bold green]"
                )
            else:
                console.print(
                    f"\n[bold red]Patient '{username}' not found.[/bold red]"
                )
            Prompt.ask("\nPress Enter to continue...")

        elif choice == "5":
            saved = storage.save_data({"patients": patient_mgr.to_dict()})
            if saved:
                console.print(
                    "\n[bold green]✓ Clinic data saved successfully. Goodbye![/bold green]"
                )
            else:
                console.print("\n[bold red]✗ Failed to save data on exit.[/bold red]")
            break


if __name__ == "__main__":
    main_menu()