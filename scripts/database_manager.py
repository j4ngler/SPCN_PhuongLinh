"""
Quản lý cơ sở dữ liệu SQLite cho hệ thống học tập cá nhân hóa
Tạo và quản lý các bảng: subjects, grades, feedback, student_profiles, ai_scores, recommendations
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional, List, Dict, Any


def get_project_root():
    """Tìm thư mục gốc dự án"""
    current = Path(__file__).resolve()
    if current.parent.name == 'scripts':
        return current.parent.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()
DB_PATH = PROJECT_ROOT / 'web' / 'student_learning.db'


def get_db_path() -> Path:
    """Lấy đường dẫn database, tạo thư mục nếu chưa có"""
    db_dir = DB_PATH.parent
    db_dir.mkdir(parents=True, exist_ok=True)
    return DB_PATH


def init_database():
    """Khởi tạo database và tạo các bảng nếu chưa tồn tại"""
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Bảng subjects: Thông tin môn học
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            category TEXT,
            credits INTEGER,
            difficulty_level TEXT,
            prerequisites TEXT
        )
    ''')
    
    # Bảng grades: Điểm số của sinh viên
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            grade_score REAL,
            attendance_rate REAL,
            homework_completion REAL,
            semester TEXT,
            year INTEGER,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    ''')
    
    # Bảng feedback: Nhận xét học tập (từ hệ thống hoặc tự đánh giá)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            comment TEXT,
            strengths TEXT,
            improvements TEXT,
            semester TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
            FOREIGN KEY (student_id) REFERENCES student_profiles(student_id)
        )
    ''')
    
    # Bảng student_profiles: Hồ sơ sinh viên
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_profiles (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            major TEXT,
            career_path TEXT,
            learning_style TEXT,
            interests TEXT,
            goals TEXT
        )
    ''')
    
    # Bảng ai_scores: Điểm phù hợp AI Score
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_scores (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            ai_score REAL NOT NULL,
            predicted_grade REAL,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    ''')
    
    # Bảng recommendations: Gợi ý học tập
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            recommendation_type TEXT,
            priority INTEGER,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database đã được khởi tạo tại: {db_path}")


def get_connection() -> sqlite3.Connection:
    """Lấy kết nối database"""
    db_path = get_db_path()
    return sqlite3.connect(str(db_path))


if __name__ == '__main__':
    init_database()

