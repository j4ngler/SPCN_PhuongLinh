"""
AI Recommender: Gợi ý học tập cá nhân hóa
Sử dụng mô hình đã huấn luyện để tính AI Score và đưa ra gợi ý học tập
"""

import pandas as pd
from pathlib import Path
import json
import joblib
import numpy as np
from typing import Dict, List, Optional


def get_project_root():
    """Tìm thư mục gốc dự án"""
    current = Path(__file__).resolve()
    if current.parent.name == 'scripts':
        return current.parent.parent
    return Path.cwd()


PROJECT_ROOT = get_project_root()
DATA_OUTPUT = PROJECT_ROOT / 'data' / 'output'
MODELS_DIR = PROJECT_ROOT / 'models'
CONFIG_DIR = PROJECT_ROOT / 'config'


def get_output_path(filename: str) -> Path:
    """Lấy đường dẫn file output"""
    DATA_OUTPUT.mkdir(parents=True, exist_ok=True)
    return DATA_OUTPUT / filename


def load_model():
    """Tải mô hình đã huấn luyện"""
    model_path = MODELS_DIR / 'ai_model.pkl'
    feature_info_path = MODELS_DIR / 'feature_info.json'
    
    if not model_path.exists():
        print("❌ Mô hình chưa được huấn luyện!")
        print("   Vui lòng chạy ai_model.py trước!")
        return None, None
    
    model = joblib.load(model_path)
    
    with open(feature_info_path, 'r', encoding='utf-8') as f:
        feature_info = json.load(f)
    
    return model, feature_info


def load_learning_paths():
    """Tải cấu hình lộ trình học tập"""
    config_path = CONFIG_DIR / 'learning_paths.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# Import từ ai_score_calculator
from ai_score_calculator import calculate_ai_scores, calculate_ai_score_for_subject, get_top_subjects_by_ai_score

def predict_ai_scores(student_id: Optional[str] = None):
    """
    Dự đoán AI Score cho tất cả sinh viên hoặc một sinh viên cụ thể
    (Wrapper function để tương thích ngược)
    """
    return calculate_ai_scores(student_id)


def generate_recommendations(student_id: str, top_n: int = 10) -> List[Dict]:
    """
    Tạo gợi ý học tập cá nhân hóa cho một sinh viên.
    
    Chiến lược hiện tại:
    - Tập trung vào các môn có AI Score THẤP / CHƯA CAO
      để học sinh ưu tiên cải thiện ở kỳ tiếp theo.
    """
    print(f"🎯 Tạo gợi ý học tập cho sinh viên: {student_id}")
    
    # Tính AI Score
    scores_df = predict_ai_scores(student_id)
    if scores_df is None or scores_df.empty:
        return []
    
    # Lấy các môn có AI Score thấp hơn để ưu tiên cải thiện
    # Sắp xếp tăng dần theo ai_score và chọn top_n đầu tiên
    scores_df = scores_df.sort_values('ai_score', ascending=True)
    top_subjects = scores_df.head(top_n)
    
    # Đọc hồ sơ sinh viên
    profiles_path = get_output_path('student_profiles_cleaned.csv')
    career_path = None
    if profiles_path.exists():
        profiles_df = pd.read_csv(profiles_path)
        student_profile = profiles_df[profiles_df['student_id'] == student_id]
        if not student_profile.empty:
            career_path = student_profile.iloc[0].get('career_path')
    
    # Đọc lộ trình học tập
    learning_paths = load_learning_paths()
    
    recommendations = []
    for idx, row in top_subjects.iterrows():
        score_val = float(row['ai_score'])

        # Phân loại mức độ để ghi lý do dễ hiểu hơn
        if score_val < 0.4:
            level_text = "còn khá thấp"
        elif score_val < 0.7:
            level_text = "ở mức trung bình, cần cải thiện thêm"
        else:
            level_text = "khá tốt nhưng vẫn có thể tối ưu"

        rec = {
            'student_id': row['student_id'],
            'subject_code': row['subject_code'],
            'subject_name': row['subject_name'],
            'ai_score': score_val,
            'priority': idx + 1,
            'reason': (
                f"Môn nên ưu tiên cải thiện ở kỳ tiếp theo (AI Score: {score_val:.2f}, "
                f"mức độ phù hợp hiện tại {level_text})"
            )
        }
        
        # Thêm lý do dựa trên career path nếu có
        if career_path and learning_paths:
            career_info = learning_paths.get('career_paths', {}).get(career_path.lower(), {})
            if row['subject_name'] in career_info.get('recommended_subjects', []):
                rec['reason'] += f" và phù hợp với định hướng {career_path}"
        
        recommendations.append(rec)
    
    return recommendations


def save_recommendations(recommendations: List[Dict], output_file: str = 'recommendations.csv'):
    """Lưu gợi ý vào file CSV"""
    if not recommendations:
        print("⚠️  Không có gợi ý để lưu")
        return
    
    df = pd.DataFrame(recommendations)
    output_path = get_output_path(output_file)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Đã lưu {len(recommendations)} gợi ý vào: {output_path}")


def save_ai_scores(scores_df: pd.DataFrame, output_file: str = 'ai_scores.csv'):
    """Lưu AI Score vào file CSV"""
    if scores_df is None or scores_df.empty:
        print("⚠️  Không có dữ liệu AI Score để lưu")
        return
    
    output_path = get_output_path(output_file)
    scores_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"✅ Đã lưu {len(scores_df)} bản ghi AI Score vào: {output_path}")


def process_all_students():
    """Xử lý gợi ý cho tất cả sinh viên"""
    print("🔄 Xử lý gợi ý cho tất cả sinh viên...")
    
    # Tính AI Score cho tất cả
    scores_df = predict_ai_scores()
    if scores_df is not None:
        save_ai_scores(scores_df)
    
    # Lấy danh sách sinh viên duy nhất
    if scores_df is not None and 'student_id' in scores_df.columns:
        student_ids = scores_df['student_id'].unique()
        
        all_recommendations = []
        for student_id in student_ids:
            recommendations = generate_recommendations(student_id, top_n=10)
            all_recommendations.extend(recommendations)
        
        if all_recommendations:
            save_recommendations(all_recommendations)
    
    print("✅ Hoàn thành xử lý gợi ý!")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        student_id = sys.argv[1]
        recommendations = generate_recommendations(student_id)
        save_recommendations(recommendations, f'recommendations_{student_id}.csv')
    else:
        process_all_students()

