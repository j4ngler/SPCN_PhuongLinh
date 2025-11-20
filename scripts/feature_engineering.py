"""
Feature Engineering: Mã hóa đặc trưng từ dữ liệu đã làm sạch
Tạo file features.csv với các đặc trưng đã được mã hóa sẵn sàng cho mô hình AI
"""

import pandas as pd
from pathlib import Path
import json
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np


def get_project_root():
    """Tìm thư mục gốc dự án"""
    current = Path(__file__).resolve()
    if current.parent.name == 'scripts':
        return current.parent.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()
DATA_OUTPUT = PROJECT_ROOT / 'data' / 'output'
CONFIG_DIR = PROJECT_ROOT / 'config'


def get_output_path(filename: str) -> Path:
    """Lấy đường dẫn file output"""
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    return DATA_OUTPUT / filename


def load_config():
    """Đọc cấu hình từ model_config.json"""
    config_path = CONFIG_DIR / 'model_config.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def encode_categorical_features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Mã hóa các đặc trưng phân loại"""
    df_encoded = df.copy()
    encoders = {}
    
    for col in columns:
        if col in df_encoded.columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = le
    
    return df_encoded, encoders


def normalize_numerical_features(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Chuẩn hóa các đặc trưng số"""
    df_normalized = df.copy()
    scaler = StandardScaler()
    
    for col in columns:
        if col in df_normalized.columns:
            df_normalized[col] = scaler.fit_transform(df_normalized[[col]])
    
    return df_normalized, scaler


def create_features():
    """Tạo file features.csv từ dữ liệu đã làm sạch"""
    print("🔄 Bắt đầu Feature Engineering...")
    
    # Đọc dữ liệu đã làm sạch
    subjects_path = get_output_path('subjects_cleaned.csv')
    grades_path = get_output_path('grades_cleaned.csv')
    profiles_path = get_output_path('student_profiles_cleaned.csv')
    
    if not subjects_path.exists() or not grades_path.exists():
        print("❌ Vui lòng chạy data_processor.py trước!")
        return
    
    subjects_df = pd.read_csv(subjects_path)
    grades_df = pd.read_csv(grades_path)
    
    # Merge dữ liệu
    merged_df = grades_df.merge(
        subjects_df,
        left_on='subject_code',
        right_on='subject_code',
        how='left'
    )
    
    # Đọc hồ sơ sinh viên nếu có
    if profiles_path.exists():
        profiles_df = pd.read_csv(profiles_path)
        merged_df = merged_df.merge(
            profiles_df,
            on='student_id',
            how='left'
        )
    
    # Đọc cấu hình
    config = load_config()
    numerical_features = config.get('features', {}).get('numerical', [])
    categorical_features = config.get('features', {}).get('categorical', [])
    
    # Tạo các đặc trưng mới
    # 1. Điểm trung bình của sinh viên
    if 'grade_score' in merged_df.columns:
        student_avg = merged_df.groupby('student_id')['grade_score'].transform('mean')
        merged_df['student_avg_grade'] = student_avg
    
    # 2. Độ khó môn học (nếu có)
    if 'difficulty_level' in merged_df.columns:
        difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
        merged_df['difficulty_numeric'] = merged_df['difficulty_level'].map(
            lambda x: difficulty_map.get(x, 2)
        )
    
    # 3. Tỷ lệ hoàn thành tổng thể
    if 'attendance_rate' in merged_df.columns and 'homework_completion' in merged_df.columns:
        merged_df['completion_rate'] = (
            merged_df['attendance_rate'] * 0.4 + 
            merged_df['homework_completion'] * 0.6
        )
    
    # Mã hóa đặc trưng phân loại
    categorical_cols = [col for col in categorical_features if col in merged_df.columns]
    if categorical_cols:
        merged_df, _ = encode_categorical_features(merged_df, categorical_cols)

    # Tự động mã hóa các cột dạng object còn lại (tránh lỗi khi huấn luyện)
    object_exclude = {
        'student_id',
        'subject_code',
        'name',
        'comment',
        'strengths',
        'improvements'
    }
    auto_categorical_cols = [
        col for col in merged_df.select_dtypes(include=['object']).columns
        if col not in object_exclude
    ]
    if auto_categorical_cols:
        merged_df, _ = encode_categorical_features(merged_df, auto_categorical_cols)

    # Chuẩn hóa đặc trưng số
    numerical_cols = [col for col in numerical_features if col in merged_df.columns]
    if numerical_cols:
        merged_df, _ = normalize_numerical_features(merged_df, numerical_cols)
    
    # Lưu file features
    output_path = get_output_path('features.csv')
    merged_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Đã tạo file features.csv với {len(merged_df)} dòng và {len(merged_df.columns)} cột")
    print(f"   Đường dẫn: {output_path}")
    
    return merged_df


if __name__ == '__main__':
    create_features()

