from __future__ import annotations
import hashlib
import os
import secrets
from typing import Optional

from .model import Patient
from .patient_manager import PatientManager


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    if salt is None:
        salt_bytes = os.urandom(16)
    elif isinstance(salt, str):
        salt_bytes = bytes.fromhex(salt)
    else:
        salt_bytes = salt

    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 100000)
    return key.hex(), salt_bytes.hex()


def verify_password(
    stored_password_hash: str, stored_salt: str, password_attempt: str
) -> bool:
    if not stored_salt:
        return False
    attempt_hash, _ = hash_password(password_attempt, salt=stored_salt)
    return secrets.compare_digest(stored_password_hash, attempt_hash)


class Authenticator:

    def __init__(self, patient_manager: PatientManager):
        if patient_manager is None:
            raise ValueError("Authenticator requires a valid PatientManager instance.")
        self.patient_manager = patient_manager

    def register_patient(
        self,
        username: str,
        password: str,
        age: Optional[int] = None,
        contact: Optional[str] = None,
        medical_history: Optional[str] = None,
    ) -> Optional[Patient]:
        if not password or len(password) < 8:
            print("[X] Password must be at least 8 characters long.")
            return None

        password_hash, salt = hash_password(password)

        patient = self.patient_manager.create_patient(
            username=username,
            password_hash=password_hash,
            salt=salt,
            age=age,
            contact=contact,
            medical_history=[medical_history] if medical_history else [],
        )

        if not patient:
            print(f"[X] Patient with username '{username}' already exists.")
            return None

        return patient

    def login(self, username: str, password: str) -> Optional[Patient]:
        patient = self.patient_manager.get_patient_by_username(username)
        if patient is None:
            print("[X] Invalid username or password.")
            return None

        if not verify_password(patient.password_hash, patient.salt, password):
            print("[X] Invalid username or password.")
            return None 
        
        return patient

        return patient