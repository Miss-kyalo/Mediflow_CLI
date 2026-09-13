from datetime import datetime
from typing import List, Optional

from .model import Appointment
from .persistence import StorageManager

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

    def create_appointment(
        self,
        doctor_username: str,
        patient_username: str,
        when: datetime,
        reason: str,
    ) -> Optional[Appointment]:
        appointments = self.get_all_appointments()

        for appt in appointments:
            if (
                appt.doctor_username == doctor_username
                and appt.when == when
                and appt.status in {"pending", "confirmed"}
            ):
                print(f"[X] Conflict: Doctor is already booked for {when}.")
                return None

        new_appt = Appointment(
            doctor_username=doctor_username,
            patient_username=patient_username,
            when=when,
            reason=reason,
        )

        appts_data = self._get_appointments_data()
        appts_data[str(new_appt.id)] = new_appt.to_dict()
        self._save_appointments_data(appts_data)
        return new_appt

    def get_all_appointments(self) -> List[Appointment]:
        appts_data = self._get_appointments_data()
        return [Appointment.from_dict(data) for data in appts_data.values()]

    def get_appointments_by_doctor(self, doctor_id: str) -> List[Appointment]:
        return [
            appt
            for appt in self.get_all_appointments()
            if appt.doctor_username == doctor_id
        ]

    def update_status(self, appt_id: str, new_status: str) -> bool:
        appts_data = self._get_appointments_data()
        key = str(appt_id)
        if key in appts_data:
            appts_data[key]["status"] = new_status.lower()
            self._save_appointments_data(appts_data)
            return True
        return False