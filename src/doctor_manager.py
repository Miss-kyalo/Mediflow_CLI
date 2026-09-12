from typing import List, Optional
from src.models import DoctorUser
from src.persistence import StorageManager


class DoctorManager:

    def __init__(
        self, 
        user_storage: StorageManager
    ):
        self.storage = user_storage

    def get_all_doctors(self) -> List[DoctorUser]:
        users = self.storage.load_data()
        doctors = []
        for user_data in users.values():
            if user_data.get("role") == "Doctor":
                doctors.append(DoctorUser.from_dict(user_data))
        return doctors

    def get_doctor_by_id(
        self, 
        doctor_id: str
    ) -> Optional[DoctorUser]:
        users = self.storage.load_data()
        user_data = users.get(doctor_id)
        if user_data and user_data.get("role") == "Doctor":
            return DoctorUser.from_dict(user_data)
        return None

    def get_doctors_by_specialty(
        self, 
        specialty: str
    ) -> List[DoctorUser]:
        all_doctors = self.get_all_doctors()
        return [
            doc for doc in all_doctors 
            if doc.specialty.lower() == specialty.lower()
        ]

    def update_availability(
        self, 
        doctor_id: str, 
        new_slots: List[str]
    ) -> bool:
        users = self.storage.load_data()
        if doctor_id in users and users[doctor_id].get("role") == "Doctor":
            users[doctor_id]["availability"] = new_slots
            self.storage.save_data(users)
            return True
        return False

    def add_availability_slot(
        self, 
        doctor_id: str, 
        time_slot: str
    ) -> bool:
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            if time_slot not in doctor.availability:
                doctor.availability.append(time_slot)
                return self.update_availability(doctor_id, doctor.availability)
        return False

    def remove_availability_slot(
        self, 
        doctor_id: str, 
        time_slot: str
    ) -> bool:
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor and time_slot in doctor.availability:
            doctor.availability.remove(time_slot)
            return self.update_availability(doctor_id, doctor.availability)
        return False