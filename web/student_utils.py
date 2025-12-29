import os
import sys
import random
import re
from pathlib import Path
from typing import List, Optional, Dict

import pandas as pd

# Thiết lập project_root và thêm thư mục scripts vào sys.path
project_root = Path(__file__).parent.parent
scripts_dir = project_root / "scripts"
sys.path.insert(0, str(scripts_dir))

from ai_recommender import generate_recommendations, predict_ai_scores  # type: ignore
from database_manager import get_connection  # type: ignore


def _load_subjects_dataframe() -> pd.DataFrame:
    """Đọc danh sách môn học từ output hoặc input"""
    paths = [
        project_root / "data" / "output" / "subjects_cleaned.csv",
        project_root / "data" / "input" / "subjects.csv",
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
        project_root / "data" / "output" / "student_profiles_cleaned.csv",
        project_root / "data" / "input" / "student_profile.csv",
    ]
    for path in paths:
        if path.exists():
            try:
                df = pd.read_csv(path)
                match = df[df["student_id"] == student_id]
                if not match.empty:
                    return match.iloc[0].to_dict()
            except Exception:
                continue
    return {}


def _save_student_dataframe(
    path: Path,
    student_id: str,
    df_new: pd.DataFrame,
    replace: bool = True,
    subset: Optional[List[str]] = None,
):
    """Ghi dữ liệu học sinh vào file CSV"""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            existing = pd.read_csv(path)
            if replace and "student_id" in existing.columns:
                existing = existing[existing["student_id"] != student_id]
            else:
                df_new = pd.concat([existing, df_new], ignore_index=True)
                if subset:
                    df_new = df_new.drop_duplicates(subset=subset, keep="last")
                    df_new = df_new.reset_index(drop=True)
                df_new.to_csv(path, index=False, encoding="utf-8")
                return
        except Exception:
            pass
    df_new.to_csv(path, index=False, encoding="utf-8")


def _save_student_input_data(student_id: str, synthetic_data: dict):
    """Ghi dữ liệu của học sinh vào các file input"""
    input_dir = project_root / "data" / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    if synthetic_data.get("profile") is not None:
        _save_student_dataframe(
            input_dir / "student_profile.csv", student_id, synthetic_data["profile"]
        )

    if synthetic_data.get("grades") is not None:
        _save_student_dataframe(
            input_dir / "grades.csv", student_id, synthetic_data["grades"]
        )

    if synthetic_data.get("feedback") is not None:
        _save_student_dataframe(
            input_dir / "teacher_feedback.csv",
            student_id,
            synthetic_data["feedback"],
        )


def _simple_ai_score(grade: float, attendance: float, homework: float) -> float:
    """Tính AI Score đơn giản từ điểm số và tỉ lệ"""
    attendance = attendance if attendance <= 1 else attendance / 100
    homework = homework if homework <= 1 else homework / 100
    grade_norm = grade / 10
    score = 0.5 * grade_norm + 0.25 * attendance + 0.25 * homework
    return round(max(0.0, min(1.0, score)), 4)


