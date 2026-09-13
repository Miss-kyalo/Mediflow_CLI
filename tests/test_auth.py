import pytest

from src.model import Patient
from src.patient_manager import PatientManager


def create_manager():
    """Create a manager with one test patient."""
    manager = PatientManager()

    patient = Patient(
        "john",
        "password_hash_123",
        25,
        "0712345678",
        []
    )

    manager.add_patient(patient)

    return manager


def test_correct_login():
    manager = create_manager()

    patient = manager.authenticate("john", "password_hash_123")

    assert patient is not None
    assert patient.username == "john"


def test_wrong_password():
    manager = create_manager()

    patient = manager.authenticate("john", "wrong_password")

    assert patient is None


def test_unknown_username():
    manager = create_manager()

    patient = manager.authenticate("mary", "password_hash_123")

    assert patient is None


def test_add_patient():
    manager = PatientManager()

    patient = Patient(
        "mary",
        "hash456",
        30
    )

    result = manager.add_patient(patient)

    assert result is True
    assert manager.get_patient("mary") == patient


def test_duplicate_patient():
    manager = create_manager()

    patient = Patient(
        "john",
        "another_hash",
        40
    )

    result = manager.add_patient(patient)

    assert result is False


def test_delete_patient():
    manager = create_manager()

    result = manager.delete_patient("john")

    assert result is True
    assert manager.get_patient("john") is None