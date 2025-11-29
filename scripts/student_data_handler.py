"""
Xử lý dữ liệu cá nhân của học sinh
- Lưu dữ liệu điểm số, feedback, hồ sơ vào data/input
- Tự động chạy pipeline sau khi lưu
- Có thể được gọi từ web app hoặc chạy độc lập
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, Optional, List

# Thêm thư mục scripts vào path
scripts_dir = Path(__file__).parent
project_root = scripts_dir.parent
sys.path.insert(0, str(scripts_dir))

# Import các module cần thiết
from data_processor import process_all_data
from feature_engineering import create_features
from ai_model import train_model
from ai_recommender import process_all_students


# Đường dẫn thư mục
INPUT_DIR = project_root / 'data' / 'input'
OUTPUT_DIR = project_root / 'data' / 'output'


def _ensure_directories():
    """Đảm bảo các thư mục tồn tại"""
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _load_or_create_csv(filepath: Path, default_columns: List[str]) -> pd.DataFrame:
    """Tải file CSV hoặc tạo mới nếu chưa tồn tại"""
    if filepath.exists():
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            return df
        except Exception as e:
            print(f"⚠️  Không thể đọc {filepath.name}: {e}. Tạo file mới.")
    
    # Tạo DataFrame mới với cột mặc định
    df = pd.DataFrame(columns=default_columns)
    return df


def _save_dataframe(df: pd.DataFrame, filepath: Path):
    """Lưu DataFrame vào file CSV"""
    df.to_csv(filepath, index=False, encoding='utf-8')
    print(f"✅ Đã lưu {filepath.name}")


def _update_or_append_record(df: pd.DataFrame, new_record: Dict, 
                             unique_keys: List[str] = None) -> pd.DataFrame:
    """
    Cập nhật bản ghi nếu đã tồn tại (dựa trên unique_keys) hoặc thêm mới
    """
    if unique_keys and not df.empty:
        # Tìm bản ghi trùng
        mask = pd.Series([True] * len(df))
        for key in unique_keys:
            if key in new_record and key in df.columns:
                mask = mask & (df[key] == new_record[key])
        
        if mask.any():
            # Cập nhật bản ghi cũ
            idx = df[mask].index[0]
            for key, value in new_record.items():
                if key in df.columns:
                    df.at[idx, key] = value
            print(f"🔄 Đã cập nhật bản ghi (dựa trên {unique_keys})")
        else:
            # Thêm bản ghi mới
            new_df = pd.DataFrame([new_record])
            df = pd.concat([df, new_df], ignore_index=True)
            print(f"➕ Đã thêm bản ghi mới")
    else:
        # Thêm mới
        new_df = pd.DataFrame([new_record])
        df = pd.concat([df, new_df], ignore_index=True)
        print(f"➕ Đã thêm bản ghi mới")
    
    return df


def add_grade_record(student_id: str, subject_code: str, grade_score: float,
                    attendance_rate: float = 0.95, homework_completion: float = 0.90,
                    semester: int = 1, year: int = 2024) -> bool:
    """
    Thêm bản ghi điểm số cho học sinh
    
    Args:
        student_id: Mã học sinh
        subject_code: Mã môn học
        grade_score: Điểm số (0-10)
        attendance_rate: Tỷ lệ chuyên cần (0-1 hoặc 0-100)
        homework_completion: Tỷ lệ hoàn thành bài tập (0-1 hoặc 0-100)
        semester: Học kỳ (1 hoặc 2)
        year: Năm học
    
    Returns:
        True nếu thành công
    """
    try:
        _ensure_directories()
        
        # Chuẩn hóa attendance và homework về 0-1
        if attendance_rate > 1:
            attendance_rate = attendance_rate / 100
        if homework_completion > 1:
            homework_completion = homework_completion / 100
        
        # Tạo bản ghi mới
        grade_record = {
            'student_id': student_id,
            'subject_code': subject_code,
            'grade_score': round(grade_score, 2),
            'attendance_rate': round(attendance_rate, 2),
            'homework_completion': round(homework_completion, 2),
            'semester': semester,
            'year': year
        }
        
        # Tải file grades.csv
        grades_file = INPUT_DIR / 'grades.csv'
        default_columns = ['student_id', 'subject_code', 'grade_score', 
                          'attendance_rate', 'homework_completion', 'semester', 'year']
        df = _load_or_create_csv(grades_file, default_columns)
        
        # Cập nhật hoặc thêm mới
        df = _update_or_append_record(df, grade_record, 
                                      unique_keys=['student_id', 'subject_code', 'semester', 'year'])
        
        # Lưu file
        _save_dataframe(df, grades_file)
        
        print(f"📝 Đã thêm điểm cho {student_id} - {subject_code}: {grade_score}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi thêm điểm: {e}")
        import traceback
        traceback.print_exc()
        return False


def add_feedback_record(student_id: str, subject_code: str, 
                       comment: str = '', strengths: str = '', 
                       improvements: str = '', teacher_id: str = 'MANUAL',
                       semester: int = 1) -> bool:
    """
    Thêm bản ghi feedback từ giáo viên
    
    Args:
        student_id: Mã học sinh
        subject_code: Mã môn học
        comment: Nhận xét chung
        strengths: Điểm mạnh
        improvements: Cần cải thiện
        teacher_id: Mã giáo viên (mặc định 'MANUAL' cho dữ liệu tự nhập)
        semester: Học kỳ
    
    Returns:
        True nếu thành công
    """
    try:
        _ensure_directories()
        
        # Tạo bản ghi mới
        feedback_record = {
            'student_id': student_id,
            'subject_code': subject_code,
            'teacher_id': teacher_id,
            'comment': comment or 'Dữ liệu do học sinh nhập',
            'strengths': strengths or 'Chủ động học tập',
            'improvements': improvements or 'Tiếp tục luyện tập và đặt mục tiêu rõ ràng',
            'semester': semester
        }
        
        # Tải file teacher_feedback.csv
        feedback_file = INPUT_DIR / 'teacher_feedback.csv'
        default_columns = ['student_id', 'subject_code', 'teacher_id', 
                          'comment', 'strengths', 'improvements', 'semester']
        df = _load_or_create_csv(feedback_file, default_columns)
        
        # Cập nhật hoặc thêm mới
        df = _update_or_append_record(df, feedback_record,
                                      unique_keys=['student_id', 'subject_code', 'semester'])
        
        # Lưu file
        _save_dataframe(df, feedback_file)
        
        print(f"💬 Đã thêm feedback cho {student_id} - {subject_code}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi thêm feedback: {e}")
        import traceback
        traceback.print_exc()
        return False


def update_student_profile(student_id: str, name: str = None,
                          major: str = None, career_path: str = None,
                          learning_style: str = None, interests: str = None,
                          goals: str = None) -> bool:
    """
    Cập nhật hoặc tạo hồ sơ học sinh
    
    Args:
        student_id: Mã học sinh
        name: Tên học sinh
        major: Chuyên ngành
        career_path: Định hướng nghề nghiệp
        learning_style: Phong cách học tập
        interests: Sở thích
        goals: Mục tiêu
    
    Returns:
        True nếu thành công
    """
    try:
        _ensure_directories()
        
        # Tải file student_profile.csv
        profile_file = INPUT_DIR / 'student_profile.csv'
        default_columns = ['student_id', 'name', 'major', 'career_path', 
                          'learning_style', 'interests', 'goals']
        df = _load_or_create_csv(profile_file, default_columns)
        
        # Tạo hoặc cập nhật bản ghi
        profile_record = {
            'student_id': student_id,
            'name': name or f'Học sinh {student_id}',
            'major': major or 'General',
            'career_path': career_path or 'general',
            'learning_style': learning_style or 'Mixed',
            'interests': interests or 'Học tập',
            'goals': goals or 'Cải thiện kết quả học tập'
        }
        
        # Cập nhật các trường nếu được cung cấp
        if not df.empty:
            existing = df[df['student_id'] == student_id]
            if not existing.empty:
                idx = existing.index[0]
                for key, value in profile_record.items():
                    if value is not None:
                        df.at[idx, key] = value
                print(f"🔄 Đã cập nhật hồ sơ cho {student_id}")
            else:
                df = _update_or_append_record(df, profile_record, unique_keys=['student_id'])
        else:
            df = _update_or_append_record(df, profile_record, unique_keys=['student_id'])
        
        # Lưu file
        _save_dataframe(df, profile_file)
        
        print(f"👤 Đã cập nhật hồ sơ cho {student_id}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật hồ sơ: {e}")
        import traceback
        traceback.print_exc()
        return False


def save_student_personal_data(student_id: str, data: Dict) -> bool:
    """
    Lưu dữ liệu cá nhân của học sinh từ form hoặc dictionary
    
    Args:
        student_id: Mã học sinh
        data: Dictionary chứa dữ liệu:
            - subject_code: Mã môn học (bắt buộc)
            - grade_score: Điểm số (bắt buộc)
            - attendance_rate: Tỷ lệ chuyên cần
            - homework_completion: Tỷ lệ hoàn thành bài tập
            - semester: Học kỳ
            - year: Năm học
            - comment: Nhận xét
            - strengths: Điểm mạnh
            - improvements: Cần cải thiện
            - name: Tên học sinh
            - major: Chuyên ngành
            - career_path: Định hướng nghề nghiệp
            - learning_style: Phong cách học tập
            - interests: Sở thích
            - goals: Mục tiêu
    
    Returns:
        True nếu thành công
    """
    try:
        print(f"\n{'='*60}")
        print(f"📥 BẮT ĐẦU LƯU DỮ LIỆU CÁ NHÂN CHO {student_id}")
        print(f"{'='*60}\n")
        
        success = True
        
        # 1. Lưu điểm số (nếu có)
        if 'subject_code' in data and 'grade_score' in data:
            success = add_grade_record(
                student_id=student_id,
                subject_code=data.get('subject_code'),
                grade_score=float(data.get('grade_score', 0)),
                attendance_rate=float(data.get('attendance_rate', 95)),
                homework_completion=float(data.get('homework_completion', 90)),
                semester=int(data.get('semester', 1)),
                year=int(data.get('year', 2024))
            ) and success
        
        # 2. Lưu feedback (nếu có)
        if 'subject_code' in data:
            success = add_feedback_record(
                student_id=student_id,
                subject_code=data.get('subject_code'),
                comment=data.get('comment', ''),
                strengths=data.get('strengths', ''),
                improvements=data.get('improvements', ''),
                teacher_id=data.get('teacher_id', 'MANUAL'),
                semester=int(data.get('semester', 1))
            ) and success
        
        # 3. Cập nhật hồ sơ (nếu có thông tin)
        if any(key in data for key in ['name', 'major', 'career_path', 'learning_style', 'interests', 'goals']):
            success = update_student_profile(
                student_id=student_id,
                name=data.get('name'),
                major=data.get('major'),
                career_path=data.get('career_path'),
                learning_style=data.get('learning_style'),
                interests=data.get('interests'),
                goals=data.get('goals')
            ) and success
        
        if success:
            print(f"\n✅ Đã lưu tất cả dữ liệu cho {student_id}")
        else:
            print(f"\n⚠️  Một số dữ liệu không thể lưu cho {student_id}")
        
        return success
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu dữ liệu cá nhân: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_pipeline_for_student(student_id: str, run_full: bool = True) -> bool:
    """
    Chạy pipeline xử lý dữ liệu sau khi học sinh nhập dữ liệu mới
    
    Args:
        student_id: Mã học sinh
        run_full: Nếu True, chạy toàn bộ pipeline (bao gồm train model)
                 Nếu False, chỉ chạy data processing và feature engineering
    
    Returns:
        True nếu thành công
    """
    try:
        print(f"\n{'='*60}")
        print(f"🔄 CHẠY PIPELINE CHO {student_id}")
        print(f"{'='*60}\n")
        
        # Bước 1: Xử lý dữ liệu
        print("📊 Bước 1: Xử lý và làm sạch dữ liệu...")
        process_all_data()
        
        # Bước 2: Feature Engineering
        print("\n📊 Bước 2: Feature Engineering...")
        create_features()
        
        if run_full:
            # Bước 3: Huấn luyện lại mô hình
            print("\n📊 Bước 3: Huấn luyện lại mô hình AI...")
            model = train_model()
            
            if model is None:
                print("⚠️  Không thể huấn luyện mô hình, nhưng vẫn tiếp tục...")
            else:
                # Bước 4: Tạo gợi ý
                print("\n📊 Bước 4: Tạo gợi ý học tập cá nhân hóa...")
                process_all_students()
        else:
            print("\n⏭️  Bỏ qua bước huấn luyện mô hình (run_full=False)")
        
        print(f"\n✅ Hoàn thành pipeline cho {student_id}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi chạy pipeline: {e}")
        import traceback
        traceback.print_exc()
        return False


def process_new_student_data(student_id: str, data: Dict, 
                            auto_run_pipeline: bool = True,
                            run_full_pipeline: bool = False) -> bool:
    """
    Xử lý dữ liệu mới của học sinh: Lưu dữ liệu và chạy pipeline
    
    Args:
        student_id: Mã học sinh
        data: Dictionary chứa dữ liệu cần lưu
        auto_run_pipeline: Tự động chạy pipeline sau khi lưu
        run_full_pipeline: Nếu True, chạy toàn bộ pipeline (train model)
                         Nếu False, chỉ chạy data processing và feature engineering
    
    Returns:
        True nếu thành công
    """
    try:
        # Bước 1: Lưu dữ liệu
        success = save_student_personal_data(student_id, data)
        
        if not success:
            print("❌ Không thể lưu dữ liệu. Dừng quy trình.")
            return False
        
        # Bước 2: Chạy pipeline (nếu được yêu cầu)
        if auto_run_pipeline:
            pipeline_success = run_pipeline_for_student(student_id, run_full=run_full_pipeline)
            if not pipeline_success:
                print("⚠️  Pipeline có lỗi, nhưng dữ liệu đã được lưu.")
        
        print(f"\n{'='*60}")
        print(f"✅ HOÀN TẤT XỬ LÝ DỮ LIỆU CHO {student_id}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi trong quy trình xử lý: {e}")
        import traceback
        traceback.print_exc()
        return False


# Ví dụ sử dụng
if __name__ == '__main__':
    # Ví dụ 1: Thêm điểm số đơn giản
    print("Ví dụ 1: Thêm điểm số")
    add_grade_record(
        student_id='HS999',
        subject_code='MATH201',
        grade_score=8.5,
        attendance_rate=95,
        homework_completion=90,
        semester=1,
        year=2024
    )
    
    # Ví dụ 2: Thêm feedback
    print("\nVí dụ 2: Thêm feedback")
    add_feedback_record(
        student_id='HS999',
        subject_code='MATH201',
        comment='Học sinh có tiến bộ tốt',
        strengths='Tư duy logic tốt',
        improvements='Cần luyện thêm bài tập nâng cao',
        semester=1
    )
    
    # Ví dụ 3: Cập nhật hồ sơ
    print("\nVí dụ 3: Cập nhật hồ sơ")
    update_student_profile(
        student_id='HS999',
        name='Nguyễn Văn A',
        major='Mathematics',
        career_path='engineering',
        learning_style='Visual',
        interests='Toán học, Lập trình',
        goals='Đạt điểm cao trong kỳ thi tốt nghiệp'
    )
    
    # Ví dụ 4: Lưu dữ liệu đầy đủ và chạy pipeline
    print("\nVí dụ 4: Lưu dữ liệu đầy đủ")
    data = {
        'subject_code': 'PHY201',
        'grade_score': 9.0,
        'attendance_rate': 98,
        'homework_completion': 95,
        'semester': 1,
        'year': 2024,
        'comment': 'Xuất sắc',
        'strengths': 'Hiểu nhanh, chăm chỉ',
        'improvements': 'Tiếp tục duy trì',
        'name': 'Nguyễn Văn A',
        'career_path': 'engineering'
    }
    
    process_new_student_data(
        student_id='HS999',
        data=data,
        auto_run_pipeline=True,
        run_full_pipeline=False  # Chỉ chạy data processing, không train lại model
    )

