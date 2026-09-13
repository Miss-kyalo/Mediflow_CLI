
**MediFlow Clinic Management System**
MediFlow is an interactive command-line application built with Python and Rich to manage clinic records, including patients, doctors, and appointments with local JSON file persistence.

**Features**
Patient Management: Register, search, list, update, and delete patient records.

Doctor Management: Track doctor profiles, specializations, and daily availability.

Appointment Scheduling: Book and track appointments without double-booking conflicts.

Secure Authentication: Password hashing using PBKDF2-HMAC-SHA256 with unique salts.

Persistent Storage: Atomic JSON reads and writes with automatic backup generation.


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

# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

