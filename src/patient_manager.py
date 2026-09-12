from model import Patient


class PatientManager:
    """Simple manager for patient records."""

    def __init__(self):
        # Store patients using username as the key.
        self.patients = {}

    def add_patient(self, patient):
        """Add a patient to the system."""
        if patient.username in self.patients:
            return False

        self.patients[patient.username] = patient
        return True

    def create_patient(self, username, password_hash, age=None,
                       contact=None, medical_history=None):
        """Create a new patient and add them to the system."""
        patient = Patient(
            username,
            password_hash,
            age,
            contact,
            medical_history
        )

        if self.add_patient(patient):
            return patient

        return None

    def get_patient(self, username):
        """Find a patient by username."""
        return self.patients.get(username)

    def authenticate(self, username, password_hash):
        """Check if the username and password hash are correct."""
        patient = self.get_patient(username)

        if patient is not None and patient.password_hash == password_hash:
            return patient

        return None

    def update_patient(self, username, contact=None, medical_history=None):
        """Update a patient's contact and medical history."""
        patient = self.get_patient(username)

        if patient is None:
            return False

        if contact is not None:
            patient.contact = contact

        if medical_history is not None:
            patient.medical_history = medical_history

        return True

    def delete_patient(self, username):
        """Remove a patient from the system."""
        if username in self.patients:
            del self.patients[username]
            return True

        return False

    def get_all_patients(self):
        """Return all patients."""
        return list(self.patients.values())

    def to_dict(self):
        """Convert all patients into dictionaries for saving."""
        data = {}

        for username, patient in self.patients.items():
            data[username] = patient.to_dict()

        return data

    @classmethod
    def from_dict(cls, data):
        """Create a PatientManager from saved data."""
        manager = cls()

        for patient_data in data.values():
            patient = Patient.from_dict(patient_data)
            manager.add_patient(patient)

        return manager