def generate_new_student_id(prefix: str = "HS") -> str:
    """Sinh mã học sinh mới chưa tồn tại"""
    existing_ids = set()

    def collect_ids(path: Path):
        if path.exists():
            try:
                df = pd.read_csv(path)
                if "student_id" in df.columns:
                    existing_ids.update(
                        df["student_id"].dropna().astype(str).tolist()
                    )
            except Exception:
                pass

    collect_ids(project_root / "data" / "input" / "student_profile.csv")
    collect_ids(project_root / "data" / "output" / "student_profiles_cleaned.csv")

    pattern = re.compile(rf"{prefix}(\d+)", re.IGNORECASE)
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
        n=min(6, len(subjects_df)), random_state=random.randint(1, 1_000_000)
    ).reset_index(drop=True)

    ai_scores = []
    grades = []
    recommendations = []

    feedback_rows = []

    for idx, subject in sample_subjects.iterrows():
        ai_score = round(random.uniform(0.45, 0.9), 4)
        ai_scores.append(
            {
                "student_id": student_id,
                "subject_code": subject.get("subject_code", f"SUB{idx:03d}"),
                "subject_name": subject.get("subject_name", "Môn học"),
                "ai_score": ai_score,
            }
        )

        grade_score = round(random.uniform(7.0, 9.5), 1)
        attendance = round(random.uniform(0.85, 0.98), 2)
        homework = round(random.uniform(0.82, 0.97), 2)
        semester = 1 if idx % 2 == 0 else 2
        year = 2024 + (idx // 4)
        grades.append(
            {
                "student_id": student_id,
                "subject_code": subject.get("subject_code", f"SUB{idx:03d}"),
                "grade_score": grade_score,
                "attendance_rate": attendance,
                "homework_completion": homework,
                "semester": semester,
                "year": year,
            }
        )

        recommendations.append(
            {
                "student_id": student_id,
                "subject_code": subject.get("subject_code", f"SUB{idx:03d}"),
                "subject_name": subject.get("subject_name", "Môn học"),
                "ai_score": ai_score,
                "priority": idx + 1,
                "reason": f"Môn học phù hợp với năng lực (AI Score: {ai_score:.2f})",
            }
        )

        feedback_rows.append(
            {
                "student_id": student_id,
                "subject_code": subject.get("subject_code", f"SUB{idx:03d}"),
                "teacher_id": f"AUTO{idx+1:03d}",
                "comment": "Dữ liệu tự sinh cho học sinh mới",
                "strengths": "Năng lực tốt, thái độ tích cực",
                "improvements": "Tiếp tục luyện tập và ôn bài",
                "semester": semester,
            }
        )
    feedback_df = pd.DataFrame(feedback_rows)
    ai_scores_df = pd.DataFrame(ai_scores)
    grades_df = pd.DataFrame(grades)
    recs_df = pd.DataFrame(recommendations).sort_values(
        by="ai_score", ascending=False
    ).head(10)

    profile = _load_student_profile(student_id)
    if not profile:
        sample_subject = sample_subjects.iloc[0] if not sample_subjects.empty else None
        profile = {
            "student_id": student_id,
            "name": full_name or f"Học sinh {student_id}",
            "major": sample_subject.get("category", "General")
            if sample_subject is not None
            else "General",
            "career_path": "engineering",
            "learning_style": random.choice(
                ["Visual", "Auditory", "Kinesthetic", "Mixed"]
            ),
            "interests": "Công nghệ, học tập",
            "goals": "Cải thiện kết quả học tập",
        }

    profile_df = pd.DataFrame([profile])

    return {
        "ai_scores": ai_scores_df,
        "grades": grades_df,
        "recommendations": recs_df,
        "feedback": feedback_df,
        "profile": profile_df,
    }


def initialize_student_data(student_id: str, full_name: str = None):
    """
    Đảm bảo học sinh mới đăng ký có dữ liệu hiển thị trên dashboard.
    Ưu tiên dùng dữ liệu thật nếu đã có, nếu không sẽ tạo dữ liệu giả lập.
    """
    output_dir = project_root / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        scores_df = None
        try:
            scores_df = predict_ai_scores(student_id)
        except Exception:
            scores_df = None

        if scores_df is not None and not scores_df.empty:
            _save_student_dataframe(output_dir / "ai_scores.csv", student_id, scores_df)
            recommendations = generate_recommendations(student_id, top_n=10)
            if recommendations:
                recs_df = pd.DataFrame(recommendations)
                _save_student_dataframe(
                    output_dir / "recommendations.csv", student_id, recs_df
                )
        else:
            synthetic = _create_synthetic_student_data(student_id, full_name)
            if synthetic:
                _save_student_dataframe(
                    output_dir / "ai_scores.csv", student_id, synthetic["ai_scores"]
                )
                _save_student_dataframe(
                    output_dir / "recommendations.csv",
                    student_id,
                    synthetic["recommendations"],
                )
                _save_student_dataframe(
                    output_dir / "grades_cleaned.csv",
                    student_id,
                    synthetic["grades"],
                )
                _save_student_dataframe(
                    output_dir / "student_profiles_cleaned.csv",
                    student_id,
                    synthetic["profile"],
                )
                if synthetic.get("feedback") is not None:
                    _save_student_dataframe(
                        output_dir / "feedback_cleaned.csv",
                        student_id,
                        synthetic["feedback"],
                    )

                _save_student_input_data(student_id, synthetic)
                return

        # Nếu có profile thật, đảm bảo ghi ra output
        profile = _load_student_profile(student_id)
        if profile:
            profile_df = pd.DataFrame([profile])
            _save_student_dataframe(
                output_dir / "student_profiles_cleaned.csv", student_id, profile_df
            )
    except Exception:
        # Không để lỗi đăng ký chỉ vì tạo dữ liệu thất bại
        pass


def _get_subject_load_for_student(student_id: str) -> List[Dict]:
    """Lấy cấu hình số buổi/tuần cho từng môn của học sinh từ DB"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT subject_code, subject_name, lessons_per_week
            FROM student_subject_load
            WHERE student_id = ?
            ORDER BY subject_code
            """,
            (student_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "subject_code": r[0],
                "subject_name": r[1] or "",
                "lessons_per_week": r[2] or 0,
            }
            for r in rows
        ]
    except Exception:
        return []


def _get_timetable_meta_for_student(student_id: str) -> Optional[Dict]:
    """Lấy thông tin meta về thời khóa biểu (thời gian cập nhật gần nhất)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT last_updated FROM student_timetable_meta WHERE student_id = ?",
            (student_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if row and row[0]:
            return {
                'last_updated': row[0],
            }
        return None
    except Exception:
        return None


def _save_subject_load_for_student(student_id: str, subjects: List[Dict]) -> None:
    """Ghi cấu hình số buổi/tuần cho từng môn của học sinh vào DB"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM student_subject_load WHERE student_id = ?",
            (student_id,),
        )
        for item in subjects:
            if not item.get("subject_code"):
                continue
            cursor.execute(
                """
                INSERT INTO student_subject_load
                (student_id, subject_code, subject_name, lessons_per_week)
                VALUES (?, ?, ?, ?)
                """,
                (
                    student_id,
                    item.get("subject_code"),
                    item.get("subject_name") or "",
                    int(item.get("lessons_per_week") or 0),
                ),
            )
        # Cập nhật thời gian chỉnh sửa TKB gần nhất
        try:
            cursor.execute(
                """
                INSERT INTO student_timetable_meta (student_id, last_updated)
                VALUES (?, CURRENT_TIMESTAMP)
                ON CONFLICT(student_id) DO UPDATE SET last_updated = CURRENT_TIMESTAMP
                """,
                (student_id,),
            )
        except Exception:
            # Nếu bảng meta chưa tồn tại hoặc lỗi, bỏ qua để không làm hỏng luồng chính
            pass
        conn.commit()
    finally:
        conn.close()


