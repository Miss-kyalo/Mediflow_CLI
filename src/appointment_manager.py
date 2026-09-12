from typing import List, Optional
from model import Appointment
from src.persistence import StorageManager

class AppointmentManager:
       
    def __init__(self, clinic_storage: StorageManager):
        self.storage = clinic_storage

    def _get_appointments_data(self) -> dict:
        clinic_data = self.storage.load_data()
        return clinic_data.get("appointments", {})

    def _save_appointments_data(self, appointments_data: dict) -> None:
        clinic_data = self.storage.load_data()
        clinic_data["appointments"] = appointments_data
        self.storage.save_data(clinic_data)

    def create_appointment(self, doctor_id: str, patient_id: str, date: str, time_slot: str) -> Optional[Appointment]:
        appointments = self.get_all_appointments()

        for appt in appointments:
            if appt.doctor_id == doctor_id and appt.date == date and appt.time_slot == time_slot and appt.status == "Scheduled":
                print(f"[X] Conflict: Doctor is already booked for {time_slot} on {date}.")
                return None

        new_appt = Appointment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            time_slot=time_slot,
            date=date
        )

        appts_data = self._get_appointments_data()
        appts_data[new_appt.appt_id] = new_appt.to_dict()
        self._save_appointments_data(appts_data)
        return new_appt

    def get_all_appointments(self) -> List[Appointment]:
        appts_data = self._get_appointments_data()
        return [Appointment.from_dict(data) for data in appts_data.values()]

    def get_appointments_by_doctor(self, doctor_id: str) -> List[Appointment]:
        return [appt for appt in self.get_all_appointments() if appt.doctor_id == doctor_id]

    def update_status(self, appt_id: str, new_status: str) -> bool:
        appts_data = self._get_appointments_data()
        if appt_id in appts_data:
            appts_data[appt_id]["status"] = new_status
            self._save_appointments_data(appts_data)
            return True
        return False