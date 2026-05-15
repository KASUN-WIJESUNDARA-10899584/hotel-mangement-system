# 🏨 HMS Backend — PUSL3190

Hotel Management System REST API built with **FastAPI + SQLite**.

---

## Project Structure

```
hms_backend/
├── main.py                  # FastAPI app entry point
├── database.py              # SQLite setup & init
├── config.py                # JWT / settings
├── seed.py                  # Test data seeder
├── requirements.txt
├── middleware/
│   └── auth_middleware.py   # JWT auth + role guards
├── utils/
│   ├── auth.py              # JWT & password hashing
│   └── notifications.py     # Notification helper
└── routes/
    ├── auth.py              # Register, Login, Logout
    ├── rooms.py             # Get rooms, filter, update status
    ├── bookings.py          # Create, view, cancel, status update
    ├── service_requests.py  # Guest requests, staff updates
    ├── billing.py           # Get bill, mark paid
    └── notifications.py     # Get & mark read
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database with test data
python seed.py

# 3. Start the server
uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**  
Swagger docs at: **http://localhost:8000/docs**

---

## Test Credentials

| Role  | Email             | Password   |
|-------|-------------------|------------|
| Admin | admin@hms.com     | admin123   |
| Guest | guest@hms.com     | guest123   |
| Staff | staff@hms.com     | staff123   |

---

## API Endpoints

### Auth
| Method | Endpoint        | Auth     | Description       |
|--------|-----------------|----------|-------------------|
| POST   | /auth/register  | None     | Register user     |
| POST   | /auth/login     | None     | Login (get token) |
| POST   | /auth/logout    | Required | Logout            |
| GET    | /auth/me        | Required | Current user info |

### Rooms
| Method | Endpoint               | Role          | Description               |
|--------|------------------------|---------------|---------------------------|
| GET    | /rooms                 | Any           | Get all rooms (filterable)|
| GET    | /rooms/{id}            | Any           | Get room by ID            |
| PATCH  | /rooms/{id}/status     | Staff / Admin | Update room status        |

**Room filter query params:** `type`, `capacity`, `min_price`, `max_price`, `status`, `check_in`, `check_out`

### Bookings
| Method | Endpoint                      | Role           | Description            |
|--------|-------------------------------|----------------|------------------------|
| POST   | /bookings                     | Guest / Admin  | Create booking         |
| GET    | /bookings/my                  | Guest / Admin  | My bookings            |
| GET    | /bookings/{id}                | Any            | Get booking by ID      |
| PATCH  | /bookings/{id}/status         | Staff / Admin  | Update booking status  |
| DELETE | /bookings/{id}                | Any            | Cancel booking         |

**Booking statuses:** `confirmed` → `checked_in` → `checked_out` | `cancelled`

### Service Requests
| Method | Endpoint                  | Role           | Description              |
|--------|---------------------------|----------------|--------------------------|
| POST   | /service-requests         | Guest / Admin  | Create service request   |
| GET    | /service-requests         | Any            | Get requests (role-based)|
| PATCH  | /service-requests/{id}    | Staff / Admin  | Update request status    |

**Request types:** `housekeeping`, `maintenance`, `room_service`, `other`  
**Request statuses:** `pending` → `assigned` → `in_progress` → `completed`

### Billing
| Method | Endpoint                        | Role           | Description      |
|--------|---------------------------------|----------------|------------------|
| GET    | /bills/booking/{booking_id}     | Any            | Get bill         |
| POST   | /bills/booking/{booking_id}/pay | Guest / Admin  | Mark as paid     |

### Notifications
| Method | Endpoint                         | Auth     | Description              |
|--------|----------------------------------|----------|--------------------------|
| GET    | /notifications                   | Required | Get my notifications     |
| PATCH  | /notifications/{id}/read         | Required | Mark one as read         |
| PATCH  | /notifications/read-all          | Required | Mark all as read         |

---

## Authentication

All protected endpoints require a Bearer token in the header:
```
Authorization: Bearer <access_token>
```

Get a token by calling `POST /auth/login`.

---

## Roles & Permissions

| Feature               | Guest | Staff | Admin |
|-----------------------|-------|-------|-------|
| Browse rooms          | ✅    | ✅    | ✅    |
| Create booking        | ✅    | ❌    | ✅    |
| Cancel own booking    | ✅    | ❌    | ✅    |
| Update booking status | ❌    | ✅    | ✅    |
| Update room status    | ❌    | ✅    | ✅    |
| Create service req    | ✅    | ❌    | ✅    |
| Update service req    | ❌    | ✅    | ✅    |
| View/pay own bill     | ✅    | ❌    | ✅    |
| View notifications    | ✅    | ✅    | ✅    |
