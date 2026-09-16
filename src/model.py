from __future__ import annotations
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class User:

    def __init__(self, username: str, password_hash: str, salt: str, role: str):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.role = role

    def get_password_hash(self) -> str:
        return self.password_hash

    def set_password_hash(self, new_hash: str) -> None:
        self.password_hash = new_hash

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "role": self.role,
        }

    def __str__(self) -> str:
        return f"User(username={self.username}, role={self.role})"


class Patient(User):

    def __init__(
        self,
        username: str,
        password_hash: str,
        salt: str = "",
        age: Optional[int] = None,
        contact: Optional[str] = None,
        medical_history: Optional[List[str]] = None,
        assigned_doctor: Optional[str] = None,
    ):
        super().__init__(username, password_hash, salt, role="patient")
        self.age = age
        self.contact = contact
        self.medical_history = medical_history if medical_history is not None else []
        self.assigned_doctor = assigned_doctor

    def add_medical_history(self, entry: str) -> None:
        self.medical_history.append(entry)

    def get_medical_history(self) -> List[str]:
        return self.medical_history

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "age": self.age,
                "contact": self.contact,
                "medical_history": self.medical_history,
                "assigned_doctor": self.assigned_doctor,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Patient":
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            salt=data.get("salt", ""),
            age=data.get("age"),
            contact=data.get("contact"),
            medical_history=data.get("medical_history"),
            assigned_doctor=data.get("assigned_doctor"),
        )


class Doctor(User):

    def __init__(
        self,
        username: str,
        password_hash: str,
        salt: str = "",
        specialization: str = "General",
        available_days: Optional[List[str]] = None,
    ):
        super().__init__(username, password_hash, salt, role="doctor")
        self.specialization = specialization
        self.available_days = available_days if available_days is not None else []

    def is_available_on_day(self, day_name: str) -> bool:
        return day_name.lower() in [day.lower() for day in self.available_days]

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update(
            {
                "specialization": self.specialization,
                "available_days": self.available_days,
            }
        )
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Doctor":
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            salt=data.get("salt", ""),
            specialization=data.get("specialization", "General"),
            available_days=data.get("available_days"),
        )


class Admin(User):

    def __init__(self, username: str, password_hash: str, salt: str = ""):
        super().__init__(username, password_hash, salt, role="admin")

    @classmethod
    def from_dict(cls, data: dict) -> "Admin":
        return cls(
            username=data["username"],
            password_hash=data["password_hash"],
            salt=data.get("salt", ""),
        )


class Appointment:

    def __init__(
        self,
        patient_username: str,
        doctor_username: str,
        when: datetime,
        reason: str,
        status: AppointmentStatus | str = AppointmentStatus.PENDING,
        appt_id: Optional[str] = None,
    ):
        self.id = appt_id if appt_id is not None else str(uuid.uuid4())
        self.patient_username = patient_username
        self.doctor_username = doctor_username
        self.when = when
        self.reason = reason
        self.status = (
            AppointmentStatus(status) if isinstance(status, str) else status
        )

    def confirm(self) -> None:
        self.status = AppointmentStatus.CONFIRMED

    def cancel(self) -> None:
        self.status = AppointmentStatus.CANCELLED

    def complete(self) -> None:
        self.status = AppointmentStatus.COMPLETED

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patient_username": self.patient_username,
            "doctor_username": self.doctor_username,
            "when": self.when.isoformat(),
            "reason": self.reason,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Appointment":
        return cls(
            patient_username=data["patient_username"],
            doctor_username=data["doctor_username"],
            when=datetime.fromisoformat(data["when"]),
            reason=data["reason"],
            status=AppointmentStatus(data.get("status", "pending")),
            appt_id=str(data["id"]) if "id" in data else None,
        )

if __name__ == "__main__":
    print("=== Testing Patient ===")
    patient = Patient("john_doe", "hashedpw123", age=30, contact="0712345678")
    patient.add_medical_history("Allergic to penicillin")
    print(patient)
    print(patient.to_dict())
    patient2 = Patient.from_dict(patient.to_dict())
    print(patient2)

    print("\n=== Testing Doctor ===")
    doctor = Doctor("dr_smith", "hashedpw456", specialization="Cardiology",
                     available_days=["Monday", "Wednesday", "Friday"])
    print(doctor)
    print(doctor.is_available_on_day("Monday"))
    print(doctor.to_dict())
    doctor2 = Doctor.from_dict(doctor.to_dict())
    print(doctor2)

    print("\n=== Testing Admin ===")
    admin = Admin("admin_jane", "hashedpw789")
    print(admin)
    admin2 = Admin.from_dict(admin.to_dict())
    print(admin2)

    print("\n=== Testing Appointment ===")
    appt = Appointment("john_doe", "dr_smith", datetime.now(), "Routine checkup")
    print(appt.to_dict())
    appt.confirm()
    print("Status after confirm:", appt.status)
    appt.complete()
    print("Status after complete:", appt.status)
    appt2 = Appointment.from_dict(appt.to_dict())
    print(appt2.status)