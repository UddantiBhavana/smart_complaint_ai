import sqlite3
from datetime import datetime
import os

DB_PATH = "database/complaints.db"


def create_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_name TEXT,
        phone_number TEXT,
        address TEXT,
        complaint_text TEXT NOT NULL,
        text_category TEXT,
        image_category TEXT,
        confidence REAL,
        evidence_status TEXT,
        department TEXT,
        recommendation TEXT,
        priority_score REAL DEFAULT 0,
        severity TEXT DEFAULT 'Medium',
        reports_count INTEGER DEFAULT 1,
        status TEXT DEFAULT 'Pending',
        before_image TEXT,
        after_image TEXT,
        resolved_at TEXT,
        created_at TEXT
    )
    """)

    # NEW: activity log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaint_activity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        note TEXT,
        officer TEXT,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (complaint_id) REFERENCES complaints(id)
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        department TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER,
        rating INTEGER,
        feedback TEXT,
        created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_default_users():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    users = [
        ("road_officer", "road123", "Officer", "Road Maintenance Department"),
        ("water_officer", "water123", "Officer", "Water Supply Department"),
        ("drainage_officer", "drain123", "Officer", "Drainage Department"),
        ("electric_officer", "elec123", "Officer", "Electricity Department"),
        ("sanitation_officer", "clean123", "Officer", "Sanitation Department"),
        ("admin", "admin123", "Admin", "All Departments")
    ]

    for username, password, role, department in users:

        cursor.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role, department)
            VALUES (?, ?, ?, ?)
        """, (username, password, role, department))

    conn.commit()
    conn.close()

def insert_complaint(
    citizen_name,
    phone_number,
    address,
    complaint_text,
    text_category,
    image_category,
    confidence,
    evidence_status,
    department,
    recommendation,
    priority_score,
    severity,
    before_image
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints(
        citizen_name,
        phone_number,
        address,
        complaint_text,
        text_category,
        image_category,
        confidence,
        evidence_status,
        department,
        recommendation,
        priority_score,
        severity,
        before_image,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?)
    """,
    (
        citizen_name,
        phone_number,
        address,
        complaint_text,
        text_category,
        image_category,
        confidence,
        evidence_status,
        department,
        recommendation,
        priority_score,
        severity,
        before_image,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

def get_all_complaints():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
        id,
        citizen_name,
        phone_number,
        address,
        complaint_text,
        text_category,
        image_category,
        confidence,
        evidence_status,
        department,
        recommendation,
        priority_score,
        severity,
        reports_count,
        status,
        before_image,
        after_image,
        resolved_at,
        created_at
        FROM complaints
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_status(complaint_id, new_status):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (new_status, complaint_id)
    )

    conn.commit()
    conn.close()


# ── NEW FUNCTIONS ────────────────────────────────────────────────────

def log_activity(complaint_id, action, note="", officer="Department Officer"):
    """Write one entry into the activity timeline for a complaint."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaint_activity (complaint_id, action, note, officer, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        complaint_id,
        action,
        note,
        officer,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_activity_log(complaint_id):
    """Return all timeline entries for a complaint, oldest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT action, note, officer, timestamp
        FROM complaint_activity
        WHERE complaint_id = ?
        ORDER BY timestamp ASC
    """, (complaint_id,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_status_with_log(complaint_id, new_status, note, officer):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if new_status == "Resolved":

        cursor.execute(
            """
            UPDATE complaints
            SET status=?,
                resolved_at=?
            WHERE id=?
            """,
            (
                new_status,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                complaint_id
            )
        )

    else:

        cursor.execute(
            """
            UPDATE complaints
            SET status=?
            WHERE id=?
            """,
            (
                new_status,
                complaint_id
            )
        )

    conn.commit()
    conn.close()

    log_activity(
        complaint_id,
        action=f"Status changed to {new_status}",
        note=note,
        officer=officer
    )


def increase_report_count(complaint_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET reports_count = reports_count + 1
        WHERE id = ?
    """, (complaint_id,))

    conn.commit()
    conn.close()

def get_active_complaints():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE status != 'Resolved'
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_complaint_by_id_and_phone(complaint_id, phone_number):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        WHERE id=? AND phone_number=?
    """, (complaint_id, phone_number))

    row = cursor.fetchone()

    conn.close()

    return row

def submit_feedback(complaint_id, rating, feedback_text):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback(
            complaint_id,
            rating,
            feedback,
            created_at
        )
        VALUES (?, ?, ?, ?)
    """,
    (
        complaint_id,
        rating,
        feedback_text,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_feedback(complaint_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT rating, feedback, created_at
        FROM feedback
        WHERE complaint_id = ?
    """,(complaint_id,))

    row = cursor.fetchone()

    conn.close()

    return row

def reopen_complaint(complaint_id, reason):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE complaints
        SET status = ?
        WHERE id = ?
        """,
        ("Reopened", complaint_id)
    )

    conn.commit()
    conn.close()

    log_activity(
        complaint_id,
        action="Complaint reopened by citizen",
        note=reason,
        officer="Citizen"
    )

def escalate_complaint(complaint_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check current status
    cursor.execute(
        """
        SELECT status
        FROM complaints
        WHERE id = ?
        """,
        (complaint_id,)
    )

    row = cursor.fetchone()

    if row and row[0] != "Escalated":

        cursor.execute(
            """
            UPDATE complaints
            SET status = ?
            WHERE id = ?
            """,
            ("Escalated", complaint_id)
        )

        conn.commit()

        log_activity(
            complaint_id,
            action="Escalated to Senior Officer",
            note="Complaint exceeded SLA time.",
            officer="System"
        )

    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT username, role, department
        FROM users
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_all_feedback():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rating, feedback, created_at
        FROM feedback
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_average_rating():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(rating)
        FROM feedback
    """)
    avg = cursor.fetchone()[0]
    conn.close()
    return round(avg,2) if avg else 0


def update_after_image(complaint_id, image_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE complaints
        SET after_image = ?
        WHERE id = ?
        """,
        (image_path, complaint_id)
    )

    conn.commit()
    conn.close()

def get_before_after_images(complaint_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT before_image, after_image
        FROM complaints
        WHERE id=?
        """,
        (complaint_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row

def get_officer_performance():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT officer,
            COUNT(*) as total_actions
        FROM complaint_activity
        WHERE officer != 'Citizen'
        AND officer != 'System'
        GROUP BY officer
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_location_statistics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT address,
            COUNT(*) as total_complaints
        FROM complaints
        GROUP BY address
        ORDER BY total_complaints DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows
