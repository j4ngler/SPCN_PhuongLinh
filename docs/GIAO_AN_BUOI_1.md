# 📚 GIÁO ÁN CHI TIẾT - BUỔI 1
## Giới thiệu dự án & Cài đặt môi trường

---

## 📋 THÔNG TIN CHUNG

- **Thời lượng:** 90-120 phút
- **Đối tượng:** Học sinh cấp 3 (lớp 10, 11, 12)
- **Mục tiêu chính:** 
  - Hiểu về dự án Nền tảng Học tập Cá nhân hóa
  - Cài đặt đầy đủ môi trường lập trình Python
  - Sẵn sàng bắt đầu học lập trình

---

## 🎯 MỤC TIÊU HỌC TẬP

Sau buổi học này, học sinh có thể:
1. ✅ Hiểu được dự án là gì và mục tiêu của nó
2. ✅ Giải thích được AI Score là gì
3. ✅ Cài đặt Python 3.12 và virtual environment
4. ✅ Cài đặt VS Code và các extension cần thiết
5. ✅ Cài đặt các thư viện Python từ requirements.txt
6. ✅ Chạy được một script Python đơn giản

---

## 📝 CHUẨN BỊ

### Cho giáo viên:
- [ ] Máy tính có Python 3.12 đã cài
- [ ] VS Code đã cài đặt
- [ ] File `web/requirements.txt` sẵn có
- [ ] Slide trình bày dự án (nếu có)
- [ ] Demo sẵn sàng chạy trên máy giáo viên

### Cho học sinh:
- [ ] Máy tính Windows/Mac/Linux
- [ ] Kết nối Internet
- [ ] Tài khoản GitHub (khuyến khích)

---

## 🕐 PHÂN BỔ THỜI GIAN

| Phần | Thời gian | Mô tả |
|------|-----------|-------|
| **1. Giới thiệu dự án** | 20 phút | Trình bày ý tưởng, demo, Q&A |
| **2. Cài đặt Python** | 30 phút | Kiểm tra, cài đặt, tạo venv |
| **3. Cài đặt VS Code** | 20 phút | Cài VS Code và extensions |
| **4. Cài đặt thư viện** | 20 phút | Cài packages từ requirements.txt |
| **5. Kiểm tra & Thực hành** | 10-30 phút | Test môi trường, chạy script mẫu |
| **Tổng cộng** | **90-120 phút** | |

---

## 📖 NỘI DUNG CHI TIẾT

### **PHẦN 1: Giới thiệu dự án (20 phút)**

#### 1.1. Trình bày ý tưởng (10 phút)

**Giáo viên trình bày:**

> "Chào các em! Hôm nay chúng ta sẽ bắt đầu một dự án rất thú vị: **Nền tảng Học tập Cá nhân hóa** (Personalized Learning Platform).
> 
> **Dự án này là gì?**
> - Một hệ thống web sử dụng AI để phân tích điểm số và thói quen học tập của học sinh
> - Tự động đưa ra gợi ý học tập phù hợp với từng cá nhân
> - Giúp học sinh biết mình nên tập trung vào môn nào, kỹ năng nào
> 
> **Tại sao cần dự án này?**
> - Mỗi học sinh có điểm mạnh/yếu khác nhau
> - AI có thể phân tích dữ liệu nhanh và chính xác hơn
> - Giúp học sinh học tập hiệu quả hơn"

**Slide/Trình chiếu:**
```
┌─────────────────────────────────────────┐
│  NỀN TẢNG HỌC TẬP CÁ NHÂN HÓA          │
│  Personalized Learning Platform         │
├─────────────────────────────────────────┤
│                                         │
│  📊 Phân tích điểm số                  │
│  🤖 AI dự đoán tiềm năng               │
│  📚 Gợi ý môn học phù hợp              │
│  🎯 Lộ trình học tập cá nhân           │
│                                         │
└─────────────────────────────────────────┘
```

#### 1.2. Giải thích AI Score (5 phút)

**Giáo viên giải thích:**

> "**AI Score là gì?**
> 
> AI Score là điểm số từ 0-100 được AI tính toán dựa trên:
> - Điểm số thực tế của học sinh
> - Tỷ lệ tham gia lớp học (attendance)
> - Tỷ lệ hoàn thành bài tập về nhà
> - Phản hồi từ giáo viên
> - Độ khó của môn học
> 
> **Ví dụ:**
> - Học sinh A có điểm Toán 8.5, tham gia đầy đủ, làm bài tập tốt
> → AI Score Toán: 85/100 (Tốt)
> 
> - Học sinh B có điểm Lý 7.0, hay vắng mặt, chưa làm bài tập
> → AI Score Lý: 55/100 (Cần cải thiện)
> 
> **AI Score giúp:**
> - Biết môn nào mình có tiềm năng
> - Biết môn nào cần tập trung cải thiện
> - Nhận gợi ý học tập phù hợp"

**Ví dụ trực quan:**
```
Học sinh: HS001
┌─────────────┬──────────┬──────────────┐
│ Môn học     │ Điểm     │ AI Score     │
├─────────────┼──────────┼──────────────┤
│ Toán        │ 8.5      │ 85/100 ✅    │
│ Lý          │ 7.0      │ 55/100 ⚠️    │
│ Hóa         │ 9.0      │ 90/100 ✅    │
│ Anh         │ 6.5      │ 50/100 ⚠️    │
└─────────────┴──────────┴──────────────┘

→ Gợi ý: Tập trung cải thiện Lý và Anh
```

#### 1.3. Demo sơ bộ (3 phút)

**Giáo viên demo:**
1. Mở trình duyệt, truy cập `http://localhost:5000`
2. Đăng nhập với tài khoản demo
3. Hiển thị Dashboard với:
   - Thông tin học sinh
   - AI Scores theo từng môn
   - Gợi ý học tập
4. Click vào một gợi ý để xem chi tiết

**Lưu ý:** Demo nhanh, không đi sâu vào code

#### 1.4. Hỏi đáp (2 phút)

**Câu hỏi thường gặp:**
- Q: "Em chưa biết gì về AI, có học được không?"
  → A: "Có! Chúng ta sẽ học từ cơ bản, không cần kiến thức trước"

- Q: "Dự án này khó không?"
  → A: "Có thử thách nhưng rất thú vị. Chúng ta sẽ học từng bước một"

- Q: "Cần biết gì trước khi bắt đầu?"
  → A: "Chỉ cần biết sử dụng máy tính cơ bản. Python sẽ học trong khóa này"

---

### **PHẦN 2: Cài đặt Python (30 phút)**

#### 2.1. Kiểm tra Python đã cài chưa (5 phút)

**Hướng dẫn học sinh:**

**Bước 1:** Mở Terminal/Command Prompt/PowerShell

**Windows:**
- Nhấn `Win + R`, gõ `cmd` hoặc `powershell`, Enter
- Hoặc tìm "Command Prompt" trong Start Menu

**Mac:**
- Nhấn `Cmd + Space`, gõ "Terminal", Enter

**Linux:**
- Nhấn `Ctrl + Alt + T`

**Bước 2:** Kiểm tra Python

```bash
python --version
```

**Kết quả mong đợi:**
- ✅ Nếu thấy: `Python 3.12.x` → Đã cài đúng!
- ❌ Nếu thấy: `Python 3.11.x` hoặc thấp hơn → Cần cài Python 3.12
- ❌ Nếu thấy: `'python' is not recognized` → Chưa cài Python

**Lưu ý Windows:**
- Nếu dùng `py` launcher: `py --version`
- Nếu có nhiều phiên bản: `py -3.12 --version`

#### 2.2. Cài đặt Python 3.12 (15 phút - chỉ cho học sinh chưa có)

