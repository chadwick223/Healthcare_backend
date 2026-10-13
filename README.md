# Healthcare Backend API

A secure, scalable RESTful backend for a healthcare management system built with **Django**, **Django REST Framework (DRF)**, **PostgreSQL (Neon)**, and **JWT authentication** (`djangorestframework-simplejwt`).

This application allows users to register, authenticate securely, manage patient and doctor records, and assign multiple doctors to patients while enforcing strict ownership and relational constraints.

---

## Table of Contents
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Authentication Flow](#authentication-flow)
- [API Reference](#api-reference)
  - [1. Authentication APIs](#1-authentication-apis)
  - [2. Patient Management APIs](#2-patient-management-apis)
  - [3. Doctor Management APIs](#3-doctor-management-apis)
  - [4. Patient-Doctor Mapping APIs](#4-patient-doctor-mapping-apis)
- [Data Seeding via Django ORM](#data-seeding-via-django-orm)
- [Error Handling & Validation](#error-handling--validation)

---

## Tech Stack
- **Framework:** Django 5.2 & Django REST Framework (DRF)
- **Database:** PostgreSQL (Neon Serverless PostgreSQL) with local SQLite fallback
- **Authentication:** JSON Web Tokens (JWT) using `djangorestframework-simplejwt`
- **Environment Management:** `python-decouple`
- **Database Engine Connector:** `psycopg2-binary` & `dj-database-url`

---

## Project Architecture

```
Healthcare_backend/
├── Healthcare_backend/       # Project core configuration
│   ├── settings.py           # Settings (Decouple + Neon Postgres + JWT)
│   ├── urls.py               # Root URL router
│   └── wsgi.py
├── core/                     # Application domain logic
│   ├── api/
│   │   ├── serializers.py    # DRF Serializers with custom validators
│   │   ├── urls.py           # API routes for auth, patients, doctors, mappings
│   │   └── views.py          # Class-based views (APIView) with permission checks
│   ├── models.py             # Database models (Patient, Doctor, PatientDoctorMapping)
│   ├── admin.py              # Django admin panel integration
│   └── migrations/           # Database migration files
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── manage.py
```

---

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/chadwick223/Healthcare_backend.git
cd Healthcare_backend
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your configuration in `.env`:
```env
SECRET_KEY=your-secure-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*
DATABASE_URL=postgresql://<user>:<password>@<neon-host>/<dbname>?sslmode=require
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Development Server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django cryptographic secret key | `django-insecure-your-key` |
| `DEBUG` | Enable/disable debug mode (`True` or `False`) | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames | `localhost,127.0.0.1,*` |
| `DATABASE_URL` | PostgreSQL connection URL (Neon or local) | `postgresql://user:pass@host/db?sslmode=require` |

---

## Authentication Flow

Protected endpoints require a valid JWT Bearer token in the `Authorization` header:

```http
Authorization: Bearer <your_access_token>
```

1. Register at `POST /api/auth/register/` or log in at `POST /api/auth/login/`.
2. The login response returns an `access` token (valid for 1 hour) and a `refresh` token (valid for 7 days).
3. Include the `access` token in the `Authorization` header for all requests to `/api/patients/`, `/api/doctors/`, and `/api/mappings/`.

---

## API Reference

### 1. Authentication APIs

#### 1.1 Register New User
* **Endpoint:** `POST /api/auth/register/`
* **Access:** Public
* **Request Body:**
```json
{
  "name": "Satvik Shukla",
  "email": "satvik@example.com",
  "password": "Password123"
}
```
* **Success Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "Satvik Shukla",
    "email": "satvik@example.com"
  }
}
```
* **Error Response (400 Bad Request):**
```json
{
  "email": ["A user with this email already exists."]
}
```

---

#### 1.2 User Login
* **Endpoint:** `POST /api/auth/login/`
* **Access:** Public
* **Request Body:**
```json
{
  "email": "satvik@example.com",
  "password": "Password123"
}
```
* **Success Response (200 OK):**
```json
{
  "message": "Login successful",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "name": "Satvik Shukla",
    "email": "satvik@example.com"
  }
}
```
* **Error Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Invalid email or password."]
}
```

---

### 2. Patient Management APIs
*All patient endpoints require authentication.*

#### 2.1 Add New Patient
* **Endpoint:** `POST /api/patients/`
* **Access:** Authenticated
* **Request Body:**
```json
{
  "name": "John Doe",
  "age": 35,
  "gender": "M",
  "phone": "9876543210",
  "address": "123 Baker Street, London",
  "medical_history": "Hypertension, Asthma"
}
```
* **Success Response (201 Created):**
```json
{
  "message": "Patient added successfully",
  "patient": {
    "id": 1,
    "name": "John Doe",
    "age": 35,
    "gender": "M",
    "phone": "9876543210",
    "address": "123 Baker Street, London",
    "medical_history": "Hypertension, Asthma",
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:00:00Z"
  }
}
```

---

#### 2.2 List Patients Created by Authenticated User
* **Endpoint:** `GET /api/patients/`
* **Access:** Authenticated
* **Description:** Retrieves only patients created by the authenticated user.
* **Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "age": 35,
    "gender": "M",
    "phone": "9876543210",
    "address": "123 Baker Street, London",
    "medical_history": "Hypertension, Asthma",
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:00:00Z"
  }
]
```

---

#### 2.3 Get Specific Patient Details
* **Endpoint:** `GET /api/patients/<id>/`
* **Access:** Authenticated
* **Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "John Doe",
  "age": 35,
  "gender": "M",
  "phone": "9876543210",
  "address": "123 Baker Street, London",
  "medical_history": "Hypertension, Asthma",
  "created_by": "Satvik Shukla",
  "created_at": "2026-10-13T20:00:00Z",
  "updated_at": "2026-10-13T20:00:00Z"
}
```
* **Error Response (404 Not Found):**
```json
{
  "error": "Patient not found."
}
```

---

#### 2.4 Update Patient Details
* **Endpoint:** `PUT /api/patients/<id>/`
* **Access:** Authenticated (Owner only)
* **Request Body:**
```json
{
  "name": "John Doe",
  "age": 36,
  "gender": "M",
  "phone": "9876543210",
  "address": "456 Elm Street, London",
  "medical_history": "Hypertension, managed with medication"
}
```
* **Success Response (200 OK):**
```json
{
  "message": "Patient updated successfully",
  "patient": {
    "id": 1,
    "name": "John Doe",
    "age": 36,
    "gender": "M",
    "phone": "9876543210",
    "address": "456 Elm Street, London",
    "medical_history": "Hypertension, managed with medication",
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:30:00Z"
  }
}
```

---

#### 2.5 Delete Patient Record
* **Endpoint:** `DELETE /api/patients/<id>/`
* **Access:** Authenticated (Owner only)
* **Success Response (200 OK):**
```json
{
  "message": "Patient record deleted successfully."
}
```

---

### 3. Doctor Management APIs

#### 3.1 Add New Doctor
* **Endpoint:** `POST /api/doctors/`
* **Access:** Authenticated
* **Request Body:**
```json
{
  "name": "Dr. Gregory House",
  "specialization": "Diagnostic Medicine",
  "email": "house@princetonplainsboro.com",
  "phone": "9123456780",
  "experience_years": 15
}
```
* **Success Response (201 Created):**
```json
{
  "message": "Doctor added successfully",
  "doctor": {
    "id": 1,
    "name": "Dr. Gregory House",
    "specialization": "Diagnostic Medicine",
    "email": "house@princetonplainsboro.com",
    "phone": "9123456780",
    "experience_years": 15,
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:00:00Z"
  }
}
```

---

#### 3.2 List All Doctors
* **Endpoint:** `GET /api/doctors/`
* **Access:** Authenticated
* **Description:** Retrieves all doctors in the healthcare directory.
* **Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Dr. Gregory House",
    "specialization": "Diagnostic Medicine",
    "email": "house@princetonplainsboro.com",
    "phone": "9123456780",
    "experience_years": 15,
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:00:00Z"
  }
]
```

---

#### 3.3 Get Specific Doctor Details
* **Endpoint:** `GET /api/doctors/<id>/`
* **Access:** Authenticated
* **Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Dr. Gregory House",
  "specialization": "Diagnostic Medicine",
  "email": "house@princetonplainsboro.com",
  "phone": "9123456780",
  "experience_years": 15,
  "created_by": "Satvik Shukla",
  "created_at": "2026-10-13T20:00:00Z",
  "updated_at": "2026-10-13T20:00:00Z"
}
```

---

#### 3.4 Update Doctor Details
* **Endpoint:** `PUT /api/doctors/<id>/`
* **Access:** Authenticated (Only the creator of the doctor record can update)
* **Request Body:**
```json
{
  "name": "Dr. Gregory House",
  "specialization": "Diagnostics & Nephrology",
  "email": "house@princetonplainsboro.com",
  "phone": "9123456780",
  "experience_years": 16
}
```
* **Success Response (200 OK):**
```json
{
  "message": "Doctor updated successfully",
  "doctor": {
    "id": 1,
    "name": "Dr. Gregory House",
    "specialization": "Diagnostics & Nephrology",
    "email": "house@princetonplainsboro.com",
    "phone": "9123456780",
    "experience_years": 16,
    "created_by": "Satvik Shukla",
    "created_at": "2026-10-13T20:00:00Z",
    "updated_at": "2026-10-13T20:45:00Z"
  }
}
```
* **Error Response (403 Forbidden):**
```json
{
  "error": "You do not have permission to update this doctor record."
}
```

---

#### 3.5 Delete Doctor Record
* **Endpoint:** `DELETE /api/doctors/<id>/`
* **Access:** Authenticated (Only the creator can delete)
* **Success Response (200 OK):**
```json
{
  "message": "Doctor record deleted successfully."
}
```

---

### 4. Patient-Doctor Mapping APIs

#### 4.1 Assign Doctor to Patient
* **Endpoint:** `POST /api/mappings/`
* **Access:** Authenticated
* **Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1
}
```
*(Also accepts `{"patient": 1, "doctor": 1}`)*
* **Success Response (201 Created):**
```json
{
  "message": "Doctor assigned to patient successfully",
  "mapping": {
    "id": 1,
    "patient": {
      "id": 1,
      "name": "John Doe",
      "age": 35,
      "gender": "M",
      "phone": "9876543210"
    },
    "doctor": {
      "id": 1,
      "name": "Dr. Gregory House",
      "specialization": "Diagnostic Medicine",
      "email": "house@princetonplainsboro.com"
    },
    "assigned_at": "2026-10-13T21:00:00Z"
  }
}
```
* **Error Response (Duplicate Assignment - 400 Bad Request):**
```json
{
  "non_field_errors": ["This doctor is already assigned to this patient."]
}
```

---

#### 4.2 List All Patient-Doctor Mappings
* **Endpoint:** `GET /api/mappings/`
* **Access:** Authenticated
* **Description:** Retrieves all mapping relationships for patients created by the authenticated user.
* **Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "patient": { "id": 1, "name": "John Doe", "age": 35, "gender": "M" },
    "doctor": { "id": 1, "name": "Dr. Gregory House", "specialization": "Diagnostic Medicine" },
    "assigned_at": "2026-10-13T21:00:00Z"
  }
]
```

