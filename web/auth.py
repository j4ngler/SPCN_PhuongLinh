"""
Module xác thực và phân quyền cho 2 loại người dùng:
- HocSinh (Student): Học sinh cấp 3 - Xem kết quả và yêu cầu gợi ý học tập
- PhuHuynh (Parent): Phụ huynh - Xem kết quả học tập của con
"""

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, Dict
import sqlite3
import sys
from pathlib import Path

# Import database_manager từ scripts
project_root = Path(__file__).parent.parent
scripts_dir = project_root / 'scripts'
sys.path.insert(0, str(scripts_dir))

from database_manager import get_connection


USER_ROLES = {
    'student': 'HocSinh',
    'parent': 'PhuHuynh'
}


def init_auth_database():
    """Khởi tạo bảng users trong database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Bảng users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            student_id TEXT,  -- Cho PhuHuynh: mã học sinh của con
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES student_profiles(student_id)
        )
    ''')
    
    conn.commit()
    conn.close()


def create_user(user_id: str, username: str, password: str, role: str, 
                full_name: str = None, email: str = None, student_id: str = None):
    """Tạo người dùng mới"""
    conn = get_connection()
    cursor = conn.cursor()
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute('''
            INSERT INTO users (user_id, username, password_hash, role, full_name, email, student_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, username, password_hash, role, full_name, email, student_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """Xác thực người dùng"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, username, password_hash, role, full_name, email, student_id
        FROM users WHERE username = ?
    ''', (username,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        return {
            'user_id': user[0],
            'username': user[1],
            'role': user[3],
            'full_name': user[4],
            'email': user[5],
            'student_id': user[6]
        }
    
    return None


def login_user(user_data: Dict):
    """Đăng nhập người dùng (lưu vào session)"""
    session['user_id'] = user_data['user_id']
    session['username'] = user_data['username']
    session['role'] = user_data['role']
    session['full_name'] = user_data.get('full_name')
    session['student_id'] = user_data.get('student_id')


def logout_user():
    """Đăng xuất người dùng"""
    session.clear()


def get_current_user() -> Optional[Dict]:
    """Lấy thông tin người dùng hiện tại từ session"""
    if 'user_id' not in session:
        return None
    
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'role': session.get('role'),
        'full_name': session.get('full_name'),
        'student_id': session.get('student_id')
    }


def require_role(role: str):
    """Decorator để yêu cầu quyền truy cập"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user or user['role'] != role:
                from flask import redirect, url_for
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator


def is_student() -> bool:
    """Kiểm tra người dùng có phải học sinh không"""
    user = get_current_user()
    return user and user['role'] == 'student'


def is_parent() -> bool:
    """Kiểm tra người dùng có phải phụ huynh không"""
    user = get_current_user()
    return user and user['role'] == 'parent'


def get_student_id_for_user() -> Optional[str]:
    """Lấy student_id cho người dùng hiện tại"""
    user = get_current_user()
    if not user:
        return None
    
    # Nếu là học sinh, trả về user_id
    if user['role'] == 'student':
        return user['user_id']
    
    # Nếu là phụ huynh, trả về student_id của con
    if user['role'] == 'parent':
        return user.get('student_id')
    
    return None

