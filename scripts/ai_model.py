"""
Huấn luyện mô hình RandomForestRegressor để tính điểm phù hợp AI Score
Dự đoán điểm phù hợp giữa sinh viên và môn học/kỹ năng
"""

import pandas as pd
from pathlib import Path
import json
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
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
MODELS_DIR = PROJECT_ROOT / 'models'


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


def create_target_variable(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tạo biến mục tiêu (AI Score) dựa trên:
    - Điểm số hiện tại
    - Tỷ lệ tham gia
    - Hoàn thành bài tập
    - Phản hồi giáo viên (nếu có)
    """
    df = df.copy()
    
    # Tính AI Score ban đầu (có thể điều chỉnh)
    if 'grade_score' in df.columns:
        base_score = df['grade_score'] / 10.0  # Chuẩn hóa về 0-1
    else:
        base_score = 0.5
    
    # Điều chỉnh theo attendance
    if 'attendance_rate' in df.columns:
        base_score = base_score * 0.7 + df['attendance_rate'] * 0.3
    
    # Điều chỉnh theo homework completion
    if 'homework_completion' in df.columns:
        base_score = base_score * 0.8 + df['homework_completion'] * 0.2
    
    # Thêm yếu tố ngẫu nhiên nhỏ để tạo đa dạng (trong thực tế sẽ dùng dữ liệu thật)
    np.random.seed(42)
    noise = np.random.normal(0, 0.05, len(df))
    df['ai_score'] = np.clip(base_score + noise, 0, 1)
    
    return df


def train_model():
    """Huấn luyện mô hình RandomForestRegressor"""
    print("🔄 Bắt đầu huấn luyện mô hình AI...")
    
    # Đọc cấu hình
    config = load_config()
    model_config = config.get('model', {})
    target = config.get('target', 'ai_score')
    min_accuracy = config.get('min_accuracy', 0.80)
    
    # Đọc dữ liệu features
    features_path = get_output_path('features.csv')
    if not features_path.exists():
        print("❌ File features.csv không tồn tại!")
        print("   Vui lòng chạy feature_engineering.py trước!")
        return None
    
    df = pd.read_csv(features_path)
    print(f"📊 Đã đọc {len(df)} dòng dữ liệu")
    
    # Tạo biến mục tiêu nếu chưa có
    if target not in df.columns:
        print("📝 Tạo biến mục tiêu AI Score...")
        df = create_target_variable(df)
        df.to_csv(features_path, index=False, encoding='utf-8')
    
    # Chọn các đặc trưng (loại bỏ ID và target)
    exclude_cols = ['student_id', 'subject_code', 'subject_id', target, 'name', 'comment']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    # Loại bỏ các cột có quá nhiều giá trị thiếu
    feature_cols = [col for col in feature_cols if df[col].notna().sum() > len(df) * 0.5]
    
    X = df[feature_cols].fillna(0)
    y = df[target]
    
    print(f"📈 Sử dụng {len(feature_cols)} đặc trưng")
    print(f"   Các đặc trưng: {', '.join(feature_cols[:10])}...")
    
    # Chia dữ liệu train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Tạo và huấn luyện mô hình
    model = RandomForestRegressor(
        n_estimators=model_config.get('n_estimators', 100),
        max_depth=model_config.get('max_depth', 10),
        min_samples_split=model_config.get('min_samples_split', 5),
        min_samples_leaf=model_config.get('min_samples_leaf', 2),
        random_state=model_config.get('random_state', 42)
    )
    
    print("🎯 Đang huấn luyện mô hình...")
    model.fit(X_train, y_train)
    
    # Đánh giá mô hình
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    print("\n📊 Kết quả đánh giá mô hình:")
    print(f"   Train R² Score: {train_r2:.4f}")
    print(f"   Test R² Score: {test_r2:.4f}")
    print(f"   Test MAE: {test_mae:.4f}")
    print(f"   Test RMSE: {test_rmse:.4f}")
    
    if test_r2 >= min_accuracy:
        print(f"✅ Mô hình đạt yêu cầu (R² >= {min_accuracy})")
    else:
        print(f"⚠️  Mô hình chưa đạt yêu cầu (R² < {min_accuracy})")
    
    # Lưu mô hình
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / 'ai_model.pkl'
    joblib.dump(model, model_path)
    print(f"💾 Đã lưu mô hình tại: {model_path}")
    
    # Lưu danh sách đặc trưng
    feature_info = {
        'features': feature_cols,
        'target': target,
        'metrics': {
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'test_mae': float(test_mae),
            'test_rmse': float(test_rmse)
        }
    }
    
    feature_info_path = MODELS_DIR / 'feature_info.json'
    with open(feature_info_path, 'w', encoding='utf-8') as f:
        json.dump(feature_info, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Đã lưu thông tin đặc trưng tại: {feature_info_path}")
    
    return model


if __name__ == '__main__':
    train_model()

