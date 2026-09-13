from unittest.mock import MagicMock
import pytest

from src.model import Patient
from src.patient_manager import PatientManager
from src.persistence import StorageManager


@pytest.fixture
def mock_storage():
    storage = MagicMock(spec=StorageManager)
    storage.load_data.return_value = {"patients": {}}
    return storage


@pytest.fixture
def sample_patient():
    return Patient(
        username="john",
        password_hash="e3b0c442fba495991b7852b855",
        salt="a1b2c3d4e5f67890",
        age=25,
        contact="0712345678",
        medical_history=[],
    )


@pytest.fixture
def patient_manager(mock_storage, sample_patient):
    mock_storage.load_data.return_value = {
        "patients": {
            sample_patient.username: sample_patient.to_dict()
        }
    }
    return PatientManager(user_storage=mock_storage)


def test_get_patient_by_username_success(patient_manager):
    patient = patient_manager.get_patient_by_username("john")

    assert patient is not None
    assert patient.username == "john"
    assert patient.age == 25


def test_get_patient_by_username_not_found(patient_manager):
    patient = patient_manager.get_patient_by_username("mary")

    assert patient is None


def test_add_patient_success(mock_storage):
    manager = PatientManager(user_storage=mock_storage)
    new_patient = Patient(
        username="mary",
        password_hash="hash456",
        salt="salt456",
        age=30
    )

    result = manager.add_patient(new_patient)

    assert result is True
    assert mock_storage.save_data.called


def test_add_duplicate_patient_fails(patient_manager, sample_patient):
    duplicate_patient = Patient(
        username="john",
        password_hash="another_hash",
        salt="another_salt",
        age=40
    )

    result = patient_manager.add_patient(duplicate_patient)

    assert result is False


def test_update_patient_success(patient_manager, mock_storage):
    result = patient_manager.update_patient(
        username="john",
        contact="0799999999",
        new_medical_entry="Routine Checkup"
    )

    assert result is True
    assert mock_storage.save_data.called


def test_delete_patient_success(patient_manager, mock_storage):
    result = patient_manager.delete_patient("john")

    assert result is True
    assert mock_storage.save_data.called


def test_delete_unknown_patient_fails(patient_manager):
    result = patient_manager.delete_patient("nonexistent_user")

    assert result is False