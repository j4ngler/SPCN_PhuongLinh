# 📚 GIÁO ÁN DẠY HỌC
## Nền tảng Học tập Cá nhân hóa (Personalized Learning Platform)
### Dành cho học sinh cấp 3

---

## 📋 THÔNG TIN CHUNG

- **Đối tượng:** Học sinh cấp 3 (lớp 10, 11, 12)
- **Thời lượng:** 10 buổi học (mỗi buổi 90-120 phút)
- **Mục tiêu:** Xây dựng nền tảng web sử dụng AI để gợi ý học tập cá nhân hóa
- **Ngôn ngữ:** Python 3.12
- **Công nghệ:** Flask, Pandas, Scikit-learn, SQLite, HTML/CSS/JavaScript

---

## 🎯 MỤC TIÊU TỔNG QUAN

Sau khi hoàn thành khóa học, học sinh có thể:
1. ✅ Hiểu và sử dụng Python để xử lý dữ liệu CSV
2. ✅ Tạo và quản lý cơ sở dữ liệu SQLite
3. ✅ Áp dụng Machine Learning (RandomForest) để dự đoán
4. ✅ Xây dựng ứng dụng web với Flask
5. ✅ Tạo giao diện Dashboard hiển thị dữ liệu
6. ✅ Hiểu cách AI có thể hỗ trợ giáo dục

---

## 📅 CHI TIẾT TỪNG BUỔI HỌC

### **BUỔI 1: Giới thiệu dự án & Cài đặt môi trường**

#### Mục tiêu
- Hiểu về dự án và mục tiêu
- Cài đặt đầy đủ môi trường lập trình

#### Nội dung

**1. Giới thiệu dự án (20 phút)**
- Trình bày ý tưởng: Nền tảng học tập cá nhân hóa
- Giải thích AI Score là gì
- Demo sơ bộ kết quả cuối cùng
- Hỏi đáp về dự án

**2. Cài đặt Python (30 phút)**
- Kiểm tra Python đã cài chưa: `python --version`
- Hướng dẫn cài Python 3.12 (nếu chưa có)
- Giải thích về virtual environment (venv)
- Tạo venv: `python -m venv venv`
- Kích hoạt venv:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`

**3. Cài đặt VS Code và extensions (20 phút)**
- Cài đặt VS Code
- Cài extensions: Python, Pylance
- Tạo workspace cho dự án

**4. Cài đặt thư viện (20 phút)**
- Giải thích về pip và requirements.txt
- Cài đặt: `pip install -r web/requirements.txt`
- Kiểm tra: `pip list`

#### Bài tập về nhà
- Đọc file README.md
- Xem cấu trúc dự án
- Chuẩn bị dữ liệu mẫu (nếu có)

#### Tài liệu tham khảo
- [Python Official Docs](https://docs.python.org/3/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

---

### **BUỔI 2: Ôn Python cơ bản & Xử lý dữ liệu CSV**

#### Mục tiêu
- Nắm vững Python cơ bản
- Đọc và ghi file CSV
- Xử lý dữ liệu với Pandas

#### Nội dung

**1. Ôn Python cơ bản (30 phút)**
- Biến, kiểu dữ liệu (int, float, string, list, dict)
- Vòng lặp (for, while)
- Điều kiện (if/else)
- Hàm (def)
- Ví dụ thực hành ngay

**2. Làm việc với file CSV (40 phút)**
- Giải thích CSV là gì
- Đọc CSV với Pandas: `pd.read_csv()`
- Xem dữ liệu: `df.head()`, `df.info()`, `df.describe()`
- Lọc dữ liệu: `df[df['column'] == value]`
- Ghi CSV: `df.to_csv()`

**3. Thực hành với dữ liệu điểm (30 phút)**
- Đọc file `grades.csv`
- Tính điểm trung bình của từng học sinh
- Tìm học sinh có điểm cao nhất
- Lưu kết quả vào file mới

#### Bài tập thực hành
```python
# Bài tập 1: Đọc và hiển thị 5 dòng đầu của grades.csv
import pandas as pd
df = pd.read_csv('data/input/grades.csv')
print(df.head())

# Bài tập 2: Tính điểm trung bình của học sinh HS001
hs001_grades = df[df['student_id'] == 'HS001']
avg = hs001_grades['grade_score'].mean()
print(f"Điểm trung bình HS001: {avg}")

# Bài tập 3: Tìm học sinh có điểm cao nhất môn MATH101
math101 = df[df['subject_code'] == 'MATH101']
top_student = math101.loc[math101['grade_score'].idxmax()]
print(f"Học sinh điểm cao nhất: {top_student['student_id']}")
```

#### Bài tập về nhà
- Viết script tính điểm trung bình tất cả học sinh
- Tạo file CSV mới chứa kết quả

---

### **BUỔI 3: Tạo cơ sở dữ liệu SQLite**

#### Mục tiêu
- Hiểu về cơ sở dữ liệu
- Tạo database SQLite
- Tạo các bảng và thêm dữ liệu

#### Nội dung

**1. Giới thiệu về Database (20 phút)**
- Database là gì? Tại sao cần database?
- SQLite là gì? (database nhẹ, không cần server)
- So sánh CSV vs Database

**2. Tạo database và bảng (40 phút)**
- Kết nối SQLite: `sqlite3.connect()`
- Tạo bảng với CREATE TABLE
- Các kiểu dữ liệu: TEXT, INTEGER, REAL
- Khóa chính (PRIMARY KEY)
- Khóa ngoại (FOREIGN KEY)

**3. Thêm dữ liệu vào database (30 phút)**
- INSERT INTO
- Đọc từ CSV và insert vào database
- Kiểm tra dữ liệu: SELECT

#### Thực hành
```python
import sqlite3
import pandas as pd

# Tạo database
conn = sqlite3.connect('student_learning.db')
cursor = conn.cursor()

# Tạo bảng subjects
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT UNIQUE NOT NULL,
        subject_name TEXT NOT NULL,
        category TEXT
    )