---

#### 4.3 Get All Doctors Assigned to a Specific Patient
* **Endpoint:** `GET /api/mappings/<patient_id>/`
* **Access:** Authenticated
* **Description:** Returns the complete list of doctors assigned to patient with ID `<patient_id>`. A single patient can have multiple doctors assigned.
* **Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Dr. Gregory House",
    "specialization": "Diagnostic Medicine",
    "email": "house@princetonplainsboro.com",
    "phone": "9123456780",
    "experience_years": 15
  },
  {
    "id": 2,
    "name": "Dr. James Wilson",
    "specialization": "Oncology",
    "email": "wilson@princetonplainsboro.com",
    "phone": "9123456781",
    "experience_years": 14
  }
]
```

---

#### 4.4 Remove Doctor from Patient
* **Endpoint:** `DELETE /api/mappings/<id>/`
* **Access:** Authenticated
* **Description:** Removes a mapping relationship. `<id>` is the primary key of the **mapping record** (returned by `GET /api/mappings/`).
* **Success Response (200 OK):**
```json
{
  "message": "Doctor removed from patient successfully."
}
```

---

## Data Seeding via Django ORM

To rapidly seed users, doctors, patients, and mappings in bulk, use Django's interactive shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from core.models import Doctor, Patient, PatientDoctorMapping

# 1. Get or create your authenticated user
user, _ = User.objects.get_or_create(
    username="satvik@example.com",
    defaults={"first_name": "Satvik", "email": "satvik@example.com"}
)
user.set_password("Password123")
user.save()

# 2. Bulk create Doctors
doctors = Doctor.objects.bulk_create([
    Doctor(name="Dr. House", specialization="Diagnostics", email="house@clinic.com", created_by=user),
    Doctor(name="Dr. Wilson", specialization="Oncology", email="wilson@clinic.com", created_by=user),
    Doctor(name="Dr. Cuddy", specialization="Endocrinology", email="cuddy@clinic.com", created_by=user),
])

# 3. Bulk create Patients
patients = Patient.objects.bulk_create([
    Patient(name="Liam Johnson", age=34, gender="M", phone="9811223344", created_by=user),
    Patient(name="Olivia Smith", age=27, gender="F", phone="9822334455", created_by=user),
])

# 4. Bulk create Mappings (assigning multiple doctors to a patient)
PatientDoctorMapping.objects.bulk_create([
    PatientDoctorMapping(patient=patients[0], doctor=doctors[0]),
    PatientDoctorMapping(patient=patients[0], doctor=doctors[1]),  # Liam gets 2 doctors!
    PatientDoctorMapping(patient=patients[1], doctor=doctors[2]),
])
```

---

## Error Handling & Validation

The API implements strict validation and error handling across all layers:
- **Email Uniqueness:** Rejects registration or doctor creation if the email already exists in the system.
- **Gender Choices:** Accepts `'M'`, `'F'`, or `'O'` (case-insensitive, also accepts `'Male'`, `'Female'`, `'Other'`).
- **Data Types:** Serializers safely convert IDs to integers, returning `400 Bad Request` with meaningful messages rather than unhandled 500 exceptions.
- **Ownership Security:** Users can only view, update, and delete their own patients, and can only assign doctors to patients they own.
- **Duplicate Prevention:** Database constraints prevent the same doctor from being assigned to the same patient more than once.
- **Status Codes:**
  - `200 OK` / `201 Created` for successful operations
  - `400 Bad Request` for invalid inputs or validation errors
  - `401 Unauthorized` for missing or invalid JWT tokens
  - `403 Forbidden` for attempting to edit/delete other users' records
  - `404 Not Found` for non-existent records
