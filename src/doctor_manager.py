from typing import List, Optional

from .model import Doctor
from .persistence import StorageManager


class DoctorManager:

    def __init__(
        self,
        user_storage: StorageManager,
    ):
        self.storage = user_storage

    def _get_doctors_data(self) -> dict:
        return self.storage.load_data().get("doctors", {})

    def _save_doctors_data(self, doctors_data: dict) -> None:
        clinic_data = self.storage.load_data()
        clinic_data["doctors"] = doctors_data
        self.storage.save_data(clinic_data)

    def get_all_doctors(self) -> List[Doctor]:
        return [Doctor.from_dict(data) for data in self._get_doctors_data().values()]

    def get_doctor_by_id(
        self,
        doctor_id: str,
    ) -> Optional[Doctor]:
        user_data = self._get_doctors_data().get(doctor_id)
        return Doctor.from_dict(user_data) if user_data else None

    def get_doctors_by_specialty(
        self,
        specialty: str,
    ) -> List[Doctor]:
        all_doctors = self.get_all_doctors()
        return [
            doc for doc in all_doctors 
            if doc.specialization.lower() == specialty.lower()
        ]

    def update_availability(
        self,
        doctor_id: str,
        new_slots: List[str],
    ) -> bool:
        doctors = self._get_doctors_data()
        if doctor_id in doctors:
            doctors[doctor_id]["available_days"] = new_slots
            self._save_doctors_data(doctors)
            return True
        return False

    def add_availability_slot(
        self,
        doctor_id: str,
        time_slot: str,
    ) -> bool:
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            if time_slot not in doctor.available_days:
                doctor.available_days.append(time_slot)
                return self.update_availability(doctor_id, doctor.available_days)
        return False

    def remove_availability_slot(
        self,
        doctor_id: str,
        time_slot: str,
    ) -> bool:
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor and time_slot in doctor.available_days:
            doctor.available_days.remove(time_slot)
            return self.update_availability(doctor_id, doctor.available_days)
        return False