''')

# Đọc từ CSV và insert
subjects_df = pd.read_csv('data/input/subjects.csv')
for _, row in subjects_df.iterrows():
    cursor.execute('''
        INSERT INTO subjects (subject_code, subject_name, category)
        VALUES (?, ?, ?)
    ''', (row['subject_code'], row['subject_name'], row['category']))

conn.commit()
conn.close()
```

#### Bài tập về nhà
- Tạo bảng `grades` và insert dữ liệu từ CSV
- Viết query tìm học sinh có điểm cao nhất

---

### **BUỔI 4: Làm sạch và mã hóa dữ liệu (Feature Engineering)**

#### Mục tiêu
- Hiểu về Feature Engineering
- Làm sạch dữ liệu
- Mã hóa dữ liệu phân loại

#### Nội dung

**1. Làm sạch dữ liệu (30 phút)**
- Xử lý giá trị thiếu (missing values)
- Loại bỏ dữ liệu trùng lặp
- Chuẩn hóa định dạng
- Xử lý giá trị ngoại lai (outliers)

**2. Feature Engineering (40 phút)**
- Label Encoding: Chuyển text thành số
- StandardScaler: Chuẩn hóa dữ liệu số
- Tạo đặc trưng mới:
  - Điểm trung bình của học sinh
  - Độ khó môn học (dạng số)
  - Tỷ lệ hoàn thành tổng thể

**3. Thực hành với script (30 phút)**
- Chạy `data_processor.py`
- Chạy `feature_engineering.py`
- Kiểm tra file `features.csv` đã tạo

#### Thực hành
```python
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

# Đọc dữ liệu
df = pd.read_csv('data/output/grades_cleaned.csv')

# Mã hóa subject_code
le = LabelEncoder()
df['subject_code_encoded'] = le.fit_transform(df['subject_code'])

# Chuẩn hóa điểm số
scaler = StandardScaler()
df['grade_score_normalized'] = scaler.fit_transform(df[['grade_score']])

# Tạo đặc trưng mới: điểm trung bình của học sinh
df['student_avg'] = df.groupby('student_id')['grade_score'].transform('mean')

# Lưu file
df.to_csv('data/output/features.csv', index=False)
```

#### Bài tập về nhà
- Thử tạo thêm đặc trưng mới
- Kiểm tra file features.csv có đúng không

---

### **BUỔI 5: Huấn luyện mô hình AI (RandomForestRegressor)**

#### Mục tiêu
- Hiểu về Machine Learning cơ bản
- Huấn luyện mô hình RandomForest
- Đánh giá mô hình

#### Nội dung

**1. Giới thiệu Machine Learning (20 phút)**
- ML là gì? Tại sao cần ML?
- Supervised Learning vs Unsupervised Learning
- Regression vs Classification
- RandomForest là gì? (rừng cây quyết định)

**2. Chuẩn bị dữ liệu (20 phút)**
- Chia dữ liệu: Train (80%) và Test (20%)
- Tách features (X) và target (y)
- Giải thích AI Score là gì

**3. Huấn luyện mô hình (30 phút)**
- Import RandomForestRegressor
- Tạo và train model
- Dự đoán trên test set
- Đánh giá: R² Score, MAE, RMSE

**4. Lưu mô hình (20 phút)**
- Lưu model với joblib
- Lưu thông tin features
- Test load lại model

#### Thực hành
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import pandas as pd

# Đọc features
df = pd.read_csv('data/output/features.csv')

# Chọn features và target
feature_cols = ['grade_score', 'attendance_rate', 'homework_completion']
X = df[feature_cols]
y = df['ai_score']  # Target đã được tạo sẵn

# Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Huấn luyện
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Đánh giá
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"R² Score: {r2:.4f}")
print(f"MAE: {mae:.4f}")

# Lưu model
joblib.dump(model, 'models/ai_model.pkl')
```

#### Bài tập về nhà
- Thử thay đổi tham số n_estimators
- Xem độ chính xác thay đổi như thế nào

---

### **BUỔI 6: Tạo API Flask - Endpoint /recommend**

#### Mục tiêu
- Hiểu về Web API
- Tạo Flask app
- Tạo endpoint trả về JSON

#### Nội dung

**1. Giới thiệu Flask (20 phút)**
- Flask là gì?
- Web app vs API
- Request và Response

**2. Tạo Flask app cơ bản (30 phút)**
- Tạo file `app.py`
- Route cơ bản: `@app.route('/')`
- Chạy server: `app.run()`
- Truy cập `http://localhost:5000`

**3. Tạo endpoint /recommend (40 phút)**
- Route GET: Hiển thị form
- Route POST: Nhận dữ liệu, trả JSON
- Sử dụng mô hình đã train
- Trả về gợi ý học tập

#### Thực hành
```python
from flask import Flask, request, jsonify, render_template
from ai_recommender import generate_recommendations

app = Flask(__name__)

@app.route('/')
def index():
    return "Chào mừng đến với Nền tảng Học tập Cá nhân hóa!"

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        top_n = int(request.form.get('top_n', 10))
        
        recommendations = generate_recommendations(student_id, top_n)
        
        return jsonify({
            'student_id': student_id,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    return render_template('recommend.html')

if __name__ == '__main__':
    app.run(debug=True)
```

#### Bài tập về nhà
- Tạo thêm endpoint `/api/ai_scores/<student_id>`
- Test API với Postman hoặc trình duyệt

---

### **BUỔI 7: Thiết kế Dashboard hiển thị kết quả**

#### Mục tiêu
- Tạo giao diện web đẹp
- Hiển thị dữ liệu từ API
- Sử dụng HTML/CSS/JavaScript

#### Nội dung

**1. HTML cơ bản (20 phút)**
- Cấu trúc HTML
- Thẻ div, table, form
- Jinja2 template (Flask)

**2. CSS styling (30 phút)**
- CSS cơ bản
- Flexbox/Grid layout
- Màu sắc, font chữ
- Responsive design

**3. Tạo Dashboard (40 phút)**
- Hiển thị thông tin học sinh
- Bảng AI Scores
- Cards hiển thị gợi ý
- Biểu đồ (nếu có thời gian)

#### Thực hành
```html
<!-- dashboard.html -->
{% extends "base.html" %}

{% block content %}
<div class="dashboard">
    <h1>Dashboard - {{ student_id }}</h1>
    
    <div class="stats">
        <div class="stat-card">
            <h3>AI Score Trung bình</h3>
            <p>{{ avg_score }}%</p>
        </div>
    </div>
    
    <div class="recommendations">
        <h2>Gợi ý Học tập</h2>
        {% for rec in recommendations %}
        <div class="recommendation-card">
            <h3>{{ rec.subject_name }}</h3>
            <p>AI Score: {{ rec.ai_score }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

#### Bài tập về nhà
- Tạo thêm trang hiển thị điểm số thực tế
- Thêm biểu đồ (Chart.js)

---

### **BUỔI 8: Chức năng Đăng nhập & Phân quyền**

#### Mục tiêu
- Tạo hệ thống đăng nhập
- Phân quyền người dùng
- Bảo mật mật khẩu

#### Nội dung

**1. Tạo bảng users (20 phút)**
- Thiết kế schema
- Tạo bảng trong database
- Hash mật khẩu với werkzeug

**2. Đăng ký tài khoản (30 phút)**
- Form đăng ký
- Validation dữ liệu
- Lưu vào database
- Tự động tạo student_id nếu cần

**3. Đăng nhập (30 phút)**
- Form đăng nhập
- Xác thực mật khẩu
- Session management
- Redirect theo role

**4. Phân quyền (10 phút)**
- Học sinh: Xem dữ liệu của mình
- Phụ huynh: Xem dữ liệu của con

#### Thực hành
```python
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

# Đăng ký
password_hash = generate_password_hash('matkhau123')
cursor.execute('''
    INSERT INTO users (username, password_hash, role, student_id)
    VALUES (?, ?, ?, ?)
