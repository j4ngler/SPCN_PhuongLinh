# 📚 Nền tảng Học tập Cá nhân hóa (Personalized Learning Platform)

## 🎯 Mục tiêu

Xây dựng một nền tảng thông minh giúp phân tích kết quả học tập của học sinh và đưa ra gợi ý học tập cá nhân hóa theo năng lực, sở thích và định hướng nghề nghiệp.

Hệ thống hỗ trợ học sinh hiểu rõ điểm mạnh – yếu của bản thân, đồng thời giúp giáo viên và phụ huynh theo dõi tiến độ học tập một cách trực quan.

## 🚀 Bắt đầu nhanh

### 1. Cài đặt môi trường
```bash
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r web/requirements.txt
```

### 2. Chuẩn bị dữ liệu
Đặt các file CSV vào `data/input/`:
- `subjects.csv` - Danh sách môn học
- `grades.csv` - Điểm số
- `teacher_feedback.csv` - Nhận xét giáo viên
- `career_path.csv` - Định hướng nghề nghiệp
- `student_profile.csv` - Hồ sơ sinh viên

### 3. Chạy pipeline
```bash
python scripts/run_pipeline.py
```

### 4. Khởi động web app
```bash
python web/app.py
```

Truy cập: http://localhost:5000

## 📁 Cấu trúc Dự án

```
SPCN_PhuongLinh/
├── scripts/          # Scripts Python xử lý dữ liệu và AI
├── data/            # Dữ liệu input/output
├── config/          # File cấu hình
├── docs/            # Tài liệu
├── web/             # Ứng dụng web Flask
└── models/          # Mô hình AI đã huấn luyện
```

Xem chi tiết tại [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)

## 🔧 Các Script chính

- `scripts/data_processor.py` - Xử lý và làm sạch dữ liệu
- `scripts/feature_engineering.py` - Mã hóa đặc trưng
- `scripts/ai_model.py` - Huấn luyện RandomForestRegressor
- `scripts/ai_recommender.py` - Tạo gợi ý học tập
- `scripts/run_pipeline.py` - Chạy toàn bộ pipeline

## 📊 API Endpoints

- `GET/POST /recommend` - Gợi ý học tập cá nhân hóa
- `GET /dashboard/<student_id>` - Dashboard học tập
- `GET /api/ai_scores/<student_id>` - AI Scores
- `GET /api/abilities/<student_id>` - Tổng hợp năng lực

## 🗓️ Lộ trình Học tập (10 buổi)

1. Giới thiệu đề tài, cài đặt môi trường
2. Ôn Python cơ bản: biến, hàm, đọc ghi file CSV
3. Tạo cơ sở dữ liệu `student_learning.db`
4. Làm sạch và mã hóa dữ liệu (Feature Engineering)
5. Huấn luyện mô hình AI (`RandomForestRegressor`)
6. Tạo API Flask `/recommend`
7. Thiết kế Dashboard hiển thị kết quả
8. Thêm chức năng đăng nhập
9. Tối ưu và đánh giá mô hình AI (≥80%)
10. Demo & Tổng kết

Xem chi tiết tại [docs/GIAO_AN_DAY_HOC.md](./docs/GIAO_AN_DAY_HOC.md)

## 💡 Tính năng chính

- ✅ Phân tích kết quả học tập và tính AI Score
- ✅ Gợi ý môn học/kỹ năng phù hợp
- ✅ Dashboard hiển thị năng lực và tiến độ
- ✅ Hỗ trợ giáo viên và phụ huynh theo dõi
- ✅ API RESTful cho tích hợp

## 📝 License

Dự án này được phát triển cho mục đích giáo dục.

## 👥 Tác giả

SPCN Phương Linh

