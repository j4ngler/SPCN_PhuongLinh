"""
Flask Web Application cho Nền tảng Học tập Cá nhân hóa
API endpoint: /recommend - Trả về gợi ý học tập cá nhân hóa
Dashboard hiển thị kết quả học tập, biểu đồ năng lực, và gợi ý
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import io
import traceback
from typing import List, Optional, Dict
import re

# Thêm thư mục scripts vào path
project_root = Path(__file__).parent.parent
scripts_dir = project_root / 'scripts'
sys.path.insert(0, str(scripts_dir))

from ai_recommender import generate_recommendations, predict_ai_scores, process_all_students  # type: ignore
from database_manager import init_database, get_connection  # type: ignore
from data_processor import process_all_data  # type: ignore
from feature_engineering import create_features  # type: ignore
from ai_model import train_model  # type: ignore
from run_pipeline import run_full_pipeline  # type: ignore
from student_data_handler import process_new_student_data  # type: ignore
from student_utils import (  # type: ignore
    _load_subjects_dataframe,
    _simple_ai_score,
    generate_new_student_id,
    initialize_student_data,
    _get_subject_load_for_student,
    _save_subject_load_for_student,
    _get_timetable_meta_for_student,
)

# Import auth module
sys.path.insert(0, str(Path(__file__).parent))
from auth import (
    init_auth_database,
    authenticate_user,
    login_user,
    logout_user,
    get_current_user,
    create_user,
)


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
        timetable_info = None
        weekly_subject_load: List[Dict] = []
        reminders: List[str] = []

        # Nếu là học sinh, cố gắng lấy thời gian cập nhật TKB gần nhất + một vài lời nhắc đơn giản
        if user and user.get('role') == 'student':
            student_id = user['user_id']
            # Lấy thông tin thời khóa biểu (thời gian cập nhật)
            timetable_info = _get_timetable_meta_for_student(student_id)
            
            # Lấy danh sách môn học trong tuần (thời khóa biểu mới nhất)
            weekly_subject_load = _get_subject_load_for_student(student_id)

            # Lời nhắc dựa trên AI Score (nếu có)
            try:
                scores_df = predict_ai_scores(student_id)
                if scores_df is not None and not scores_df.empty:
                    low_count = int((scores_df['ai_score'] < 0.4).sum())
                    mid_count = int(((scores_df['ai_score'] >= 0.4) & (scores_df['ai_score'] < 0.7)).sum())
                    if low_count > 0:
                        reminders.append(
                            f"Có {low_count} môn đang ở mức CẦN CẢI THIỆN. Hãy tập trung nghe giảng hơn trong các tiết đó."
                        )
                    if mid_count > 0:
                        reminders.append(
                            f"Có {mid_count} môn ở mức TRUNG BÌNH. Bạn có thể đặt mục tiêu cải thiện trong tuần này."
                        )
            except Exception:
                pass

        return render_template(
            'index.html',
            user=user,
            timetable_info=timetable_info,
            weekly_subject_load=weekly_subject_load,
            reminders=reminders,
        )
    
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

    @app.route('/student/timetable', methods=['GET', 'POST'])
    def student_timetable():
        """Cho phép học sinh thiết lập 'môn học trong tuần' (TKB đơn giản theo số buổi/tuần)
        
        Người dùng có thể nhập MÃ MÔN hoặc TÊN MÔN:
        - Nếu trùng mã/tên trong subjects.csv -> hệ thống tự map sang subject_code chuẩn
        - Nếu không trùng -> lưu nguyên chuỗi nhập như một môn tự do (vẫn hiển thị ở TKB,
          nhưng sẽ không ghép được với AI_Score hiện tại).
        """
        user = get_current_user()
        if not user or user['role'] != 'student':
            return redirect(url_for('login'))

        student_id = user['user_id']
        subjects_df = _load_subjects_dataframe()
        all_subjects = []
        if subjects_df is not None and not subjects_df.empty:
            all_subjects = subjects_df[['subject_code', 'subject_name']].to_dict('records')

        # Chuẩn bị index để map text nhập (mã hoặc tên môn) về subject_code chuẩn
        def _norm_text(text: str) -> str:
            return re.sub(r'\s+', ' ', str(text or '').strip()).lower()

        code_index: Dict[str, Dict] = {}
        name_index: Dict[str, Dict] = {}
        for subj in all_subjects:
            scode = str(subj.get('subject_code') or '').strip()
            sname = str(subj.get('subject_name') or '').strip()
            if scode:
                code_index[_norm_text(scode)] = subj
            if sname:
                name_index[_norm_text(sname)] = subj

        # Danh sách ngày và tiết (khung TKB: Thứ 2 - Thứ 7, tiết 1-5 buổi sáng, 6-10 buổi chiều)
        days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7']
        day_keys = ['t2', 't3', 't4', 't5', 't6', 't7']
        periods = list(range(1, 11))  # 1-5: sáng, 6-10: chiều

        message = None
        error = None

        if request.method == 'POST':
            try:
                # Đếm số lần xuất hiện của từng mã môn trong khung TKB
                from collections import Counter

                subject_counter: Counter = Counter()

                for d_idx, d_key in enumerate(day_keys):
                    for period in periods:
                        field_name = f"slot_{d_key}_{period}"
                        code = (request.form.get(field_name, '') or '').strip()
                        if not code:
                            continue
                        subject_counter[code] += 1

                # Chuẩn bị dữ liệu lưu vào bảng student_subject_load
                subjects_to_save: List[Dict] = []
                
                for code, count in subject_counter.items():
                    raw_text = str(code or '').strip()
                    norm = _norm_text(raw_text)

                    resolved_code = None
                    resolved_name = None

                    # 1) Thử map theo mã môn
                    subj = code_index.get(norm)
                    if subj:
                        resolved_code = subj.get('subject_code')
                        resolved_name = subj.get('subject_name')
                    else:
                        # 2) Thử map theo tên môn
                        subj = name_index.get(norm)
                        if subj:
                            resolved_code = subj.get('subject_code')
                            resolved_name = subj.get('subject_name')

                    # 3) Nếu không tìm thấy trong danh sách, coi đây là môn tự do
                    if not resolved_code:
                        resolved_code = raw_text    # dùng chính text làm "mã"
                        resolved_name = raw_text    # và cũng là tên hiển thị

                    subjects_to_save.append(
                        {
                            'subject_code': resolved_code,
                            'subject_name': resolved_name,
                            'lessons_per_week': int(count),
                        }
                    )

                if not subjects_to_save:
                    raise ValueError("Vui lòng nhập ít nhất 1 tiết học trong tuần (nhập mã môn vào các ô trong bảng)")

                _save_subject_load_for_student(student_id, subjects_to_save)
                message = "✅ Đã lưu thời khóa biểu đơn giản cho tuần của bạn."
            except ValueError as ve:
                error = str(ve)
            except Exception as e:
                error = f"Không thể lưu thời khóa biểu: {e}"

        current_subject_load = _get_subject_load_for_student(student_id)

        # Nếu chưa có cấu hình, gợi ý tối đa 5 môn đầu tiên từ danh sách môn học
        if not current_subject_load and all_subjects:
            for subj in all_subjects[:5]:
                current_subject_load.append(
                    {
                        'subject_code': subj.get('subject_code', ''),
                        'subject_name': subj.get('subject_name', ''),
                        'lessons_per_week': 0,
                    }
                )

        return render_template(
            'timetable.html',
            user=user,
            student_id=student_id,
            all_subjects=all_subjects,
            subject_load=current_subject_load,
            message=message,
            error=error,
        )
    
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
        user = get_current_user()
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

            # Lấy cấu hình môn học trong tuần của học sinh (TKB đơn giản)
            weekly_subject_load = _get_subject_load_for_student(student_id)

            # Ghép thêm AI Score vào từng môn trong tuần (nếu có)
            ai_score_by_subject: Dict[str, float] = {}
            if scores_data:
                for row in scores_data:
                    code = str(row.get('subject_code') or '').strip()
                    if not code:
                        continue
                    try:
                        score_val = float(row.get('ai_score', 0.0))
                    except (TypeError, ValueError):
                        score_val = 0.0
                    ai_score_by_subject[code] = score_val

            for item in weekly_subject_load:
                code = str(item.get('subject_code') or '').strip()
                item['ai_score'] = ai_score_by_subject.get(code)
            
            generated_student_id = session.pop('generated_student_id', None)
            
            return render_template(
                'dashboard.html',
                user=user,
                student_id=student_id,
                profile=profile,
                scores=scores_data,
                recommendations=recommendations,
                grades=grades_data,
                stats=stats,
                generated_student_id=generated_student_id,
                weekly_subject_load=weekly_subject_load,
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
    port = int(os.environ.get('PORT', 5001))
    base_url = f"http://localhost:{port}"

    print(f"🚀 Khởi động web app tại {base_url}")
    print(f"📊 Dashboard: {base_url}/dashboard/<student_id>")
    print(f"🔗 API Recommend: {base_url}/recommend")

    # Tự động mở trình duyệt sau khi server khởi động
    def open_browser():
        # Chờ một chút để Flask khởi động xong
        time.sleep(1.5)
        try:
            webbrowser.open_new(base_url)
        except Exception as e:
            print(f"⚠️ Không thể tự mở trình duyệt: {e}")

    threading.Thread(target=open_browser, daemon=True).start()

    app.run(debug=True, host='0.0.0.0', port=port)

