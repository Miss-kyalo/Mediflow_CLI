from typing import List, Optional

from .model import Patient
from .persistence import StorageManager


class PatientManager:

    def __init__(self, user_storage: StorageManager):
        self.storage = user_storage

    def _get_patients_dict(self) -> dict:
        clinic_data = self.storage.load_data()
        return clinic_data.get("patients", {})

    def get_all_patients(self) -> List[Patient]:
        patients_data = self._get_patients_dict()
        return [Patient.from_dict(data) for data in patients_data.values()]

    def get_patient_by_username(self, username: str) -> Optional[Patient]:
        patient_data = self._get_patients_dict().get(username)
        return Patient.from_dict(patient_data) if patient_data else None

    def add_patient(self, patient: Patient) -> bool:
        clinic_data = self.storage.load_data()
        patients_dict = clinic_data.setdefault("patients", {})

        if patient.username in patients_dict:
            return False

        patients_dict[patient.username] = patient.to_dict()
        self.storage.save_data(clinic_data)
        return True

    def create_patient(
        self,
        username: str,
        password_hash: str,
        salt: str = "",
        age: Optional[int] = None,
        contact: Optional[str] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Optional[Patient]:
        patient = Patient(
            username=username,
            password_hash=password_hash,
            salt=salt,
            age=age,
            contact=contact,
            medical_history=medical_history,
        )

        if self.add_patient(patient):
            return patient

        return None

    def update_patient(
        self,
        username: str,
        contact: Optional[str] = None,
        new_medical_entry: Optional[str] = None,
    ) -> bool:
        clinic_data = self.storage.load_data()
        patients_dict = clinic_data.get("patients", {})

        if username not in patients_dict:
            return False

        patient_data = patients_dict[username]

        if contact is not None:
            patient_data["contact"] = contact

        if new_medical_entry is not None:
            history = patient_data.setdefault("medical_history", [])
            history.append(new_medical_entry)

        self.storage.save_data(clinic_data)
        return True

    def delete_patient(self, username: str) -> bool:
        clinic_data = self.storage.load_data()
        patients_dict = clinic_data.get("patients", {})

        if username in patients_dict:
            del patients_dict[username]
            self.storage.save_data(clinic_data)
            return True

        return False