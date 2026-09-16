
**MEDIFLOW**
Mediflow is a modular Python command-line application built to manage clinic workflows, including patient onboarding, doctor availability tracking, and appointment scheduling. It features atomic JSON data persistence, multi-role authentication, and conflict-free booking logic.

**Key Features**
Multi-Role Authentication: Built with standard security best practices (Patient, Doctor, Admin) utilizing PBKDF2-HMAC-SHA256 password hashing with dynamic salt generation and constant-time string comparison (secrets.compare_digest).

Patient Management: Account registration, profile updates (contact info, age), medical history tracking, and keyword-based medical condition searches.

Doctor & Schedule Management: Specialty-based doctor lookup and customizable availability slots (available_days).

Conflict-Aware Scheduling: Prevents double-booking by enforcing doctor schedule availability and preventing overlapping patient appointments. Tracks status across standard lifecycles (pending, confirmed, completed, cancelled).

Atomic JSON Persistence: Built-in StorageManager leverages atomic writes via temporary (.tmp) files and backup (.bak) fallback logic to prevent database corruption during unexpected crashes.

Input Validation & Utilities: Input sanitization, human age bounds verification, phone number regex validation, and standardized datetime parsing (YYYY-MM-DD HH:MM).


**Project Structure**

├── src/
│   ├── appointment_manager.py
│   ├── auth.py
│   ├── doctor_manager.py
│   ├── model.py
│   ├── patient_manager.py
│   ├── persistence.py
│   └── utility.py
├── main.py
├── test.py
└── requirements.txt

**PROJECT CONTRIBUTIONS:**
appointment_manager.py -lynn
auth.py-margret
doctor_manager.py-lynn
model.py-margret
patient_manager.py-mohammed siraj
persistence.py-Abdulmajid
utility.py-margret
test_auth.py-mohammed siraj
main.py-Abdulmajid
Readme.md-lynn

# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.
