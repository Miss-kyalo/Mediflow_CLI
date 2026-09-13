from datetime import datetime


next_appointment = 1

class User:

    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role  # 'patient' or 'doctor'   

    def get_password_hash(self):
        return self.password_hash

    def set_password_hash(self, new_hash):
        self.password_hash = new_hash

    def to_dict(self):
        #turns this object into a plain dictionary so it can be saved to a JSON file
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role
        }

    def __str__(self):
        return f"User(username={self.username}, role={self.role})"

class Patient(User):
    def __init__(self, username, password_hash, age=None, contact=None, medical_history=None):
        super().__init__(username, password_hash, role='patient')
        self.age = age
        self.contact = contact
        self.medical_history = medical_history or []

    def add_medical_history(self, entry):
        if self.medical_history is None:
            self.medical_history = []
        self.medical_history.append(entry)

    def get_medical_history(self):
        return self.medical_history

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'age': self.age,
            'contact': self.contact,
            'medical_history': self.medical_history
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            password_hash=data['password_hash'],
            age=data.get('age'),
            contact=data.get('contact'),
            medical_history=data.get('medical_history')
        )

class Doctor(User):

    def __init__(self, username, password_hash, specialization="General", available_days=None):
        super().__init__(username, password_hash, role='doctor')
        self.specialization = specialization
        self.available_days = available_days or []

    def is_available_on_day(self, day_name):
        return day_name in self.available_days

    def to_dict(self):
        data = super().to_dict()
        data["specialization"] = self.specialization
        data["available_days"] = self.available_days
        return data
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['username'],
            data['password_hash'],
            data.get('specialization', "General"),
            data.get('available_days')
        )

class Admin(User):

    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, role='admin')

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['username'],
            data['password_hash']
        )

class Appointment:
    def __init__(self, patient_username, doctor_username, when, reason, status="pending", appt_id=None):
        global next_appointment

        if appt_id is not None:
            self.id = appt_id
            next_appointment = max(next_appointment, int(appt_id) + 1)
        else:
            self.id = next_appointment
            next_appointment += 1

        self.patient_username = patient_username
        self.doctor_username = doctor_username
        self.when = when  # datetime object
        self.reason = reason
        self.status = status  # 'pending', 'confirmed', 'completed', 'cancelled'

    def confirm(self):
        self.status = "confirmed"

    def cancel(self):
        self.status = "cancelled"

    def complete(self):
        self.status = "completed"

    def to_dict(self):
        return {
            'id': self.id,
            'patient_username': self.patient_username,
            'doctor_username': self.doctor_username,
            'when': self.when.isoformat(),
            'reason': self.reason,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            patient_username=data['patient_username'],
            doctor_username=data['doctor_username'],
            when=datetime.fromisoformat(data['when']),
            reason=data['reason'],
            status=data.get('status', 'pending'),
            appt_id=data.get('id')
        )

    