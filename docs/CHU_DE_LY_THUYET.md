# 📚 CÁC CHỦ ĐỀ LÝ THUYẾT CÓ THỂ DẠY

## Tài liệu tổng hợp các khái niệm lý thuyết trong dự án Nền tảng Học tập Cá nhân hóa

---

## 🐍 1. PYTHON CƠ BẢN VÀ NÂNG CAO

### 1.1. Cú pháp Python cơ bản
- **Biến và kiểu dữ liệu**: `int`, `float`, `str`, `bool`, `list`, `dict`, `tuple`
- **Toán tử**: số học, so sánh, logic
- **Cấu trúc điều khiển**: `if/elif/else`, `for`, `while`
- **Hàm (Functions)**: định nghĩa, tham số, giá trị trả về
- **Module và Package**: `import`, `from ... import`
- **Xử lý ngoại lệ**: `try/except/finally`

### 1.2. Lập trình hướng đối tượng (OOP)
- **Class và Object**: định nghĩa class, tạo instance
- **Phương thức và thuộc tính**: `self`, `__init__`
- **Kế thừa (Inheritance)**: class con kế thừa class cha
- **Encapsulation**: private, protected, public attributes

### 1.3. Xử lý file và đường dẫn
- **Pathlib**: `Path` object, xử lý đường dẫn cross-platform
- **File I/O**: đọc/ghi file text, CSV
- **Context Manager**: `with` statement
- **Encoding**: UTF-8, xử lý tiếng Việt

### 1.4. Xử lý dữ liệu với Pandas
- **DataFrame**: cấu trúc dữ liệu 2 chiều
- **Series**: cấu trúc dữ liệu 1 chiều
- **Đọc/Ghi CSV**: `pd.read_csv()`, `df.to_csv()`
- **Lọc và truy vấn**: `df[df['col'] == value]`, `df.query()`
- **Nhóm và tổng hợp**: `groupby()`, `agg()`, `transform()`
- **Merge và Join**: `merge()`, `join()`, `concat()`
- **Xử lý dữ liệu thiếu**: `fillna()`, `dropna()`
- **Chuẩn hóa dữ liệu**: `clip()`, `astype()`

---

## 🤖 2. MACHINE LEARNING & AI

### 2.1. Khái niệm cơ bản về Machine Learning
- **Machine Learning là gì?**: học từ dữ liệu, không lập trình cứng
- **Supervised Learning**: học có giám sát (có nhãn)
  - **Regression**: dự đoán giá trị liên tục (AI Score)
  - **Classification**: phân loại (ví dụ: giỏi/khá/trung bình)
- **Unsupervised Learning**: học không giám sát (không có nhãn)
- **Training vs Testing**: chia dữ liệu để đánh giá

### 2.2. Random Forest Regressor
- **Ensemble Learning**: kết hợp nhiều mô hình
- **Decision Tree**: cây quyết định, cách hoạt động
- **Random Forest**: rừng cây quyết định
  - `n_estimators`: số lượng cây
  - `max_depth`: độ sâu tối đa
  - `min_samples_split`: số mẫu tối thiểu để chia nhánh
  - `min_samples_leaf`: số mẫu tối thiểu ở lá
- **Ưu điểm**: chống overfitting, xử lý dữ liệu phức tạp
- **Nhược điểm**: khó giải thích, tốn tài nguyên

### 2.3. Feature Engineering (Kỹ thuật đặc trưng)
- **Feature là gì?**: đặc trưng/đặc điểm của dữ liệu
- **Feature Selection**: chọn đặc trưng quan trọng
- **Feature Creation**: tạo đặc trưng mới từ dữ liệu hiện có
  - Ví dụ: điểm trung bình, tỷ lệ hoàn thành
- **Label Encoding**: chuyển text thành số (0, 1, 2, ...)
- **One-Hot Encoding**: chuyển category thành vector nhị phân
- **StandardScaler**: chuẩn hóa dữ liệu về trung bình 0, độ lệch chuẩn 1
- **Normalization**: chuẩn hóa về khoảng [0, 1]

