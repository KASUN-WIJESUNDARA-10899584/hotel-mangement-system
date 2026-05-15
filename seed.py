"""
Run once to populate the database with test data:
    python seed.py
"""
from database import init_db, get_db
from utils.auth import hash_password

def seed():
    init_db()

    with get_db() as conn:
        # ── Users ──────────────────────────────────────────────────────────────
        users = [
            ("Admin User",     "admin@hms.com",  hash_password("admin123"),  "admin"),
            ("John Guest",     "guest@hms.com",  hash_password("guest123"),  "guest"),
            ("Alice Staff",    "staff@hms.com",  hash_password("staff123"),  "staff"),
        ]
        for u in users:
            conn.execute(
                "INSERT OR IGNORE INTO users (name, email, password, role) VALUES (?, ?, ?, ?)", u
            )

        # ── Rooms ──────────────────────────────────────────────────────────────
        rooms = [
            ("101", "single",  1, 50.00,  "available",    "WiFi, TV",           "Cozy single room"),
            ("102", "double",  2, 90.00,  "available",    "WiFi, TV, Mini-bar", "Comfortable double room"),
            ("201", "suite",   4, 200.00, "available",    "WiFi, TV, Jacuzzi",  "Luxury suite with ocean view"),
            ("202", "double",  2, 85.00,  "cleaning",     "WiFi, TV",           "Standard double room"),
            ("301", "single",  1, 55.00,  "maintenance",  "WiFi",               "Single room under renovation"),
        ]
        for r in rooms:
            conn.execute(
                """INSERT OR IGNORE INTO rooms
                   (number, type, capacity, price, status, amenities, description)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""", r
            )

    print("✅ Seed data inserted.")
    print("\nTest credentials:")
    print("  Admin  → admin@hms.com  / admin123")
    print("  Guest  → guest@hms.com  / guest123")
    print("  Staff  → staff@hms.com  / staff123")


if __name__ == "__main__":
    seed()
