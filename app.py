import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from models.database import (
    init_db, get_student_by_email, get_student_by_id, create_student,
    save_resume, get_latest_resume, get_all_students_admin, get_all_resumes_admin
)
from models.parser import extract_resume_text, extract_skills
from models.readiness import calculate_resume_score, calculate_placement_readiness
from models.recommender import recommend_jobs, recommend_courses
from models.question_bank import generate_interview_questions

app = Flask(__name__)
app.config.from_object(Config)

# Ensure uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database on startup
init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# --- Helper Decorators & Helpers ---
def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('role') == 'admin'


# --- Routes ---

@app.route('/')
def index():
    if is_logged_in():
        if is_admin():
            return redirect(url_for('admin_panel'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


# Step 2: Student Login & Registration
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        student = get_student_by_email(email)
        if student and check_password_hash(student['password'], password):
            session['user_id'] = student['id']
            session['user_name'] = student['name']
            session['user_email'] = student['email']
            session['role'] = student['role']
            flash(f"Welcome back, {student['name']}!", "success")
            
            if student['role'] == 'admin':
                return redirect(url_for('admin_panel'))
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        department = request.form.get('department', '')
        year = int(request.form.get('year', 4))
        cgpa = float(request.form.get('cgpa', 0.0))

        if get_student_by_email(email):
            flash("A student with this email address already exists.", "warning")
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)
        student_id = create_student(name, email, password_hash, department, year, cgpa, role='student')
        
        session['user_id'] = student_id
        session['user_name'] = name
        session['user_email'] = email
        session['role'] = 'student'
        
        flash("Registration successful! Welcome to SkillBridge AI.", "success")
        return redirect(url_for('upload_resume'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


# Step 3: Resume Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if not is_logged_in() or is_admin():
        return redirect(url_for('login'))

    student_id = session['user_id']
    student = get_student_by_id(student_id)
    latest_resume = get_latest_resume(student_id)

    if request.method == 'POST':
        if 'resume_file' not in request.files:
            flash("No file part in request.", "danger")
            return redirect(request.url)
            
        file = request.files['resume_file']
        if file.filename == '':
            flash("No file selected.", "danger")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Step 3 & 4: Extract text & identify skills
            extracted_text = extract_resume_text(file_path)
            extracted_skills = extract_skills(extracted_text)
            skills_str = ", ".join(extracted_skills)

            # Step 5: Resume Score
            resume_score = calculate_resume_score(extracted_skills, extracted_text)

            # Step 9: Placement Readiness Score
            placement_score = calculate_placement_readiness(
                resume_score=resume_score,
                cgpa=student['cgpa'],
                skill_count=len(extracted_skills)
            )

            # Step 12: Store details in database
            save_resume(
                student_id=student_id,
                resume_name=filename,
                resume_score=resume_score,
                placement_score=placement_score,
                skills_str=skills_str,
                extracted_text=extracted_text
            )

            flash(f"Resume uploaded and analyzed successfully! Extracted {len(extracted_skills)} technical skills.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid file format. Please upload a PDF or DOCX file.", "danger")

    return render_template('upload.html', student=student, latest_resume=latest_resume)


# Step 10: Student Dashboard
@app.route('/dashboard')
def dashboard():
    if not is_logged_in() or is_admin():
        return redirect(url_for('login'))

    student_id = session['user_id']
    student = get_student_by_id(student_id)
    latest_resume = get_latest_resume(student_id)

    if not latest_resume:
        return render_template(
            'dashboard.html',
            student=student,
            resume=None,
            skills=[],
            jobs=[],
            courses=[],
            interview_questions=[],
            placement_readiness=0
        )

    # Parse stored skills list
    skills_list = [s.strip() for s in latest_resume['skills'].split(',')] if latest_resume['skills'] else []

    # Step 6: Job Recommendations
    job_recommendations = recommend_jobs(skills_list)

    # Collect missing skills across recommended top job roles
    all_missing_skills = []
    for job in job_recommendations[:3]:  # Top 3 jobs
        all_missing_skills.extend(job['missing_skills'])

    # Step 7: Course Recommendations
    course_recommendations = recommend_courses(all_missing_skills)

    # Step 8: Interview Questions
    interview_questions = generate_interview_questions(skills_list)

    # Step 9: Placement Readiness Score
    placement_readiness = latest_resume.get('placement_score', 0)
    if not placement_readiness:
        placement_readiness = calculate_placement_readiness(
            resume_score=latest_resume['resume_score'],
            cgpa=student['cgpa'],
            skill_count=len(skills_list)
        )

    return render_template(
        'dashboard.html',
        student=student,
        resume=latest_resume,
        skills=skills_list,
        jobs=job_recommendations,
        courses=course_recommendations,
        interview_questions=interview_questions,
        placement_readiness=placement_readiness
    )


# Step 11: Admin Panel
@app.route('/admin')
def admin_panel():
    if not is_logged_in() or not is_admin():
        flash("Admin credentials required to view admin panel.", "warning")
        return redirect(url_for('login'))

    students = get_all_students_admin()
    resumes = get_all_resumes_admin()

    resumes_count = len(resumes)
    avg_resume_score = (sum(r['resume_score'] for r in resumes) / resumes_count) if resumes_count > 0 else 0
    avg_placement_score = (sum(r['placement_score'] for r in resumes) / resumes_count) if resumes_count > 0 else 0

    return render_template(
        'admin.html',
        students=students,
        resumes_count=resumes_count,
        avg_resume_score=avg_resume_score,
        avg_placement_score=avg_placement_score
    )


@app.route('/admin/export_csv')
def export_admin_csv():
    if not is_logged_in() or not is_admin():
        return redirect(url_for('login'))

    import csv
    from io import StringIO
    from flask import Response

    students = get_all_students_admin()
    si = StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['ID', 'Name', 'Email', 'Department', 'Year', 'CGPA', 'Resume Score (%)', 'Placement Readiness (%)', 'Extracted Skills', 'Uploaded File'])
    
    for s in students:
        cw.writerow([
            s.get('id', ''),
            s.get('name', ''),
            s.get('email', ''),
            s.get('department', ''),
            s.get('year', ''),
            s.get('cgpa', ''),
            s.get('resume_score', 'N/A'),
            s.get('placement_score', 'N/A'),
            s.get('skills', ''),
            s.get('resume_name', '')
        ])

    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=skillbridge_students_readiness_report.csv"}
    )


if __name__ == '__main__':
    print("[SkillBridge AI] Starting Flask Server on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