### 2.4. Đánh giá mô hình (Model Evaluation)
- **Train-Test Split**: chia 80-20 hoặc 70-30
- **R² Score (R-squared)**: hệ số xác định, đo độ phù hợp
  - R² = 1: hoàn hảo
  - R² = 0: bằng với dự đoán trung bình
  - R² < 0: tệ hơn dự đoán trung bình
- **MAE (Mean Absolute Error)**: sai số tuyệt đối trung bình
- **RMSE (Root Mean Squared Error)**: căn bậc hai của sai số bình phương trung bình
- **Overfitting vs Underfitting**: quá khớp vs chưa khớp
- **Cross-Validation**: kiểm tra chéo để đánh giá tốt hơn

### 2.5. AI Score - Khái niệm trong dự án
- **AI Score là gì?**: điểm số phản ánh mức độ phù hợp giữa học sinh và môn học
- **Cách tính**: dựa trên điểm số, tỷ lệ tham gia, hoàn thành bài tập
- **Ứng dụng**: gợi ý môn học phù hợp, lộ trình học tập

---

## 🌐 3. WEB DEVELOPMENT VỚI FLASK

### 3.1. Flask Framework
- **Flask là gì?**: micro web framework cho Python
- **WSGI**: Web Server Gateway Interface
- **Routing**: định tuyến URL đến hàm xử lý
  - `@app.route('/path')`
  - Methods: `GET`, `POST`, `PUT`, `DELETE`
- **Request và Response**: nhận dữ liệu từ client, trả về kết quả
- **Template Engine (Jinja2)**: render HTML động
- **Static Files**: CSS, JavaScript, images

### 3.2. RESTful API
- **API là gì?**: Application Programming Interface
- **REST**: Representational State Transfer
- **HTTP Methods**: GET (đọc), POST (tạo), PUT (cập nhật), DELETE (xóa)
- **JSON**: định dạng trao đổi dữ liệu
- **Endpoint**: điểm cuối của API
  - `/api/recommend`
  - `/api/ai_scores/<student_id>`
  - `/api/run/<task_name>`

### 3.3. Session và Authentication
- **Session**: lưu trữ thông tin người dùng trên server
- **Cookie**: lưu trữ thông tin trên client
- **Authentication**: xác thực người dùng (đăng nhập)
- **Authorization**: phân quyền truy cập
- **Password Hashing**: băm mật khẩu với `werkzeug.security`
  - `generate_password_hash()`: tạo hash
  - `check_password_hash()`: kiểm tra hash

### 3.4. Form Handling
- **HTML Forms**: `<form>`, `<input>`, `<select>`, `<textarea>`
- **Form Validation**: kiểm tra dữ liệu đầu vào
- **CSRF Protection**: bảo vệ chống tấn công CSRF
- **File Upload**: upload file CSV, xử lý `request.files`

---

## 🗄️ 4. DATABASE & SQL

### 4.1. Cơ sở dữ liệu (Database)
- **Database là gì?**: kho lưu trữ dữ liệu có cấu trúc
- **SQLite**: database nhẹ, file-based, không cần server
- **So sánh CSV vs Database**:
  - CSV: đơn giản, dễ đọc, nhưng chậm với dữ liệu lớn
  - Database: nhanh, có cấu trúc, hỗ trợ query phức tạp

### 4.2. SQL (Structured Query Language)
- **CREATE TABLE**: tạo bảng
- **INSERT INTO**: thêm dữ liệu
- **SELECT**: truy vấn dữ liệu
- **UPDATE**: cập nhật dữ liệu
- **DELETE**: xóa dữ liệu
- **WHERE**: điều kiện lọc
- **JOIN**: kết hợp bảng
- **PRIMARY KEY**: khóa chính
- **FOREIGN KEY**: khóa ngoại
- **UNIQUE**: ràng buộc duy nhất
- **NOT NULL**: ràng buộc không null

