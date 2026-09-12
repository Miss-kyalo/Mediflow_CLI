import hashlib

from model import Patient
from patient_manager import PatientManager

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class Authenticator:

    def __init__(self, patient_manager=None):
        self.patient_manager = patient_manager

    def register_patient(self, username, password, age=None, contact=None, medical_history=None):
        password_hash = hash_password(password)
        patient = Patient(username, password_hash, age, contact)

        added = self.patient_manager.add_patient(patient)
        if not added:
            print(f"Patient with username '{username}' already exists.")
            return None
        
        return patient

    def login(self, username, password):
        password_hash = hash_password(password)
        patient = self.patient_manager.authenticate(username, password_hash)

        if patient is None:
            print("Invalid username or password.")
            return None
        
        return patient
