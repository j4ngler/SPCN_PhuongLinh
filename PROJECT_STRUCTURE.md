# 📁 Cấu Trúc Dự Án SPCN_PhuongLinh

## 🗂️ Tổng Quan Cấu Trúc

```
SPCN_PhuongLinh/
├── scripts/              # Tất cả các script Python
│   ├── data_processor.py        # Xử lý và làm sạch dữ liệu CSV
│   ├── feature_engineering.py   # Mã hóa đặc trưng (Feature Engineering)
│   ├── ai_model.py              # Huấn luyện RandomForestRegressor
│   ├── ai_score_calculator.py   # Tính điểm phù hợp (AI Score)
│   ├── ai_recommender.py        # Gợi ý học tập cá nhân hóa
│   ├── database_manager.py      # Quản lý SQLite database
│   ├── run_pipeline.py          # Pipeline chạy toàn bộ quy trình
│   └── ...
│
├── data/                 # Dữ liệu
│   ├── input/           # Dữ liệu đầu vào (CSV gốc)
│   │   ├── subjects.csv
│   │   ├── grades.csv
│   │   ├── teacher_feedback.csv
│   │   ├── career_path.csv
│   │   └── student_profile.csv
│   │
│   └── output/          # Dữ liệu đã xử lý
│       ├── features.csv
│       ├── ai_scores.csv
│       ├── recommendations.csv
│       ├── student_abilities.csv
│       └── learning_progress.csv
│
├── config/              # File cấu hình
│   ├── model_config.json
│   └── learning_paths.json
│
├── docs/                # Tài liệu
│   ├── README.md
│   ├── PIPELINE_HUONG_DAN.md
│   ├── GIAO_AN_DAY_HOC.md
│   └── ...
│
├── web/                 # Ứng dụng web Flask
│   ├── app.py           # Backend chính với API /recommend
│   ├── auth.py         # Module xác thực và phân quyền (HocSinh, PhuHuynh)
│   ├── templates/      # HTML templates
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── recommend.html
│   │   ├── dashboard.html
│   │   └── ...
│   ├── static/         # CSS, JavaScript, images
│   └── student_learning.db  # Database SQLite
│
└── [Root files]         # File ở thư mục gốc
    ├── .gitignore
    ├── PROJECT_STRUCTURE.md
    └── SPCN_PhuongLinh.md
```

## 📝 Mô Tả Các Thư Mục

### `scripts/`
Chứa tất cả các script Python xử lý dữ liệu, AI, và phân tích:
- **Xử lý dữ liệu**: `data_processor.py` (Làm sạch dữ liệu)
- **Feature Engineering**: `feature_engineering.py` (Mã hóa đặc trưng → Đặc trưng học tập)
- **AI/ML**: 
  - `ai_model.py` (Huấn luyện RandomForestRegressor → Dự đoán AI Score)
  - `ai_score_calculator.py` (Tính điểm phù hợp AI Score)
  - `ai_recommender.py` (Tạo danh sách gợi ý)
- **Database**: `database_manager.py`
- **Pipeline**: `run_pipeline.py`

**Cách chạy**: Từ thư mục gốc dự án:
```bash
python scripts/data_processor.py
python scripts/ai_model.py
python scripts/run_pipeline.py
```

### `data/input/`
Chứa dữ liệu đầu vào gốc (file CSV):
- `subjects.csv`: Danh sách môn học
- `grades.csv`: Lịch sử điểm số
- `teacher_feedback.csv`: Nhận xét từ giáo viên
- `career_path.csv`: Định hướng nghề nghiệp
- `student_profile.csv`: Thông tin hồ sơ sinh viên

### `data/output/`
Chứa tất cả dữ liệu đã xử lý:
- `features.csv`: Đặc trưng đã mã hóa
- `ai_scores.csv`: Điểm phù hợp AI Score cho từng sinh viên-môn học
- `recommendations.csv`: Gợi ý học tập cá nhân hóa
- `student_abilities.csv`: Bảng tổng hợp năng lực học tập
- `learning_progress.csv`: Tiến độ học tập theo thời gian

