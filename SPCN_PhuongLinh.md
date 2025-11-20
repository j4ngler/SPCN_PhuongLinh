# 📚 Dự án: Nền tảng Học tập Cá nhân hóa (Personalized Learning Platform)

## 🎯 Mục tiêu
Xây dựng một nền tảng thông minh giúp phân tích kết quả học tập của học sinh cấp 3 và đưa ra gợi ý học tập cá nhân hóa theo năng lực, sở thích và định hướng nghề nghiệp.  
Hệ thống hỗ trợ học sinh hiểu rõ điểm mạnh – yếu của bản thân, đồng thời giúp phụ huynh theo dõi tiến độ học tập một cách trực quan.

---

## 🧩 Thành phần chính

- **Chức năng:**  
  Thu thập thông tin từ danh sách môn học, lịch sử điểm, nhận xét học tập, và định hướng nghề nghiệp của học sinh cấp 3.

- **Các công việc tiền xử lý:**  
  Chuẩn hóa, làm sạch và mã hóa đặc trưng từ các bảng dữ liệu:
  - `subjects.csv`
  - `grades.csv`
  - `teacher_feedback.csv`
  - `career_path.csv`
  - `student_profile.csv`

- **Mô hình AI (RandomForestRegressor):**
  - Tính điểm phù hợp (**AI Score**) giữa học sinh và từng môn học hoặc lĩnh vực kỹ năng.  
  - Dự đoán xu hướng học tập, gợi ý kỹ năng nên rèn luyện hoặc ngành nên theo đuổi.

- **Dashboard học tập:**
  - Hiển thị kết quả học tập, biểu đồ năng lực, và gợi ý học tập cá nhân.  
  - Cho phép học sinh và phụ huynh xem kết quả, nhận phản hồi và tinh chỉnh mục tiêu học.

- **Đầu ra hệ thống:**
  - Bảng tổng hợp năng lực học tập cá nhân  
  - Gợi ý môn học/kỹ năng phù hợp  
  - Biểu đồ tiến bộ theo thời gian  

---

## 🗓️ Lộ trình thực hiện đề tài

| Buổi | Nội dung chính | Kết quả mong đợi |
|------|----------------|------------------|
| 1 | Giới thiệu đề tài, cài đặt môi trường (Python, VS Code, pip, venv) | Hoàn thành môi trường lập trình |
| 2 | Ôn Python cơ bản: biến, hàm, đọc ghi file CSV | Xử lý được dữ liệu điểm học tập |
| 3 | Tạo cơ sở dữ liệu `student_learning.db` và các bảng `subjects`, `grades`, `feedback` | CSDL học tập có dữ liệu mẫu |
| 4 | Làm sạch và mã hóa dữ liệu (Feature Engineering) | Sinh file `features.csv` |
| 5 | Huấn luyện mô hình AI (`RandomForestRegressor`) | Dự đoán được điểm phù hợp `ai_score` |
| 6 | Tạo API Flask `/recommend` để trả về gợi ý học tập | API chạy ổn định, trả dữ liệu JSON |
| 7 | Thiết kế Dashboard hiển thị kết quả và biểu đồ tiến độ | Giao diện hiển thị gợi ý học tập |
| 8 | Thêm chức năng đăng nhập học sinh – giáo viên | Quản lý người dùng cơ bản |
| 9 | Tối ưu và đánh giá mô hình AI | Cải thiện độ chính xác ≥80% |
| 10 | Demo & Tổng kết | Nền tảng hoạt động, có gợi ý học tập cá nhân hóa |

---

### 💡 Tóm tắt
Dự án giúp học sinh cấp 3 nhận được gợi ý học tập phù hợp với năng lực, tạo cầu nối giữa AI và giáo dục, hướng tới việc cá nhân hóa quá trình học tập trong môi trường số hiện đại.

