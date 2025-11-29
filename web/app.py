"""
Flask Web Application cho Nền tảng Học tập Cá nhân hóa
API endpoint: /recommend - Trả về gợi ý học tập cá nhân hóa
Dashboard hiển thị kết quả học tập, biểu đồ năng lực, và gợi ý
"""

import os
import sys
import random
import webbrowser
import threading
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import io
import traceback
import re
from typing import List, Optional, Dict

# Thêm thư mục scripts vào path
project_root = Path(__file__).parent.parent
scripts_dir = project_root / 'scripts'
sys.path.insert(0, str(scripts_dir))

from ai_recommender import generate_recommendations, predict_ai_scores, process_all_students
from database_manager import init_database
from data_processor import process_all_data
from feature_engineering import create_features
from ai_model import train_model
from run_pipeline import run_full_pipeline
from student_data_handler import process_new_student_data

# Import auth module
sys.path.insert(0, str(Path(__file__).parent))
from auth import (
    init_auth_database, authenticate_user, login_user, logout_user,
    get_current_user, create_user
)


def _load_subjects_dataframe() -> pd.DataFrame:
    """Đọc danh sách môn học từ output hoặc input"""
    paths = [
        project_root / 'data' / 'output' / 'subjects_cleaned.csv',
        project_root / 'data' / 'input' / 'subjects.csv'
    ]
    for path in paths:
        if path.exists():
            try:
                return pd.read_csv(path)
            except Exception:
                return pd.DataFrame()
    return pd.DataFrame()


def _load_student_profile(student_id: str) -> dict:
    """Tìm profile học sinh trong output hoặc input"""
    paths = [
        project_root / 'data' / 'output' / 'student_profiles_cleaned.csv',
        project_root / 'data' / 'input' / 'student_profile.csv'
    ]
    for path in paths:
        if path.exists():
            try:
                df = pd.read_csv(path)
                match = df[df['student_id'] == student_id]
                if not match.empty:
                    return match.iloc[0].to_dict()
            except Exception:
                continue
    return {}


