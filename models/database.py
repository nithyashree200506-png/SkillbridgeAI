import sqlite3
import pymysql
import os
from config import Config
from werkzeug.security import generate_password_hash

def get_db_connection():
    if Config.DB_TYPE == 'mysql':
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                port=Config.MYSQL_PORT,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn, 'mysql'
        except Exception as e:
            print(f"[DB Warning] Could not connect to MySQL: {e}. Falling back to SQLite.")
    
    # SQLite Fallback
    conn = sqlite3.connect(Config.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn, 'sqlite'

def init_db():
    conn, db_type = get_db_connection()
    if db_type == 'sqlite':
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                department TEXT NOT NULL,
                year INTEGER NOT NULL,
                cgpa REAL NOT NULL,
                role TEXT DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                resume_name TEXT NOT NULL,
                resume_score REAL DEFAULT 0,
                placement_score REAL DEFAULT 0,
                skills TEXT,
                extracted_text TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES student (id) ON DELETE CASCADE
            )
        ''')
        
        # Check if default admin exists
        try:
            cursor.execute("SELECT id FROM student WHERE email = ?", ('admin@skillbridge.ai',))
            if not cursor.fetchone():
                admin_pwd = generate_password_hash('admin123')
                cursor.execute('''
                    INSERT OR IGNORE INTO student (name, email, password, department, year, cgpa, role)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', ('System Admin', 'admin@skillbridge.ai', admin_pwd, 'Administration', 4, 10.0, 'admin'))
        except Exception as e:
            print(f"[DB Info] Admin seed notice: {e}")
            
        conn.commit()
        conn.close()
        print("[DB Info] SQLite database initialized successfully.")

def get_student_by_email(email):
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    if db_type == 'sqlite':
        cursor.execute("SELECT * FROM student WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    else:
        cursor.execute("SELECT * FROM student WHERE email = %s", (email,))
        row = cursor.fetchone()
        conn.close()
        return row

def get_student_by_id(student_id):
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    if db_type == 'sqlite':
        cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    else:
        cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
        row = cursor.fetchone()
        conn.close()
        return row

def create_student(name, email, password_hash, department, year, cgpa, role='student'):
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    try:
        if db_type == 'sqlite':
            cursor.execute('''
                INSERT INTO student (name, email, password, department, year, cgpa, role)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, password_hash, department, year, cgpa, role))
        else:
            cursor.execute('''
                INSERT INTO student (name, email, password, department, year, cgpa, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (name, email, password_hash, department, year, cgpa, role))
        conn.commit()
        student_id = cursor.lastrowid
        return student_id
    finally:
        conn.close()

def save_resume(student_id, resume_name, resume_score, placement_score, skills_str, extracted_text):
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    try:
        if db_type == 'sqlite':
            cursor.execute('''
                INSERT INTO resume (student_id, resume_name, resume_score, placement_score, skills, extracted_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, resume_name, resume_score, placement_score, skills_str, extracted_text))
        else:
            cursor.execute('''
                INSERT INTO resume (student_id, resume_name, resume_score, placement_score, skills, extracted_text)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (student_id, resume_name, resume_score, placement_score, skills_str, extracted_text))
        conn.commit()
        resume_id = cursor.lastrowid
        return resume_id
    finally:
        conn.close()

def get_latest_resume(student_id):
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    if db_type == 'sqlite':
        cursor.execute("SELECT * FROM resume WHERE student_id = ? ORDER BY uploaded_at DESC LIMIT 1", (student_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    else:
        cursor.execute("SELECT * FROM resume WHERE student_id = %s ORDER BY uploaded_at DESC LIMIT 1", (student_id,))
        row = cursor.fetchone()
        conn.close()
        return row

def get_all_resumes_admin():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    if db_type == 'sqlite':
        cursor.execute('''
            SELECT r.*, s.name as student_name, s.email as student_email, s.department, s.year, s.cgpa
            FROM resume r
            JOIN student s ON r.student_id = s.id
            ORDER BY r.uploaded_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    else:
        cursor.execute('''
            SELECT r.*, s.name as student_name, s.email as student_email, s.department, s.year, s.cgpa
            FROM resume r
            JOIN student s ON r.student_id = s.id
            ORDER BY r.uploaded_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows

def get_all_students_admin():
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    if db_type == 'sqlite':
        cursor.execute('''
            SELECT s.*, 
                   r.resume_name, r.resume_score, r.placement_score, r.skills, r.uploaded_at
            FROM student s
            LEFT JOIN (
                SELECT r1.* FROM resume r1
                INNER JOIN (
                    SELECT student_id, MAX(uploaded_at) as max_date
                    FROM resume GROUP BY student_id
                ) r2 ON r1.student_id = r2.student_id AND r1.uploaded_at = r2.max_date
            ) r ON s.id = r.student_id
            WHERE s.role = 'student'
            ORDER BY s.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    else:
        cursor.execute('''
            SELECT s.*, 
                   r.resume_name, r.resume_score, r.placement_score, r.skills, r.uploaded_at
            FROM student s
            LEFT JOIN resume r ON s.id = r.student_id
            WHERE s.role = 'student'
            ORDER BY s.created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return rows