**Hướng dẫn chi tiết:**

**Windows:**
1. Truy cập: https://www.python.org/downloads/
2. Tải Python 3.12.x (Latest version)
3. Chạy file `.exe` đã tải
4. ⚠️ **QUAN TRỌNG:** Tick vào "Add Python to PATH"
5. Click "Install Now"
6. Đợi cài đặt hoàn tất
7. Kiểm tra lại: `python --version`

**Mac:**
```bash
# Cách 1: Dùng Homebrew (khuyến khích)
brew install python@3.12

# Cách 2: Tải từ python.org
# Truy cập python.org/downloads, tải file .pkg cho Mac
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-pip
```

**Kiểm tra sau khi cài:**
```bash
python3.12 --version
# Hoặc
python --version
```

#### 2.3. Giải thích về Virtual Environment (5 phút)

**Giáo viên giải thích:**

> "**Virtual Environment (venv) là gì?**
> 
> - Là một môi trường Python riêng biệt cho từng dự án
> - Giống như một "hộp cát" riêng, không ảnh hưởng đến Python hệ thống
> 
> **Tại sao cần venv?**
> - Mỗi dự án có thể cần phiên bản thư viện khác nhau
> - Tránh xung đột giữa các dự án
> - Dễ quản lý và chia sẻ
> 
> **Ví dụ:**
> - Dự án A cần pandas 1.5.0
> - Dự án B cần pandas 2.0.0
> → Dùng venv để tách biệt"

**Minh họa:**
```
Hệ thống Python
├── venv_project_A/  (pandas 1.5.0)
├── venv_project_B/  (pandas 2.0.0)
└── venv_spcn/       (pandas 2.1.0) ← Dự án của chúng ta
```

#### 2.4. Tạo Virtual Environment (5 phút)

**Hướng dẫn học sinh:**

**Bước 1:** Di chuyển vào thư mục dự án

```bash
# Windows
cd D:\Intern\BkStar\SPCN_PhuongLinh

# Mac/Linux
cd ~/path/to/SPCN_PhuongLinh
```

**Bước 2:** Tạo venv

```bash
python -m venv venv
```

**Giải thích:**
- `python -m venv` → Chạy module venv
- `venv` → Tên thư mục sẽ tạo (có thể đặt tên khác)

**Kết quả:** Sẽ tạo thư mục `venv/` với cấu trúc:
```
venv/
├── Scripts/     (Windows) hoặc bin/ (Mac/Linux)
├── Lib/
└── pyvenv.cfg
```

**Bước 3:** Kích hoạt venv

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Dấu hiệu thành công:**
- Đầu dòng terminal sẽ có `(venv)`:
```
(venv) PS D:\Intern\BkStar\SPCN_PhuongLinh>
```

**Bước 4:** Kiểm tra Python trong venv

```bash
python --version
which python  # Mac/Linux
where python  # Windows
```

**Lưu ý:** Đường dẫn phải trỏ đến `venv/Scripts/python.exe` (Windows) hoặc `venv/bin/python` (Mac/Linux)

**Tắt venv (khi cần):**
```bash
deactivate
```

---

### **PHẦN 3: Cài đặt VS Code và Extensions (20 phút)**

#### 3.1. Cài đặt VS Code (10 phút)

**Hướng dẫn:**

**Bước 1:** Tải VS Code
- Truy cập: https://code.visualstudio.com/
- Tải phiên bản phù hợp với hệ điều hành

**Bước 2:** Cài đặt
- Windows: Chạy file `.exe`, next → next → finish
- Mac: Kéo vào Applications
- Linux: Giải nén và chạy

**Bước 3:** Mở VS Code
- Windows: Tìm "Visual Studio Code" trong Start Menu
- Mac: Mở từ Applications
- Linux: Chạy `code` từ terminal

#### 3.2. Cài đặt Extensions (10 phút)

