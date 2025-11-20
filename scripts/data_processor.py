"""
Xử lý và làm sạch dữ liệu từ các file CSV đầu vào
Chuẩn hóa dữ liệu: subjects.csv, grades.csv, teacher_feedback.csv, career_path.csv, student_profile.csv
"""

import pandas as pd
from pathlib import Path
import os
import sys


def get_project_root():
    """Tìm thư mục gốc dự án"""
    current = Path(__file__).resolve()
    if current.parent.name == 'scripts':
        return current.parent.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()
DATA_INPUT = PROJECT_ROOT / 'data' / 'input'
DATA_OUTPUT = PROJECT_ROOT / 'data' / 'output'


def get_input_path(filename: str) -> Path:
    """Lấy đường dẫn file input"""
    return DATA_INPUT / filename


def get_output_path(filename: str) -> Path:
    """Lấy đường dẫn file output, tạo thư mục nếu chưa có"""
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    return DATA_OUTPUT / filename


def load_csv_safe(filename: str) -> pd.DataFrame:
    """Đọc file CSV an toàn, trả về DataFrame rỗng nếu không tồn tại"""
    path = get_input_path(filename)
    if not path.exists():
        print(f"⚠️  File không tồn tại: {path}")
        print(f"   Tạo file mẫu tại: {path}")
        return pd.DataFrame()
    try:
        return pd.read_csv(path, encoding='utf-8')
    except Exception as e:
        print(f"❌ Lỗi đọc file {filename}: {e}")
        return pd.DataFrame()


def clean_subjects(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu môn học"""
    if df.empty:
        return df
    
    # Loại bỏ dòng trùng lặp
    df = df.drop_duplicates(subset=['subject_code'], keep='first')
    
    # Điền giá trị thiếu
    df['category'] = df['category'].fillna('General')
    df['credits'] = pd.to_numeric(df['credits'], errors='coerce').fillna(3)
    df['difficulty_level'] = df['difficulty_level'].fillna('Medium')
    
    return df


def clean_grades(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu điểm số"""
    if df.empty:
        return df
    
    # Chuyển đổi kiểu dữ liệu
    df['grade_score'] = pd.to_numeric(df['grade_score'], errors='coerce')
    df['attendance_rate'] = pd.to_numeric(df['attendance_rate'], errors='coerce')
    df['homework_completion'] = pd.to_numeric(df['homework_completion'], errors='coerce')
    
    # Chuẩn hóa điểm số về thang 0-10
    df['grade_score'] = df['grade_score'].clip(0, 10)
    df['attendance_rate'] = df['attendance_rate'].clip(0, 1)
    df['homework_completion'] = df['homework_completion'].clip(0, 1)
    
    # Loại bỏ dòng có điểm số không hợp lệ
    df = df.dropna(subset=['student_id', 'subject_code', 'grade_score'])
    
    return df


def clean_feedback(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu nhận xét giáo viên"""
    if df.empty:
        return df
    
    # Điền giá trị thiếu
    df['comment'] = df['comment'].fillna('')
    df['strengths'] = df['strengths'].fillna('')
    df['improvements'] = df['improvements'].fillna('')
    
    return df


def clean_student_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu hồ sơ sinh viên"""
    if df.empty:
        return df
    
    # Điền giá trị thiếu
    df['major'] = df['major'].fillna('Unknown')
    df['career_path'] = df['career_path'].fillna('General')
    df['learning_style'] = df['learning_style'].fillna('Mixed')
    
    return df


def process_all_data():
    """Xử lý tất cả dữ liệu đầu vào"""
    print("🔄 Bắt đầu xử lý dữ liệu...")
    
    # Đọc các file CSV
    subjects_df = load_csv_safe('subjects.csv')
    grades_df = load_csv_safe('grades.csv')
    feedback_df = load_csv_safe('teacher_feedback.csv')
    career_path_df = load_csv_safe('career_path.csv')
    student_profiles_df = load_csv_safe('student_profile.csv')
    
    # Làm sạch dữ liệu
    if not subjects_df.empty:
        subjects_df = clean_subjects(subjects_df)
        subjects_df.to_csv(get_output_path('subjects_cleaned.csv'), index=False, encoding='utf-8')
        print(f"✅ Đã xử lý {len(subjects_df)} môn học")
    
    if not grades_df.empty:
        grades_df = clean_grades(grades_df)
        grades_df.to_csv(get_output_path('grades_cleaned.csv'), index=False, encoding='utf-8')
        print(f"✅ Đã xử lý {len(grades_df)} bản ghi điểm số")
    
    if not feedback_df.empty:
        feedback_df = clean_feedback(feedback_df)
        feedback_df.to_csv(get_output_path('feedback_cleaned.csv'), index=False, encoding='utf-8')
        print(f"✅ Đã xử lý {len(feedback_df)} nhận xét")
    
    if not student_profiles_df.empty:
        student_profiles_df = clean_student_profiles(student_profiles_df)
        student_profiles_df.to_csv(get_output_path('student_profiles_cleaned.csv'), index=False, encoding='utf-8')
        print(f"✅ Đã xử lý {len(student_profiles_df)} hồ sơ sinh viên")
    
    print("✅ Hoàn thành xử lý dữ liệu!")


if __name__ == '__main__':
    process_all_data()

