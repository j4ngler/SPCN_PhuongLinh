"""
Pipeline chạy toàn bộ quy trình xử lý dữ liệu và AI
1. Xử lý dữ liệu (data_processor.py)
2. Feature Engineering (feature_engineering.py)
3. Huấn luyện mô hình (ai_model.py)
4. Tạo gợi ý (ai_recommender.py)
"""

import sys
from pathlib import Path

# Thêm thư mục scripts vào path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

from data_processor import process_all_data
from feature_engineering import create_features
from ai_model import train_model
from ai_recommender import process_all_students
from database_manager import init_database


def run_full_pipeline():
    """Chạy toàn bộ pipeline"""
    print("=" * 60)
    print("🚀 BẮT ĐẦU PIPELINE XỬ LÝ DỮ LIỆU VÀ AI")
    print("=" * 60)
    
    try:
        # Bước 1: Khởi tạo database
        print("\n📊 Bước 1: Khởi tạo database...")
        init_database()
        
        # Bước 2: Xử lý dữ liệu
        print("\n📊 Bước 2: Xử lý và làm sạch dữ liệu...")
        process_all_data()
        
        # Bước 3: Feature Engineering
        print("\n📊 Bước 3: Feature Engineering...")
        create_features()
        
        # Bước 4: Huấn luyện mô hình
        print("\n📊 Bước 4: Huấn luyện mô hình AI...")
        model = train_model()
        
        if model is None:
            print("❌ Không thể huấn luyện mô hình. Dừng pipeline.")
            return
        
        # Bước 5: Tạo gợi ý
        print("\n📊 Bước 5: Tạo gợi ý học tập cá nhân hóa...")
        process_all_students()
        
        print("\n" + "=" * 60)
        print("✅ HOÀN THÀNH PIPELINE!")
        print("=" * 60)
        print("\n📁 Các file kết quả đã được lưu trong thư mục data/output/")
        print("💡 Bạn có thể chạy web app để xem kết quả:")
        print("   python web/app.py")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong pipeline: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    run_full_pipeline()

