"""
Tính điểm phù hợp (AI Score Calculator)
Module riêng để tính toán AI Score từ dự đoán của mô hình AI
Tách biệt logic tính điểm phù hợp khỏi ai_recommender.py
"""

import pandas as pd
from pathlib import Path
import json
import joblib
import numpy as np
from typing import Dict, List, Optional, Tuple


def get_project_root():
    """Tìm thư mục gốc dự án"""
    current = Path(__file__).resolve()
    if current.parent.name == 'scripts':
        return current.parent.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()
DATA_OUTPUT = PROJECT_ROOT / 'data' / 'output'
MODELS_DIR = PROJECT_ROOT / 'models'


def get_output_path(filename: str) -> Path:
    """Lấy đường dẫn file output"""
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    return DATA_OUTPUT / filename


def load_model():
    """Tải mô hình đã huấn luyện"""
    model_path = MODELS_DIR / 'ai_model.pkl'
    feature_info_path = MODELS_DIR / 'feature_info.json'
    
    if not model_path.exists():
        return None, None
    
    model = joblib.load(model_path)
    
    with open(feature_info_path, 'r', encoding='utf-8') as f:
        feature_info = json.load(f)
    
    return model, feature_info


def _filter_latest_term(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lọc dữ liệu để chỉ giữ lại học kỳ gần nhất cho từng học sinh.
    
    Ý nghĩa: dùng kết quả học tập ở học kỳ mới nhất để gợi ý
    cho *kỳ tiếp theo*.
    """
    if 'year' not in df.columns or 'semester' not in df.columns:
        # Không có thông tin học kỳ/năm -> giữ nguyên
        return df

    tmp = df.copy()
    # Chuyển về số để so sánh, lỗi thì để NaN
    tmp['year_int'] = pd.to_numeric(tmp['year'], errors='coerce')
    tmp['sem_int'] = pd.to_numeric(tmp['semester'], errors='coerce')

    # Nếu toàn NaN thì không lọc, tránh làm rỗng dữ liệu
    if tmp['year_int'].notna().sum() == 0 or tmp['sem_int'].notna().sum() == 0:
        return df

    # Tìm year và semester lớn nhất cho từng học sinh
    max_year = tmp.groupby('student_id')['year_int'].transform('max')
    # Với mỗi học sinh, trong năm lớn nhất, lấy học kỳ lớn nhất
    max_sem = (
        tmp[tmp['year_int'] == max_year]
        .groupby('student_id')['sem_int']
        .transform('max')
    )

    mask = (tmp['year_int'] == max_year) & (tmp['sem_int'] == max_sem)
    tmp = tmp[mask].drop(columns=['year_int', 'sem_int'])
    return tmp


def calculate_ai_scores(student_id: Optional[str] = None) -> Optional[pd.DataFrame]:
    """
    Tính điểm phù hợp (AI Score) cho tất cả sinh viên hoặc một sinh viên cụ thể
    Dữ liệu dùng để tính được lọc theo *học kỳ gần nhất* của từng học sinh
    (hiểu là gợi ý cho kỳ tiếp theo).
    
    Returns:
        DataFrame với columns: student_id, subject_code, subject_name, ai_score
        (nếu có) sẽ giữ thêm các cột year, semester để tham chiếu
    """
    # Tải mô hình
    model, feature_info = load_model()
    if model is None:
        print("❌ Mô hình chưa được huấn luyện!")
        return None
    
    # Đọc dữ liệu features
    features_path = get_output_path('features.csv')
    if not features_path.exists():
        print("❌ File features.csv không tồn tại!")
        return None
    
    df = pd.read_csv(features_path)

    # Lọc theo student_id nếu có
    if student_id:
        df = df[df['student_id'] == student_id]
        if df.empty:
            print(f"❌ Không tìm thấy sinh viên: {student_id}")
            return None

    # Lọc theo học kỳ gần nhất cho từng học sinh
    df = _filter_latest_term(df)
    if df.empty:
        print("❌ Không còn dữ liệu sau khi lọc theo học kỳ gần nhất")
        return None

    # Lấy các đặc trưng
    feature_cols = feature_info['features']
    X = df[feature_cols].fillna(0)
    
    # Dự đoán AI Score
    predictions = model.predict(X)
    
    # Tạo DataFrame kết quả
    base_cols = ['student_id', 'subject_code', 'subject_name']
    # Giữ thêm year, semester nếu có để tham chiếu trên dashboard / phân tích
    if 'year' in df.columns:
        base_cols.append('year')
    if 'semester' in df.columns:
        base_cols.append('semester')

    result_df = df[base_cols].copy()
    result_df['ai_score'] = predictions
    result_df['ai_score'] = result_df['ai_score'].clip(0, 1)  # Đảm bảo trong khoảng 0-1
    
    # Sắp xếp theo AI Score giảm dần
    result_df = result_df.sort_values('ai_score', ascending=False)
    
    return result_df


def calculate_ai_score_for_subject(student_id: str, subject_code: str) -> Optional[float]:
    """
    Tính AI Score cho một cặp sinh viên-môn học cụ thể
    
    Returns:
        AI Score (float) hoặc None nếu không tìm thấy
    """
    scores_df = calculate_ai_scores(student_id)
    if scores_df is None or scores_df.empty:
        return None
    
    subject_scores = scores_df[scores_df['subject_code'] == subject_code]
    if subject_scores.empty:
        return None
    
    return float(subject_scores.iloc[0]['ai_score'])


def get_top_subjects_by_ai_score(student_id: str, top_n: int = 10) -> List[Dict]:
    """
    Lấy top N môn học có AI Score cao nhất cho một sinh viên
    
    Returns:
        List of dicts với thông tin môn học và AI Score
    """
    scores_df = calculate_ai_scores(student_id)
    if scores_df is None or scores_df.empty:
        return []
    
    top_subjects = scores_df.head(top_n)
    
    return top_subjects.to_dict('records')


if __name__ == '__main__':
    # Test
    print("🧪 Test tính AI Score...")
    scores = calculate_ai_scores('SV001')
    if scores is not None:
        print(f"✅ Tìm thấy {len(scores)} môn học cho SV001")
        print(scores.head())