def _save_student_dataframe(path: Path, student_id: str, df_new: pd.DataFrame, replace: bool = True, subset: Optional[List[str]] = None):
    """Ghi dữ liệu học sinh vào file CSV
    
    Args:
        path: Đường dẫn file
        student_id: Mã học sinh
        df_new: DataFrame cần ghi
        replace: True -> xoá toàn bộ dữ liệu cũ của học sinh trước khi ghi
        subset: Nếu replace=False, dùng subset để loại bỏ trùng dòng (ví dụ ['student_id','subject_code'])
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing = pd.read_csv(path)
            if replace and 'student_id' in existing.columns:
                existing = existing[existing['student_id'] != student_id]
            else:
                df_new = pd.concat([existing, df_new], ignore_index=True)
                if subset:
                    df_new = df_new.drop_duplicates(subset=subset, keep='last')
                    df_new = df_new.reset_index(drop=True)
                df_new.to_csv(path, index=False, encoding='utf-8')
                return
        except Exception:
            pass
    df_new.to_csv(path, index=False, encoding='utf-8')


def _save_student_input_data(student_id: str, synthetic_data: dict):
    """Ghi dữ liệu của học sinh vào các file input"""
    input_dir = project_root / 'data' / 'input'
    input_dir.mkdir(parents=True, exist_ok=True)
    
    if synthetic_data.get('profile') is not None:
        _save_student_dataframe(input_dir / 'student_profile.csv', student_id, synthetic_data['profile'])
    
    if synthetic_data.get('grades') is not None:
        _save_student_dataframe(input_dir / 'grades.csv', student_id, synthetic_data['grades'])
    
    if synthetic_data.get('feedback') is not None:
        _save_student_dataframe(input_dir / 'teacher_feedback.csv', student_id, synthetic_data['feedback'])


def _simple_ai_score(grade: float, attendance: float, homework: float) -> float:
    """Tính AI Score đơn giản từ điểm số và tỉ lệ"""
    attendance = attendance if attendance <= 1 else attendance / 100
    homework = homework if homework <= 1 else homework / 100
    grade_norm = grade / 10
    score = 0.5 * grade_norm + 0.25 * attendance + 0.25 * homework
    return round(max(0.0, min(1.0, score)), 4)


def generate_new_student_id(prefix: str = 'HS') -> str:
    """Sinh mã học sinh mới chưa tồn tại"""
    existing_ids = set()
    
    def collect_ids(path: Path):
        if path.exists():
            try:
                df = pd.read_csv(path)
                if 'student_id' in df.columns:
                    existing_ids.update(df['student_id'].dropna().astype(str).tolist())
            except Exception:
                pass
    
    collect_ids(project_root / 'data' / 'input' / 'student_profile.csv')
    collect_ids(project_root / 'data' / 'output' / 'student_profiles_cleaned.csv')
    
    pattern = re.compile(rf'{prefix}(\d+)', re.IGNORECASE)
    max_num = 0
    for sid in existing_ids:
        match = pattern.fullmatch(str(sid))
        if match:
            try:
                num = int(match.group(1))
                max_num = max(max_num, num)
            except ValueError:
                continue
    return f"{prefix}{max_num + 1:03d}"


def _create_synthetic_student_data(student_id: str, full_name: str = None):
    """Tạo dữ liệu giả lập cho học sinh mới"""
    subjects_df = _load_subjects_dataframe()
    if subjects_df.empty:
        return None
    
    sample_subjects = subjects_df.sample(
        n=min(6, len(subjects_df)),
        random_state=random.randint(1, 1_000_000)
    ).reset_index(drop=True)
    
    ai_scores = []
    grades = []
    recommendations = []
    
    feedback_rows = []
    
    for idx, subject in sample_subjects.iterrows():
        ai_score = round(random.uniform(0.45, 0.9), 4)
        ai_scores.append({
            'student_id': student_id,
            'subject_code': subject.get('subject_code', f'SUB{idx:03d}'),
            'subject_name': subject.get('subject_name', 'Môn học'),
            'ai_score': ai_score
        })
        
        grade_score = round(random.uniform(7.0, 9.5), 1)
        attendance = round(random.uniform(0.85, 0.98), 2)
        homework = round(random.uniform(0.82, 0.97), 2)
        semester = 1 if idx % 2 == 0 else 2
        year = 2024 + (idx // 4)
        grades.append({
            'student_id': student_id,
            'subject_code': subject.get('subject_code', f'SUB{idx:03d}'),
            'grade_score': grade_score,
            'attendance_rate': attendance,
            'homework_completion': homework,
            'semester': semester,
            'year': year
        })
        
        recommendations.append({
            'student_id': student_id,
            'subject_code': subject.get('subject_code', f'SUB{idx:03d}'),
            'subject_name': subject.get('subject_name', 'Môn học'),
            'ai_score': ai_score,
            'priority': idx + 1,
            'reason': f"Môn học phù hợp với năng lực (AI Score: {ai_score:.2f})"
        })
        
        feedback_rows.append({
            'student_id': student_id,
            'subject_code': subject.get('subject_code', f'SUB{idx:03d}'),
            'teacher_id': f'AUTO{idx+1:03d}',
            'comment': 'Dữ liệu tự sinh cho học sinh mới',
            'strengths': 'Năng lực tốt, thái độ tích cực',
            'improvements': 'Tiếp tục luyện tập và ôn bài',
            'semester': semester
        })
    feedback_df = pd.DataFrame(feedback_rows)
    ai_scores_df = pd.DataFrame(ai_scores)
    grades_df = pd.DataFrame(grades)
    recs_df = pd.DataFrame(recommendations).sort_values(by='ai_score', ascending=False).head(10)
    
    profile = _load_student_profile(student_id)
    if not profile:
        sample_subject = sample_subjects.iloc[0] if not sample_subjects.empty else None
        profile = {
            'student_id': student_id,
            'name': full_name or f'Học sinh {student_id}',
            'major': sample_subject.get('category', 'General') if sample_subject is not None else 'General',
            'career_path': 'engineering',
            'learning_style': random.choice(['Visual', 'Auditory', 'Kinesthetic', 'Mixed']),
            'interests': 'Công nghệ, học tập',
            'goals': 'Cải thiện kết quả học tập'
        }
    
    profile_df = pd.DataFrame([profile])
    
    return {
        'ai_scores': ai_scores_df,
        'grades': grades_df,
        'recommendations': recs_df,
        'feedback': feedback_df,
        'profile': profile_df
    }


def initialize_student_data(student_id: str, full_name: str = None):
    """
    Đảm bảo học sinh mới đăng ký có dữ liệu hiển thị trên dashboard.
    Ưu tiên dùng dữ liệu thật nếu đã có, nếu không sẽ tạo dữ liệu giả lập.
    """
    output_dir = project_root / 'data' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        scores_df = None
        try:
            scores_df = predict_ai_scores(student_id)
        except Exception:
            scores_df = None
        
        if scores_df is not None and not scores_df.empty:
            _save_student_dataframe(output_dir / 'ai_scores.csv', student_id, scores_df)
            recommendations = generate_recommendations(student_id, top_n=10)
            if recommendations:
                recs_df = pd.DataFrame(recommendations)
                _save_student_dataframe(output_dir / 'recommendations.csv', student_id, recs_df)
        else:
            synthetic = _create_synthetic_student_data(student_id, full_name)
            if synthetic:
                _save_student_dataframe(output_dir / 'ai_scores.csv', student_id, synthetic['ai_scores'])
                _save_student_dataframe(output_dir / 'recommendations.csv', student_id, synthetic['recommendations'])
                _save_student_dataframe(output_dir / 'grades_cleaned.csv', student_id, synthetic['grades'])
                _save_student_dataframe(output_dir / 'student_profiles_cleaned.csv', student_id, synthetic['profile'])
                if synthetic.get('feedback') is not None:
                    _save_student_dataframe(output_dir / 'feedback_cleaned.csv', student_id, synthetic['feedback'])
                
                _save_student_input_data(student_id, synthetic)
                return
        
        # Nếu có profile thật, đảm bảo ghi ra output
        profile = _load_student_profile(student_id)
        if profile:
            profile_df = pd.DataFrame([profile])
            _save_student_dataframe(output_dir / 'student_profiles_cleaned.csv', student_id, profile_df)
    except Exception:
        # Không để lỗi đăng ký chỉ vì tạo dữ liệu thất bại
        pass


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get('SPCN_SECRET', 'dev-secret-key-change-phuonglinh')
    
    # Project base (parent of web/)
    app.config['PROJECT_BASE_DIR'] = project_root
    
    # Khởi tạo database khi start app
    with app.app_context():
        init_database()
        init_auth_database()
    
    def project_path(filename: str) -> Path:
        """Tìm file ở vị trí mới (data/output/, config/) hoặc vị trí cũ"""
        data_output = project_root / 'data' / 'output'
        config_dir = project_root / 'config'
        
        # File config
        if filename.endswith('.json'):
            new_path = config_dir / filename
            if new_path.exists():
                return new_path
        
        # File output
        if filename.endswith('.csv'):
            new_path = data_output / filename
            if new_path.exists():
                return new_path
        
        # Fallback: thư mục gốc
        return project_root / filename
    
    @app.route('/')
    def index():
        """Trang chủ"""
        user = get_current_user()
        return render_template('index.html', user=user)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Đăng nhập"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = authenticate_user(username, password)
            if user:
                login_user(user)
                # Redirect theo role
                if user['role'] == 'student':
                    return redirect(url_for('student_dashboard'))
                elif user['role'] == 'parent':
                    return redirect(url_for('parent_dashboard'))
                else:
                    return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Tên đăng nhập hoặc mật khẩu không đúng')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Đăng ký tài khoản mới"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            role = request.form.get('role')
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            student_id_input = request.form.get('student_id')  # Cho học sinh hoặc phụ huynh
            
            # Validation
            if not username or not password:
                return render_template('register.html', error='Vui lòng điền đầy đủ thông tin')
            
            if password != confirm_password:
                return render_template('register.html', error='Mật khẩu xác nhận không khớp')
            
            if not role or role not in ['student', 'parent']:
                return render_template('register.html', error='Vui lòng chọn loại tài khoản')
            
            generated_student_id = None
            
            # Yêu cầu nhập student_id cho phụ huynh, học sinh có thể để trống để hệ thống tự tạo
            if role == 'parent' and not student_id_input:
                return render_template('register.html', error='Phụ huynh cần nhập mã học sinh của con')
            
            if role == 'student' and (not student_id_input or not student_id_input.strip()):
                student_id_input = generate_new_student_id()
                generated_student_id = student_id_input.strip()
            
            # Tạo user_id: học sinh dùng chính mã học sinh, phụ huynh dùng username
            if role == 'student':
                user_id = student_id_input
                linked_student_id = student_id_input
            else:
                user_id = username
                linked_student_id = student_id_input
            
            # Tạo tài khoản
            success = create_user(
                user_id=user_id,
                username=username,
                password=password,
                role=role,
                full_name=full_name,
                email=email,
                student_id=linked_student_id
            )
            
            if success:
                if role == 'student':
                    initialize_student_data(student_id_input, full_name or username or username)
                elif role == 'parent':
                    initialize_student_data(student_id_input)
                
                # Tự động đăng nhập sau khi đăng ký
                user = authenticate_user(username, password)
                if user:
                    if generated_student_id:
                        session['generated_student_id'] = generated_student_id
                    login_user(user)
                    if user['role'] == 'student':
                        return redirect(url_for('student_dashboard'))
                    elif user['role'] == 'parent':
                        return redirect(url_for('parent_dashboard'))
                    else:
                        return redirect(url_for('index'))
            else:
                return render_template('register.html', error='Tên đăng nhập đã tồn tại hoặc mã học sinh đã được sử dụng')
        
        return render_template('register.html')
    
    @app.route('/logout')
    def logout():
        """Đăng xuất"""
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/student/dashboard')
    def student_dashboard():
        """Dashboard cho học sinh cấp 3"""
        user = get_current_user()
        if not user or user['role'] != 'student':
            return redirect(url_for('login'))
        
        student_id = user['user_id']
        return redirect(url_for('dashboard', student_id=student_id))
    
    @app.route('/parent/dashboard')
    def parent_dashboard():
        """Dashboard cho phụ huynh - Xem kết quả học tập của con"""
        user = get_current_user()
        if not user or user['role'] != 'parent':
            return redirect(url_for('login'))
        
        student_id = user.get('student_id')
        if not student_id:
            return render_template('parent_dashboard.html', 
                                 user=user, 
                                 error='Chưa liên kết với học sinh')
        
        return redirect(url_for('dashboard', student_id=student_id))
    
    @app.route('/student/data-entry', methods=['GET', 'POST'])
    def student_data_entry():
        """Cho phép học sinh nhập dữ liệu điểm số của mình"""
        user = get_current_user()
        if not user or user['role'] != 'student':
            return redirect(url_for('login'))
        
        subjects_df = _load_subjects_dataframe()
        subjects_list = []
        if subjects_df is not None and not subjects_df.empty:
            subjects_list = subjects_df[['subject_code', 'subject_name']].to_dict('records')
        
        message = None
        error = None
        
        if request.method == 'POST':
            try:
                student_id = user['user_id']
                
                # Chuyển đổi form data thành dictionary
                data = {
                    'subject_code': request.form.get('subject_code', '').strip(),
                    'grade_score': request.form.get('grade_score', '0'),
                    'attendance_rate': request.form.get('attendance_rate', '95'),
                    'homework_completion': request.form.get('homework_completion', '90'),
                    'semester': request.form.get('semester', '1'),
                    'year': request.form.get('year', '2024'),
                    'comment': request.form.get('comment', '').strip(),
                    'strengths': request.form.get('strengths', '').strip(),
                    'improvements': request.form.get('improvements', '').strip(),
                }
                
                # Thêm thông tin hồ sơ nếu có
                if request.form.get('name'):
                    data['name'] = request.form.get('name').strip()
                if request.form.get('major'):
                    data['major'] = request.form.get('major').strip()
                if request.form.get('career_path'):
                    data['career_path'] = request.form.get('career_path').strip()
                if request.form.get('learning_style'):
                    data['learning_style'] = request.form.get('learning_style').strip()
                if request.form.get('interests'):
                    data['interests'] = request.form.get('interests').strip()
                if request.form.get('goals'):
                    data['goals'] = request.form.get('goals').strip()
                
                # Validate dữ liệu
                if not data['subject_code']:
                    raise ValueError('Vui lòng chọn môn học')
                
                # Lưu dữ liệu và chạy pipeline (không train lại model để nhanh hơn)
                success = process_new_student_data(
                    student_id=student_id,
                    data=data,
                    auto_run_pipeline=True,
                    run_full_pipeline=False  # Chỉ xử lý dữ liệu, không train lại model
                )
                
                if success:
                    # Tính AI Score đơn giản để hiển thị
                    grade_score = float(data.get('grade_score', 0))
                    attendance = float(data.get('attendance_rate', 95))
                    homework = float(data.get('homework_completion', 90))
                    attendance_dec = attendance / 100 if attendance > 1 else attendance
                    homework_dec = homework / 100 if homework > 1 else homework
                    ai_score = _simple_ai_score(grade_score, attendance_dec, homework_dec)
                    
                    message = f"✅ Đã lưu dữ liệu cho môn {data['subject_code']} (AI Score ~ {ai_score:.2f}). Hệ thống đã xử lý và cập nhật gợi ý học tập."
                else:
                    raise Exception('Không thể lưu dữ liệu')
                    
            except ValueError as ve:
                error = str(ve)
            except Exception as e:
                error = f"Không thể lưu dữ liệu: {e}"
        
        return render_template(
            'student_data_entry.html',
            user=user,
            subjects=subjects_list,
            message=message,
            error=error
        )
    
    @app.route('/recommend', methods=['GET', 'POST'])
    def recommend():
        """
        API endpoint trả về gợi ý học tập cá nhân hóa
        GET: Hiển thị form nhập student_id
        POST: Trả về JSON với gợi ý
        """
        if request.method == 'POST':
            data = request.get_json() if request.is_json else request.form
            student_id = data.get('student_id')
            top_n = int(data.get('top_n', 10))
            
            # Kiểm tra quyền truy cập
            user = get_current_user()
            if user:
                # Học sinh chỉ xem được của mình
                if user['role'] == 'student' and student_id != user['user_id']:
                    return jsonify({'error': 'Không có quyền truy cập'}), 403
                # Phụ huynh chỉ xem được của con
                if user['role'] == 'parent' and student_id != user.get('student_id'):
                    return jsonify({'error': 'Không có quyền truy cập'}), 403
            
            if not student_id:
                return jsonify({'error': 'student_id is required'}), 400
            
            try:
                recommendations = generate_recommendations(student_id, top_n=top_n)
                return jsonify({
                    'student_id': student_id,
                    'recommendations': recommendations,
                    'count': len(recommendations)
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # GET: Hiển thị form
        user = get_current_user()
        return render_template('recommend.html', user=user)
    
    @app.route('/dashboard/<student_id>')
    def dashboard(student_id):
        """Dashboard hiển thị kết quả học tập và gợi ý"""
        try:
            # Đọc trực tiếp từ file output nếu có
            output_dir = project_root / 'data' / 'output'
            
            # Đọc hồ sơ học sinh
            profiles_path = output_dir / 'student_profiles_cleaned.csv'
            profile = None
            if profiles_path.exists():
                try:
                    profiles_df = pd.read_csv(profiles_path)
                    student_profile = profiles_df[profiles_df['student_id'] == student_id]
                    if not student_profile.empty:
                        profile = student_profile.iloc[0].to_dict()
                except:
                    pass
            
            # Đọc AI Scores từ file
            scores_data = None
            scores_path = output_dir / 'ai_scores.csv'
            if scores_path.exists():
                try:
                    scores_df = pd.read_csv(scores_path)
                    student_scores = scores_df[scores_df['student_id'] == student_id]
                    if not student_scores.empty:
                        scores_data = student_scores.to_dict('records')
                except:
                    pass
            
            # Nếu không có từ file, thử dùng API
            if scores_data is None:
                try:
                    scores_df = predict_ai_scores(student_id)
                    if scores_df is not None and not scores_df.empty:
                        scores_data = scores_df.to_dict('records')
                except:
                    pass
            
            # Đọc Recommendations từ file
            recommendations = []
            rec_path = output_dir / 'recommendations.csv'
            if rec_path.exists():
                try:
                    rec_df = pd.read_csv(rec_path)
                    student_recs = rec_df[rec_df['student_id'] == student_id].head(10)
                    if not student_recs.empty:
                        recommendations = student_recs.to_dict('records')
                except:
                    pass
            
            # Nếu không có từ file, thử tạo mới
            if not recommendations:
                try:
                    recommendations = generate_recommendations(student_id, top_n=10)
                except:
                    pass
            
            # Đọc điểm số thực tế
            grades_data = None
            grades_path = output_dir / 'grades_cleaned.csv'
            if grades_path.exists():
                try:
                    grades_df = pd.read_csv(grades_path)
                    student_grades = grades_df[grades_df['student_id'] == student_id]
                    if not student_grades.empty:
                        grades_data = student_grades.to_dict('records')
                except:
                    pass
            
            # Tính thống kê
            stats = {}
            if scores_data:
                ai_scores = [s.get('ai_score', 0) for s in scores_data if isinstance(s.get('ai_score'), (int, float))]
                if ai_scores:
                    stats['avg_ai_score'] = sum(ai_scores) / len(ai_scores)
                    stats['max_ai_score'] = max(ai_scores)
                    stats['min_ai_score'] = min(ai_scores)
                    stats['total_subjects'] = len(ai_scores)
            
            if grades_data:
                grade_scores = [g.get('grade_score', 0) for g in grades_data if isinstance(g.get('grade_score'), (int, float))]
                if grade_scores:
                    stats['avg_grade'] = sum(grade_scores) / len(grade_scores)
                    stats['total_grades'] = len(grade_scores)
            
            generated_student_id = session.pop('generated_student_id', None)
            
            return render_template(
                'dashboard.html',
                student_id=student_id,
                profile=profile,
                scores=scores_data,
                recommendations=recommendations,
                grades=grades_data,
                stats=stats,
                generated_student_id=generated_student_id
            )
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            return f"Lỗi: {e}<br><pre>{error_trace}</pre>", 500
    
    @app.route('/api/ai_scores/<student_id>')
    def api_ai_scores(student_id):
        """API trả về AI Scores của một học sinh"""
        try:
            scores_df = predict_ai_scores(student_id)
            if scores_df is None or scores_df.empty:
                return jsonify({'error': 'No data found'}), 404
            
            return jsonify({
                'student_id': student_id,
                'scores': scores_df.to_dict('records')
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/abilities/<student_id>')
    def api_abilities(student_id):
        """API trả về bảng tổng hợp năng lực học tập"""
        try:
            scores_df = predict_ai_scores(student_id)
            if scores_df is None or scores_df.empty:
                return jsonify({'error': 'No data found'}), 404
            
            # Tính toán năng lực theo category
            subjects_path = project_path('subjects_cleaned.csv')
            if subjects_path.exists():
                subjects_df = pd.read_csv(subjects_path)
                merged = scores_df.merge(
                    subjects_df,
                    on='subject_code',
                    how='left'
                )
                
                if 'category' in merged.columns:
                    abilities = merged.groupby('category').agg({
                        'ai_score': ['mean', 'count']
                    }).reset_index()
                    abilities.columns = ['category', 'avg_score', 'subject_count']
                    abilities = abilities.sort_values('avg_score', ascending=False)
                    
                    return jsonify({
                        'student_id': student_id,
                        'abilities': abilities.to_dict('records')
                    })
            
            return jsonify({'error': 'Unable to calculate abilities'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/manage')
    def manage():
        """Trang quản lý hệ thống"""
        user = get_current_user()
        if not user:
            return redirect(url_for('login'))
        return render_template('manage.html', user=user)
    
    @app.route('/api/run/<task_name>', methods=['POST'])
    def run_task(task_name):
        """API để chạy các tác vụ từ web"""
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'error': 'Cần đăng nhập'}), 401
        
        try:
            output_buffer = io.StringIO()
            error_buffer = io.StringIO()
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = output_buffer
            sys.stderr = error_buffer
            
            if task_name == 'data-processor':
                process_all_data()
                message = "Xử lý dữ liệu hoàn tất!"
                
            elif task_name == 'feature-engineering':
                create_features()
                message = "Feature Engineering hoàn tất!"
                
            elif task_name == 'train-model':
                model = train_model()
                if model is None:
                    raise Exception("Không thể huấn luyện mô hình")
                message = "Huấn luyện mô hình hoàn tất!"
                
            elif task_name == 'generate-recommendations':
                process_all_students()
                message = "Tạo gợi ý hoàn tất!"
                
            elif task_name == 'pipeline':
                run_full_pipeline()
                message = "Pipeline hoàn tất!"
                
            elif task_name == 'init-database':
                init_database()
                init_auth_database()
                message = "Khởi tạo database hoàn tất!"
                
            else:
                return jsonify({'success': False, 'error': f'Tác vụ không hợp lệ: {task_name}'}), 400
            
            output = output_buffer.getvalue()
            error_output = error_buffer.getvalue()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            full_output = output
            if error_output:
                full_output += "\n\n[STDERR]\n" + error_output
            
            return jsonify({
                'success': True,
                'message': message,
                'output': full_output
            })
            
        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            error_trace = traceback.format_exc()
            error_output = error_buffer.getvalue() if 'error_buffer' in locals() else ''
            return jsonify({
                'success': False,
                'error': str(e),
                'traceback': error_trace,
                'stderr': error_output
            }), 500
    
    @app.route('/api/upload', methods=['POST'])
    def upload_file():
        """API để upload file CSV"""
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'error': 'Cần đăng nhập'}), 401
        
        files = request.files.getlist('files')
        if not files:
            return jsonify({'success': False, 'error': 'Không có file'}), 400
        
        allowed_names = {
            'subjects.csv': 'subjects.csv',
            'grades.csv': 'grades.csv',
            'teacher_feedback.csv': 'teacher_feedback.csv',
            'career_path.csv': 'career_path.csv',
            'student_profile.csv': 'student_profile.csv'
        }
        
        saved_files = []
        skipped_files = []
        errors = []
        
        try:
            input_dir = project_root / 'data' / 'input'
            input_dir.mkdir(parents=True, exist_ok=True)
            
            for file in files:
                filename = file.filename
                if not filename:
                    continue
                if not filename.lower().endswith('.csv'):
                    skipped_files.append(f"{filename} (không phải CSV)")
                    continue
                
                canonical_name = allowed_names.get(filename.lower())
                if not canonical_name:
                    skipped_files.append(f"{filename} (không hợp lệ, cần đổi tên thành một trong {list(allowed_names.keys())})")
                    continue
                
                try:
                    file_path = input_dir / canonical_name
                    file.save(str(file_path))
                    saved_files.append(canonical_name)
                except Exception as save_err:
                    errors.append(f"Không thể lưu {filename}: {save_err}")
            
            if not saved_files and not errors:
                return jsonify({
                    'success': False,
                    'error': 'Không có file hợp lệ để upload',
                    'details': '\n'.join(skipped_files) if skipped_files else None
                }), 400
            
            response = {
                'success': not errors,
                'message': f'Đã upload {len(saved_files)} file',
                'saved_files': saved_files
            }
            if skipped_files:
                response['skipped'] = skipped_files
            if errors:
                response['success'] = False
                response['error'] = 'Một số file không thể lưu'
                response['details'] = '\n'.join(errors)
            
            return jsonify(response), (200 if response['success'] else 500 if errors else 200)
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Lỗi upload: {str(e)}'
            }), 500
    
    @app.route('/api/system-status', methods=['GET'])
    def system_status():
        """API kiểm tra trạng thái hệ thống"""
        try:
            input_dir = project_root / 'data' / 'input'
            output_dir = project_root / 'data' / 'output'
            models_dir = project_root / 'models'
            db_path = project_root / 'web' / 'student_learning.db'
            
            # Đếm file input
            input_files = 0
            if input_dir.exists():
                input_files = len([f for f in input_dir.iterdir() if f.suffix == '.csv'])
            
            # Đếm file output
            output_files = 0
            if output_dir.exists():
                output_files = len([f for f in output_dir.iterdir() if f.suffix == '.csv'])
            
            # Kiểm tra mô hình
            model_exists = (models_dir / 'ai_model.pkl').exists() if models_dir.exists() else False
            
            # Kiểm tra database
            database_exists = db_path.exists()
            
            return jsonify({
                'input_files': input_files,
                'output_files': output_files,
                'model_exists': model_exists,
                'database_exists': database_exists
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Khởi động web app tại http://localhost:{port}")
    print(f"📊 Dashboard: http://localhost:{port}/dashboard/<student_id>")
    print(f"🔗 API Recommend: http://localhost:{port}/recommend")
    app.run(debug=True, host='0.0.0.0', port=port)