''', ('hs001', password_hash, 'student', 'HS001'))

# Đăng nhập
user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
if user and check_password_hash(user['password_hash'], password):
    session['user_id'] = user['user_id']
    session['role'] = user['role']
```

#### Bài tập về nhà
- Tạo tài khoản cho 5 học sinh
- Test đăng nhập và phân quyền

---

### **BUỔI 9: Tối ưu và Đánh giá mô hình AI**

#### Mục tiêu
- Hiểu cách cải thiện mô hình
- Đánh giá độ chính xác
- Tối ưu tham số

#### Nội dung

**1. Đánh giá mô hình (30 phút)**
- R² Score: Độ phù hợp
- MAE: Sai số trung bình
- RMSE: Sai số bình phương trung bình
- Mục tiêu: R² ≥ 0.80

**2. Tối ưu tham số (40 phút)**
- Thử các giá trị khác nhau:
  - n_estimators: 50, 100, 200
  - max_depth: 5, 10, 20
  - min_samples_split: 2, 5, 10
- So sánh kết quả

**3. Cải thiện dữ liệu (20 phút)**
- Thêm đặc trưng mới
- Xử lý dữ liệu tốt hơn
- Kiểm tra lại độ chính xác

#### Thực hành
```python
from sklearn.model_selection import GridSearchCV

# Tìm tham số tốt nhất
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestRegressor(),
    param_grid,
    cv=5,
    scoring='r2'
)

grid_search.fit(X_train, y_train)
print(f"Tham số tốt nhất: {grid_search.best_params_}")
print(f"Độ chính xác tốt nhất: {grid_search.best_score_}")
```

#### Bài tập về nhà
- Tìm tham số tốt nhất cho mô hình
- Đạt được R² ≥ 0.80

---

### **BUỔI 10: Demo & Tổng kết**

#### Mục tiêu
- Trình bày dự án hoàn chỉnh
- Tổng kết kiến thức
- Định hướng phát triển

#### Nội dung

**1. Demo dự án (40 phút)**
- Mỗi học sinh trình bày 5-10 phút
- Demo các chức năng:
  - Đăng ký/Đăng nhập
  - Dashboard hiển thị kết quả
  - API trả về gợi ý
  - Nhập dữ liệu mới
- Nhận xét và góp ý

**2. Tổng kết kiến thức (30 phút)**
- Ôn lại các khái niệm:
  - Python, Pandas
  - SQLite, Database
  - Machine Learning
  - Flask, Web API
  - HTML/CSS/JavaScript
- Q&A

**3. Định hướng phát triển (20 phút)**
- Có thể mở rộng thêm:
  - Thêm biểu đồ tiến độ
  - Gửi email thông báo
  - Mobile app
  - Tích hợp với hệ thống điểm của trường
- Tài liệu tham khảo

#### Checklist hoàn thành
- [ ] Database có đầy đủ dữ liệu
- [ ] Mô hình AI đạt R² ≥ 0.80
- [ ] Web app chạy ổn định
- [ ] Dashboard hiển thị đúng
- [ ] Đăng nhập/Đăng ký hoạt động
- [ ] API trả về gợi ý chính xác

---

## 📚 TÀI LIỆU THAM KHẢO

### Python & Pandas
- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Machine Learning
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [RandomForest Explained](https://scikit-learn.org/stable/modules/ensemble.html#forest)

### Flask & Web Development
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTML/CSS Tutorial](https://www.w3schools.com/)

### SQLite
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

---

## 🎓 ĐÁNH GIÁ

### Điểm số
- **Thực hành trên lớp:** 30%
- **Bài tập về nhà:** 30%
- **Dự án cuối khóa:** 40%

### Tiêu chí đánh giá dự án
1. **Chức năng (40%)**
   - Đăng ký/Đăng nhập hoạt động
   - Dashboard hiển thị đúng
   - API trả về gợi ý chính xác

2. **Code quality (30%)**
   - Code sạch, có comment
   - Tổ chức file hợp lý
   - Xử lý lỗi tốt

3. **Giao diện (20%)**
   - UI đẹp, dễ sử dụng
   - Responsive design

4. **Thuyết trình (10%)**
   - Trình bày rõ ràng
   - Trả lời câu hỏi tốt

---

## 💡 LƯU Ý CHO GIÁO VIÊN

1. **Điều chỉnh tốc độ:** Tùy trình độ học sinh, có thể kéo dài hoặc rút ngắn từng buổi
2. **Thực hành nhiều:** Cho học sinh code ngay, không chỉ nghe lý thuyết
3. **Hỗ trợ kịp thời:** Giúp học sinh debug lỗi ngay khi gặp
4. **Khuyến khích:** Khen ngợi khi học sinh làm được, động viên khi gặp khó khăn
5. **Tài liệu:** Cung cấp code mẫu và tài liệu tham khảo

---

## 📝 GHI CHÚ

- Giáo án này có thể điều chỉnh linh hoạt theo nhu cầu thực tế
- Khuyến khích học sinh tự tìm hiểu và mở rộng dự án
- Tạo môi trường học tập tích cực, vui vẻ

---

**Chúc các em học tốt và hoàn thành dự án thành công! 🎉**

