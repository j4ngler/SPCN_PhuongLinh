# 📚 Nền tảng Học tập Cá nhân hóa (Personalized Learning Platform)

## 🎯 Giới thiệu

Dự án xây dựng một nền tảng thông minh giúp phân tích kết quả học tập của sinh viên và đưa ra gợi ý học tập cá nhân hóa theo năng lực, sở thích và định hướng nghề nghiệp.

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8+
- pip

### Bước 1: Clone repository
```bash
cd SPCN_PhuongLinh
```

### Bước 2: Tạo virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r web/requirements.txt
```

### Bước 4: Chuẩn bị dữ liệu
Đặt các file CSV vào thư mục `data/input/`:
- `subjects.csv`
- `grades.csv`
- `teacher_feedback.csv`
- `career_path.csv`
- `student_profile.csv`

### Bước 5: Chạy pipeline
```bash
python scripts/run_pipeline.py
```

### Bước 6: Khởi động web app
```bash
python web/app.py
```

Truy cập: http://localhost:5000

## 📁 Cấu trúc Dự án

Xem [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) để biết chi tiết.

## 🔧 Sử dụng

### API Endpoints

#### GET/POST `/recommend`
Trả về gợi ý học tập cá nhân hóa

**Request (POST):**
```json
{
  "student_id": "SV001",
  "top_n": 10
}
```

**Response:**
```json
{
  "student_id": "SV001",
  "recommendations": [
    {
      "subject_code": "MATH101",
      "subject_name": "Toán học cơ bản",
      "ai_score": 0.85,
      "priority": 1,
      "reason": "Môn học phù hợp với năng lực..."
    }
  ],
  "count": 10
}
```

#### GET `/dashboard/<student_id>`
Hiển thị dashboard học tập của sinh viên

#### GET `/api/ai_scores/<student_id>`
Trả về AI Scores của sinh viên

#### GET `/api/abilities/<student_id>`
Trả về bảng tổng hợp năng lực học tập

## 📊 Quy trình Xử lý

1. **Xử lý dữ liệu** (`data_processor.py`): Làm sạch và chuẩn hóa dữ liệu
2. **Feature Engineering** (`feature_engineering.py`): Mã hóa đặc trưng
3. **Huấn luyện mô hình** (`ai_model.py`): RandomForestRegressor
4. **Tạo gợi ý** (`ai_recommender.py`): Tính AI Score và đưa ra gợi ý

## 🎓 Lộ trình Học tập

Xem [GIAO_AN_DAY_HOC.md](./GIAO_AN_DAY_HOC.md) để biết chi tiết 10 buổi học.

## 📝 License

Dự án này được phát triển cho mục đích giáo dục.

