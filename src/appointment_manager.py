from datetime import datetime
from typing import List, Optional

from .model import Appointment
from .persistence import StorageManager


class AppointmentManager:

    def __init__(self, clinic_storage: StorageManager):
        self.storage = clinic_storage

    def _get_appointments_dict(self) -> dict:
        clinic_data = self.storage.load_data()
        return clinic_data.get("appointments", {})

    def get_all_appointments(self) -> List[Appointment]:
        appts_data = self._get_appointments_dict()
        return [Appointment.from_dict(data) for data in appts_data.values()]

    def create_appointment(
        self,
        doctor_username: str,
        patient_username: str,
        when: datetime,
        reason: str,
    ) -> Optional[Appointment]:
        clinic_data = self.storage.load_data()
        appts_dict = clinic_data.setdefault("appointments", {})

        for raw_appt in appts_dict.values():
            if (
                raw_appt.get("status") in {"pending", "confirmed"}
                and raw_appt.get("when") == when.isoformat()
            ):
                if raw_appt.get("doctor_username") == doctor_username:
                    print(
                        f"[X] Conflict: Doctor {doctor_username} is already booked for {when}."
                    )
                    return None
                if raw_appt.get("patient_username") == patient_username:
                    print(
                        f"[X] Conflict: Patient {patient_username} already has an appointment at {when}."
                    )
                    return None

        new_appt = Appointment(
            doctor_username=doctor_username,
            patient_username=patient_username,
            when=when,
            reason=reason,
        )

        appts_dict[str(new_appt.id)] = new_appt.to_dict()
        self.storage.save_data(clinic_data)
        return new_appt

    def get_appointments_by_doctor(self, doctor_username: str) -> List[Appointment]:
        return [
            appt
            for appt in self.get_all_appointments()
            if appt.doctor_username == doctor_username
        ]

    def update_status(self, appt_id: str, new_status: str) -> bool:
        clinic_data = self.storage.load_data()
        appts_dict = clinic_data.get("appointments", {})
        key = str(appt_id)

        if key in appts_dict:
            appts_dict[key]["status"] = new_status.lower()
            self.storage.save_data(clinic_data)
            return True

        return False