**Extensions cần thiết:**

1. **Python** (Microsoft)
   - Tìm: `Python` (ID: ms-python.python)
   - Click "Install"
   - Tự động cài Pylance và các tools khác

2. **Pylance** (Microsoft) - Tự động cài cùng Python
   - Hỗ trợ IntelliSense, type checking

3. **Python Indent** (khuyến khích)
   - Tìm: `Python Indent` (ID: KevinRose.vsc-python-indent)
   - Giúp format code Python đúng

**Cách cài:**
1. Mở VS Code
2. Click icon Extensions (hoặc `Ctrl+Shift+X`)
3. Tìm tên extension
4. Click "Install"

**Kiểm tra:**
- Mở một file `.py` bất kỳ
- Nếu thấy syntax highlighting (màu sắc) → Thành công!

#### 3.3. Tạo Workspace (2 phút)

**Hướng dẫn:**

1. Mở VS Code
2. File → Open Folder
3. Chọn thư mục `SPCN_PhuongLinh`
4. File → Save Workspace As...
5. Lưu với tên `SPCN_PhuongLinh.code-workspace`

**Lợi ích:**
- Lưu cấu hình workspace
- Mở lại dễ dàng
- Chia sẻ với người khác

---

### **PHẦN 4: Cài đặt thư viện Python (20 phút)**

#### 4.1. Giải thích về pip và requirements.txt (5 phút)

**Giáo viên giải thích:**

> "**pip là gì?**
> - Package Installer for Python
> - Công cụ để cài đặt thư viện Python
> - Tương tự như App Store cho Python
> 
> **requirements.txt là gì?**
> - File liệt kê tất cả thư viện cần thiết cho dự án
> - Giúp cài đặt nhanh: `pip install -r requirements.txt`
> - Dễ chia sẻ và tái tạo môi trường"

**Ví dụ requirements.txt:**
```txt
flask==3.0.0
pandas==2.1.0
scikit-learn==1.3.0
sqlite3
```

#### 4.2. Kiểm tra pip (2 phút)

**Đảm bảo venv đã được kích hoạt!**

```bash
pip --version
```

**Kết quả mong đợi:**
```
pip 23.x.x from ...\venv\Lib\site-packages\pip (python 3.12)
```

#### 4.3. Cài đặt từ requirements.txt (10 phút)

**Bước 1:** Kiểm tra file requirements.txt

```bash
# Xem nội dung file
cat web/requirements.txt  # Mac/Linux
type web\requirements.txt  # Windows
```

**Bước 2:** Cài đặt

```bash
pip install -r web/requirements.txt
```

**Quá trình cài đặt:**
- Sẽ mất vài phút
- Hiển thị progress bar
- Có thể có cảnh báo (warnings) - không sao

**Lưu ý:**
- Nếu lỗi về quyền: Đảm bảo venv đã được kích hoạt
- Nếu lỗi về network: Kiểm tra kết nối Internet
- Nếu lỗi về phiên bản: Có thể cần cập nhật pip: `pip install --upgrade pip`

#### 4.4. Kiểm tra cài đặt (3 phút)

**Kiểm tra các thư viện quan trọng:**

```bash
# Xem danh sách đã cài
pip list

# Kiểm tra từng thư viện
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import sklearn; print('Scikit-learn:', sklearn.__version__)"
```

**Kết quả mong đợi:**
```
Flask: 3.0.0
Pandas: 2.1.0
Scikit-learn: 1.3.0
```

---

### **PHẦN 5: Kiểm tra & Thực hành (10-30 phút)**

#### 5.1. Tạo script test đơn giản (5 phút)

