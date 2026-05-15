import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "hms.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT    NOT NULL,
                email       TEXT    NOT NULL UNIQUE,
                password    TEXT    NOT NULL,
                role        TEXT    NOT NULL DEFAULT 'guest'
                                    CHECK(role IN ('guest','staff','admin')),
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS rooms (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                number      TEXT    NOT NULL UNIQUE,
                type        TEXT    NOT NULL,
                capacity    INTEGER NOT NULL,
                price       REAL    NOT NULL,
                status      TEXT    NOT NULL DEFAULT 'available'
                                    CHECK(status IN ('available','occupied','cleaning','maintenance')),
                amenities   TEXT,
                description TEXT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS bookings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_id        INTEGER NOT NULL REFERENCES users(id),
                room_id         INTEGER NOT NULL REFERENCES rooms(id),
                check_in        TEXT    NOT NULL,
                check_out       TEXT    NOT NULL,
                status          TEXT    NOT NULL DEFAULT 'confirmed'
                                        CHECK(status IN ('confirmed','checked_in','checked_out','cancelled')),
                total_price     REAL    NOT NULL,
                guests_count    INTEGER NOT NULL DEFAULT 1,
                created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS service_requests (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id  INTEGER NOT NULL REFERENCES bookings(id),
                guest_id    INTEGER NOT NULL REFERENCES users(id),
                staff_id    INTEGER REFERENCES users(id),
                type        TEXT    NOT NULL
                                    CHECK(type IN ('housekeeping','maintenance','room_service','other')),
                description TEXT,
                status      TEXT    NOT NULL DEFAULT 'pending'
                                    CHECK(status IN ('pending','assigned','in_progress','completed')),
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS bills (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_id  INTEGER NOT NULL UNIQUE REFERENCES bookings(id),
                guest_id    INTEGER NOT NULL REFERENCES users(id),
                amount      REAL    NOT NULL,
                paid        INTEGER NOT NULL DEFAULT 0,
                paid_at     TEXT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL REFERENCES users(id),
                title       TEXT    NOT NULL,
                message     TEXT    NOT NULL,
                is_read     INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
            );
        """)
    print("✅ Database initialized.")