### 4.3. Database Design
- **Schema**: cấu trúc database
- **Normalization**: chuẩn hóa dữ liệu (1NF, 2NF, 3NF)
- **Relationships**: quan hệ một-nhiều, nhiều-nhiều
- **Index**: chỉ mục để tăng tốc truy vấn

---

## 🎨 5. FRONTEND (HTML/CSS/JavaScript)

### 5.1. HTML (HyperText Markup Language)
- **Cấu trúc HTML**: `<html>`, `<head>`, `<body>`
- **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<footer>`
- **Forms**: `<form>`, `<input>`, `<button>`, `<select>`
- **Tables**: `<table>`, `<tr>`, `<td>`, `<th>`
- **Jinja2 Template**: template engine của Flask
  - `{% extends %}`: kế thừa template
  - `{% block %}`: khối nội dung
  - `{{ variable }}`: hiển thị biến
  - `{% for %}`: vòng lặp
  - `{% if %}`: điều kiện

### 5.2. CSS (Cascading Style Sheets)
- **Selectors**: class, ID, element, pseudo-class
- **Box Model**: margin, border, padding, content
- **Layout**: Flexbox, Grid
- **Responsive Design**: media queries, mobile-first
- **Colors**: hex, rgb, rgba
- **Typography**: font-family, font-size, font-weight
- **Animations**: keyframes, transitions
- **Modern CSS**: CSS Variables, Flexbox, Grid

### 5.3. JavaScript (cơ bản)
- **DOM Manipulation**: thao tác với HTML elements
- **Event Handling**: click, submit, change
- **AJAX/Fetch API**: gửi request không reload trang
- **JSON**: parse và stringify
- **Async/Await**: xử lý bất đồng bộ

---

## 📊 6. DATA PROCESSING & PIPELINE

### 6.1. Data Pipeline (Quy trình xử lý dữ liệu)
- **Pipeline là gì?**: chuỗi các bước xử lý tự động
- **ETL**: Extract (trích xuất), Transform (biến đổi), Load (tải)
- **Workflow**: quy trình từ đầu vào đến đầu ra
  - Input: CSV files
  - Processing: làm sạch, feature engineering
  - Model Training: huấn luyện AI
  - Output: recommendations, AI scores

### 6.2. Data Cleaning (Làm sạch dữ liệu)
- **Missing Values**: giá trị thiếu
  - Xóa: `dropna()`
  - Điền: `fillna()` với giá trị mặc định, trung bình, median
- **Duplicates**: dữ liệu trùng lặp
  - `drop_duplicates()`
- **Outliers**: giá trị ngoại lai
  - Phát hiện: IQR, Z-score
  - Xử lý: loại bỏ hoặc giới hạn
- **Data Type Conversion**: chuyển đổi kiểu dữ liệu
  - `astype()`, `pd.to_numeric()`
- **Data Validation**: kiểm tra tính hợp lệ
  - Range checking: `clip()`
  - Format validation

### 6.3. Data Transformation
- **Aggregation**: tổng hợp dữ liệu
  - `groupby()`, `agg()`, `sum()`, `mean()`, `count()`
- **Pivoting**: xoay dữ liệu
  - `pivot()`, `pivot_table()`
- **Merging**: kết hợp dữ liệu
  - `merge()`, `join()`, `concat()`
- **Feature Creation**: tạo đặc trưng mới
  - Tính toán từ các cột hiện có
  - Ví dụ: điểm trung bình, tỷ lệ hoàn thành

---

## 🔐 7. SECURITY & BEST PRACTICES

### 7.1. Bảo mật Web
- **Password Hashing**: không lưu mật khẩu dạng plain text
- **SQL Injection**: ngăn chặn bằng parameterized queries
- **XSS (Cross-Site Scripting)**: sanitize user input
- **CSRF (Cross-Site Request Forgery)**: token bảo vệ
- **Session Security**: secure, httponly cookies

### 7.2. Best Practices
- **Code Organization**: tổ chức code theo module
- **Error Handling**: xử lý lỗi với try/except
- **Logging**: ghi log để debug
- **Documentation**: comment và docstring
- **Version Control**: Git, GitHub
- **Environment Variables**: lưu cấu hình nhạy cảm
- **Virtual Environment**: cô lập dependencies

---

## 🧪 8. TESTING & DEBUGGING

### 8.1. Testing
- **Unit Testing**: test từng hàm riêng lẻ
- **Integration Testing**: test tích hợp các module
- **Manual Testing**: test thủ công
- **Test Cases**: các trường hợp test

### 8.2. Debugging
- **Print Debugging**: in ra giá trị để kiểm tra
- **Debugger**: breakpoint, step through
- **Error Messages**: đọc và hiểu thông báo lỗi
- **Logging**: ghi log để theo dõi

---

## 📦 9. DEPENDENCY MANAGEMENT

### 9.1. Package Management
- **pip**: Python package installer
- **requirements.txt**: danh sách dependencies
- **Virtual Environment (venv)**: môi trường ảo
  - Tạo: `python -m venv venv`
  - Kích hoạt: `venv\Scripts\activate` (Windows)
  - Cài đặt: `pip install -r requirements.txt`

### 9.2. Các thư viện chính trong dự án
- **Flask**: web framework
- **Pandas**: xử lý dữ liệu
- **Scikit-learn**: machine learning
- **NumPy**: tính toán số học
- **SQLite3**: database (built-in)
- **Joblib**: lưu/tải mô hình ML
- **Werkzeug**: utilities cho Flask (password hashing)

---

## 🎯 10. PROJECT-SPECIFIC CONCEPTS

### 10.1. Personalized Learning Platform
- **Học tập cá nhân hóa**: điều chỉnh nội dung theo từng học sinh
- **AI-driven Recommendations**: gợi ý dựa trên AI
- **Student Profile**: hồ sơ học sinh
- **Career Path**: định hướng nghề nghiệp
- **Learning Path**: lộ trình học tập

### 10.2. System Architecture
- **MVC Pattern**: Model-View-Controller
- **Separation of Concerns**: tách biệt logic
- **Modular Design**: thiết kế module
- **Data Flow**: luồng dữ liệu từ input → processing → output

### 10.3. User Roles
- **Student (Học sinh)**: xem kết quả của mình
- **Parent (Phụ huynh)**: xem kết quả của con
- **Role-based Access Control**: phân quyền theo vai trò

---

## 📚 11. KHUYẾN NGHỊ THỨ TỰ DẠY

### Mức độ cơ bản (Buổi 1-3)
1. Python cơ bản
2. Xử lý file CSV với Pandas
3. SQLite và SQL cơ bản

### Mức độ trung bình (Buổi 4-6)
4. Feature Engineering
5. Machine Learning cơ bản (RandomForest)
6. Flask và Web API

### Mức độ nâng cao (Buổi 7-10)
7. Frontend (HTML/CSS/JavaScript)
8. Authentication và Security
9. Tối ưu mô hình AI
10. Demo và tổng kết

---

## 💡 12. TÀI LIỆU THAM KHẢO

### Python
- [Python Official Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)

### Pandas
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

### Machine Learning
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Introduction to Machine Learning](https://scikit-learn.org/stable/getting_started.html)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Tutorial](https://flask.palletsprojects.com/tutorial/)

### SQLite
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

### HTML/CSS
- [MDN Web Docs](https://developer.mozilla.org/)
- [W3Schools](https://www.w3schools.com/)

---

## 🎓 KẾT LUẬN

Dự án này bao gồm rất nhiều khái niệm lý thuyết từ cơ bản đến nâng cao, phù hợp cho học sinh cấp 3 muốn tìm hiểu về:
- Lập trình Python
- Xử lý dữ liệu
- Machine Learning và AI
- Web Development
- Database

Giáo viên có thể điều chỉnh độ sâu và phạm vi của từng chủ đề tùy theo trình độ và thời gian của học sinh.

---

**Tài liệu này được tạo để hỗ trợ giáo viên trong việc giảng dạy dự án Nền tảng Học tập Cá nhân hóa.**