**Tạo file `test_setup.py`:**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script kiểm tra môi trường đã cài đặt đúng chưa
"""

print("🔍 Kiểm tra môi trường...")
print("-" * 40)

# Kiểm tra Python version
import sys
print(f"✅ Python version: {sys.version}")

# Kiểm tra các thư viện
try:
    import flask
    print(f"✅ Flask: {flask.__version__}")
except ImportError:
    print("❌ Flask chưa được cài đặt")

try:
    import pandas as pd
    print(f"✅ Pandas: {pd.__version__}")
except ImportError:
    print("❌ Pandas chưa được cài đặt")

try:
    import sklearn
    print(f"✅ Scikit-learn: {sklearn.__version__}")
except ImportError:
    print("❌ Scikit-learn chưa được cài đặt")

try:
    import sqlite3
    print(f"✅ SQLite: {sqlite3.sqlite_version}")
except ImportError:
    print("❌ SQLite không có sẵn")

print("-" * 40)
print("🎉 Hoàn tất kiểm tra!")
```

#### 5.2. Chạy script test (3 phút)

**Trong terminal (đã kích hoạt venv):**

```bash
python test_setup.py
```

**Kết quả mong đợi:**
```
🔍 Kiểm tra môi trường...
----------------------------------------
✅ Python version: 3.12.x
✅ Flask: 3.0.0
✅ Pandas: 2.1.0
✅ Scikit-learn: 1.3.0
✅ SQLite: 3.42.0
----------------------------------------
🎉 Hoàn tất kiểm tra!
```

**Nếu có lỗi:**
- Kiểm tra lại venv đã kích hoạt chưa
- Kiểm tra lại `pip install -r web/requirements.txt`

#### 5.3. Thực hành Python cơ bản (10-20 phút - tùy thời gian)

**Tạo file `hello_project.py`:**

```python
# In ra thông điệp chào mừng
print("Chào mừng đến với Nền tảng Học tập Cá nhân hóa!")
print("Dự án: SPCN_PhuongLinh")

# Thử import pandas và đọc file CSV (nếu có)
try:
    import pandas as pd
    print("\n✅ Pandas đã sẵn sàng!")
    
    # Thử đọc một file CSV (nếu có)
    import os
    if os.path.exists('data/input/subjects.csv'):
        df = pd.read_csv('data/input/subjects.csv')
        print(f"✅ Đã đọc file subjects.csv: {len(df)} dòng")
        print(df.head())
    else:
        print("ℹ️  File subjects.csv chưa có (sẽ tạo sau)")
except Exception as e:
    print(f"⚠️  Lỗi: {e}")

print("\n🎯 Môi trường đã sẵn sàng để bắt đầu!")
```

**Chạy:**
```bash
python hello_project.py
```

---

## 📝 BÀI TẬP VỀ NHÀ

### Bài tập bắt buộc:
1. ✅ Đọc file `README.md` trong dự án
2. ✅ Xem cấu trúc thư mục dự án (xem `PROJECT_STRUCTURE.md` nếu có)
3. ✅ Đảm bảo môi trường đã cài đặt đúng:
   - Python 3.12
   - VS Code với extensions
   - Tất cả thư viện từ requirements.txt

### Bài tập khuyến khích:
1. ⭐ Tìm hiểu về Python cơ bản:
   - Biến, kiểu dữ liệu
   - Vòng lặp, điều kiện
   - Hàm
2. ⭐ Xem video hướng dẫn Python cơ bản (nếu chưa biết)
3. ⭐ Chuẩn bị dữ liệu mẫu (nếu có):
   - Điểm số của bản thân
   - Danh sách môn học yêu thích

---

## ✅ CHECKLIST HOÀN THÀNH

Học sinh tự kiểm tra:

- [ ] Đã hiểu dự án là gì
- [ ] Đã cài Python 3.12
- [ ] Đã tạo và kích hoạt virtual environment
- [ ] Đã cài VS Code
- [ ] Đã cài extensions: Python, Pylance
- [ ] Đã cài tất cả thư viện từ requirements.txt
- [ ] Đã chạy thành công script test
- [ ] Đã đọc README.md
- [ ] Đã xem cấu trúc dự án

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: `python: command not found`
**Nguyên nhân:** Python chưa được thêm vào PATH
**Giải pháp:**
- Windows: Cài lại Python, đảm bảo tick "Add Python to PATH"
- Mac/Linux: Dùng `python3` thay vì `python`

### Lỗi 2: `pip: command not found`
**Nguyên nhân:** pip chưa được cài hoặc venv chưa kích hoạt
**Giải pháp:**
```bash
python -m ensurepip --upgrade
# Hoặc
python -m pip install --upgrade pip
```

### Lỗi 3: `Permission denied` khi cài package
**Nguyên nhân:** Đang cài vào Python hệ thống thay vì venv
**Giải pháp:** Đảm bảo venv đã được kích hoạt (thấy `(venv)` ở đầu dòng)

### Lỗi 4: VS Code không nhận Python
**Nguyên nhân:** Chưa chọn Python interpreter đúng
**Giải pháp:**
1. Mở VS Code
2. `Ctrl+Shift+P` (hoặc `Cmd+Shift+P` trên Mac)
3. Gõ "Python: Select Interpreter"
4. Chọn Python từ `venv/Scripts/python.exe`

### Lỗi 5: `ModuleNotFoundError` khi import
**Nguyên nhân:** Thư viện chưa được cài hoặc đang dùng Python sai
**Giải pháp:**
```bash
# Kiểm tra venv đã kích hoạt
# Cài lại thư viện
pip install <tên_thư_viện>
```

---

## 📚 TÀI LIỆU THAM KHẢO

### Python:
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python for Beginners](https://www.python.org/about/gettingstarted/)

### VS Code:
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Getting Started](https://code.visualstudio.com/docs/getstarted/introvideos)

### Virtual Environment:
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)
- [Real Python: Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

### pip và requirements.txt:
- [pip User Guide](https://pip.pypa.io/en/stable/user_guide/)
- [Managing Python Dependencies](https://realpython.com/python-application-layouts/)

---

## 💡 LƯU Ý CHO GIÁO VIÊN

1. **Kiểm tra từng học sinh:**
   - Đi vòng quanh lớp, kiểm tra từng máy
   - Đảm bảo tất cả đã cài đặt đúng
   - Giúp học sinh gặp lỗi

2. **Tốc độ:**
   - Học sinh có máy nhanh: Có thể làm thêm bài tập
   - Học sinh gặp khó khăn: Hỗ trợ kỹ hơn, không vội

3. **Khuyến khích:**
   - Khen ngợi khi học sinh làm được
   - Động viên khi gặp lỗi
   - Tạo không khí vui vẻ, không áp lực

4. **Chuẩn bị:**
   - Có sẵn file requirements.txt
   - Có sẵn script test
   - Có sẵn giải pháp cho các lỗi thường gặp

---

## 🎯 KẾT THÚC BUỔI HỌC

### Tóm tắt:
1. ✅ Đã giới thiệu dự án Nền tảng Học tập Cá nhân hóa
2. ✅ Đã cài đặt Python 3.12 và virtual environment
3. ✅ Đã cài đặt VS Code và extensions
4. ✅ Đã cài đặt các thư viện cần thiết
5. ✅ Đã kiểm tra môi trường hoạt động đúng

### Chuẩn bị buổi sau:
- Đọc lại Python cơ bản (nếu chưa biết)
- Xem lại cấu trúc dự án
- Chuẩn bị tinh thần học xử lý dữ liệu CSV

### Thông báo:
> "Buổi sau chúng ta sẽ học về Python cơ bản và cách xử lý dữ liệu CSV với Pandas. Các em nhớ làm bài tập về nhà nhé!"

---

**Chúc các em học tốt! 🎉**

---

*Giáo án này có thể điều chỉnh linh hoạt theo tình hình thực tế của lớp học.*

