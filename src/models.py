from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class DoctorUser:
    doctor_id: str
    specialty: str
    availability: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "DoctorUser":
        return cls(
            doctor_id=data.get("doctor_id", data.get("id", "")),
            specialty=data.get("specialty", ""),
            availability=list(data.get("availability", [])),
        )


@dataclass
class Appointment:
    doctor_id: str
    patient_id: str
    time_slot: str
    date: str
    status: str = "Scheduled"
    appt_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict:
        return {
            "appt_id": self.appt_id,
            "doctor_id": self.doctor_id,
            "patient_id": self.patient_id,
            "time_slot": self.time_slot,
            "date": self.date,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Appointment":
        return cls(
            appt_id=data["appt_id"],
            doctor_id=data["doctor_id"],
            patient_id=data["patient_id"],
            time_slot=data["time_slot"],
            date=data["date"],
            status=data.get("status", "Scheduled"),
        )
