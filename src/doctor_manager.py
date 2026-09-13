from typing import List, Optional

from .model import Doctor
from .persistence import StorageManager


class DoctorManager:

    def __init__(self, user_storage: StorageManager):
        self.storage = user_storage

    def _get_doctors_dict(self) -> dict:
        clinic_data = self.storage.load_data()
        return clinic_data.get("doctors", {})

    def get_all_doctors(self) -> List[Doctor]:
        doctors_data = self._get_doctors_dict()
        return [Doctor.from_dict(data) for data in doctors_data.values()]

    def get_doctor_by_id(self, doctor_id: str) -> Optional[Doctor]:
        user_data = self._get_doctors_dict().get(str(doctor_id))
        return Doctor.from_dict(user_data) if user_data else None

    def get_doctors_by_specialty(self, specialty: str) -> List[Doctor]:
        target_specialty = specialty.strip().lower()
        return [
            doc
            for doc in self.get_all_doctors()
            if getattr(doc, "specialization", "").lower() == target_specialty
        ]

    def update_availability(self, doctor_id: str, new_slots: List[str]) -> bool:
        clinic_data = self.storage.load_data()
        doctors_dict = clinic_data.get("doctors", {})
        key = str(doctor_id)

        if key in doctors_dict:
            doctors_dict[key]["available_days"] = new_slots
            self.storage.save_data(clinic_data)
            return True

        return False

    def add_availability_slot(self, doctor_id: str, time_slot: str) -> bool:
        clinic_data = self.storage.load_data()
        doctors_dict = clinic_data.get("doctors", {})
        key = str(doctor_id)

        if key in doctors_dict:
            slots = doctors_dict[key].setdefault("available_days", [])
            if time_slot not in slots:
                slots.append(time_slot)
                self.storage.save_data(clinic_data)
                return True

        return False

    def remove_availability_slot(self, doctor_id: str, time_slot: str) -> bool:
        clinic_data = self.storage.load_data()
        doctors_dict = clinic_data.get("doctors", {})
        key = str(doctor_id)

        if key in doctors_dict:
            slots = doctors_dict[key].get("available_days", [])
            if time_slot in slots:
                slots.remove(time_slot)
                self.storage.save_data(clinic_data)
                return True

        return False