### `config/`
Chứa file cấu hình hệ thống:
- `model_config.json`: Cấu hình mô hình AI (RandomForestRegressor)
- `learning_paths.json`: Định nghĩa các lộ trình học tập

### `docs/`
Chứa tất cả tài liệu:
- README.md: Hướng dẫn sử dụng
- PIPELINE_HUONG_DAN.md: Hướng dẫn chi tiết pipeline
- GIAO_AN_DAY_HOC.md: Giáo án giảng dạy theo 10 buổi
- Slide, PDF, v.v.

### `web/`
Ứng dụng web Flask:
- `app.py`: Backend chính với API `/recommend` và các route cho 2 loại người dùng
- `auth.py`: Module xác thực và phân quyền (HocSinh, PhuHuynh)
- `templates/`: HTML templates cho Dashboard và các trang
- `static/`: CSS, JavaScript, images
- `student_learning.db`: Database SQLite

**Các API Endpoints:**
- `GET/POST /recommend`: Gợi ý học tập cá nhân hóa
- `GET /dashboard/<student_id>`: Dashboard hiển thị kết quả
- `GET /api/ai_scores/<student_id>`: API trả về AI Scores
- `GET /api/abilities/<student_id>`: API trả về tổng hợp năng lực

## 🎯 Điểm Khác Biệt với SPCN_HaiAnh

**SPCN_HaiAnh**: Tập trung vào **xếp lịch học** (scheduling) với AI gợi ý lớp học phù hợp.

**SPCN_PhuongLinh**: Tập trung vào **cá nhân hóa học tập** (personalized learning):
- Phân tích kết quả học tập và năng lực
- Tính điểm phù hợp (AI Score) giữa sinh viên và môn học/kỹ năng
- Gợi ý lộ trình học tập cá nhân hóa
- Dashboard hiển thị năng lực, điểm mạnh/yếu, và tiến độ
- Hỗ trợ giáo viên và phụ huynh theo dõi tiến độ

## 🔄 Tương Thích Ngược

Các script và web app được thiết kế để:
1. **Tự động tìm file** ở vị trí mới (`data/output/`, `config/`)
2. **Fallback** về vị trí cũ (thư mục gốc) nếu không tìm thấy
3. **Hoạt động** dù chạy từ thư mục gốc hay từ `scripts/`

## 📌 Lưu Ý

- **Scripts** nên chạy từ **thư mục gốc** dự án để đảm bảo đường dẫn đúng
- **Web app** tự động tìm file ở cả vị trí mới và cũ
- **File mới** sẽ được tạo ở `data/output/` hoặc `config/` tùy loại

## 🚀 Cách Sử Dụng

### Chạy từ thư mục gốc:
```bash
# Chạy pipeline hoàn chỉnh
python scripts/run_pipeline.py

# Chạy AI model training
python scripts/ai_model.py

# Chạy AI recommender
python scripts/ai_recommender.py

# Chạy web app
python web/app.py
```

## 🗄️ Database Schema

Database `student_learning.db` chứa các bảng:
- `subjects`: Thông tin môn học
- `grades`: Điểm số của học sinh
- `feedback`: Nhận xét học tập (từ hệ thống hoặc tự đánh giá)
- `student_profiles`: Hồ sơ học sinh
- `ai_scores`: Điểm phù hợp AI Score
- `recommendations`: Gợi ý học tập
- `users`: Người dùng hệ thống (HocSinh, PhuHuynh)

## 👥 Phân quyền Người dùng

Hệ thống hỗ trợ 2 loại người dùng (dành cho học sinh cấp 3):
- **HocSinh (Student)**: Học sinh cấp 3 - Xem kết quả học tập và yêu cầu gợi ý học tập cá nhân hóa
- **PhuHuynh (Parent)**: Phụ huynh - Xem kết quả học tập của con thông qua Dashboard

