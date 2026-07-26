from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Job Catalog with Target Skills
JOB_PROFILES = [
    {
        "title": "Python Developer",
        "category": "Software Engineering",
        "description": "Develop scalable backend systems, APIs, and microservices using Python and web frameworks.",
        "required_skills": ["Python", "SQL", "Flask", "Django", "Git", "REST API", "PostgreSQL"],
        "badge": "Primary Role"
    },
    {
        "title": "AI / ML Engineer",
        "category": "Artificial Intelligence",
        "description": "Design, build, and deploy machine learning models, neural networks, and AI algorithms.",
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "AI", "Scikit-Learn", "TensorFlow", "PyTorch", "NumPy"],
        "badge": "High Demand"
    },
    {
        "title": "Web Developer",
        "category": "Frontend / Full Stack",
        "description": "Build interactive, modern web applications, user interfaces, and responsive client experiences.",
        "required_skills": ["HTML", "CSS", "JavaScript", "Bootstrap", "React", "Node.js", "Flask", "Git"],
        "badge": "Hot Market"
    },
    {
        "title": "Data Analyst / Scientist",
        "category": "Data & Analytics",
        "description": "Analyze data, discover insights, generate statistical visualizations, and drive decision-making.",
        "required_skills": ["Python", "SQL", "Data Science", "Pandas", "NumPy", "Matplotlib", "Tableau", "Power BI"],
        "badge": "Top Choice"
    },
    {
        "title": "DevOps & Cloud Engineer",
        "category": "Infrastructure",
        "description": "Automate deployments, manage cloud infrastructure, containers, and continuous deployment pipelines.",
        "required_skills": ["Linux", "Git", "Docker", "Kubernetes", "AWS", "Python", "SQL"],
        "badge": "Fast Growing"
    },
    {
        "title": "Full Stack Engineer",
        "category": "Software Engineering",
        "description": "Handle both client-side and server-side development end-to-end.",
        "required_skills": ["Python", "JavaScript", "HTML", "CSS", "SQL", "Flask", "React", "MongoDB", "Git"],
        "badge": "Versatile"
    }
]

# Course Mapping Catalog for Missing Skills
COURSE_CATALOG = {
    "Python": {
        "title": "Python Programming Masterclass",
        "platform": "SkillBridge Academy",
        "duration": "10 Hours",
        "url": "#"
    },
    "SQL": {
        "title": "Mastering SQL & Database Design",
        "platform": "SkillBridge Academy",
        "duration": "8 Hours",
        "url": "#"
    },
    "Flask": {
        "title": "Introduction to Flask Web Development",
        "platform": "SkillBridge Academy",
        "duration": "6 Hours",
        "url": "#"
    },
    "Machine Learning": {
        "title": "Machine Learning A-Z: Hands-on Python",
        "platform": "SkillBridge AI Lab",
        "duration": "16 Hours",
        "url": "#"
    },
    "Data Science": {
        "title": "Data Science Fundamentals with Pandas & NumPy",
        "platform": "SkillBridge AI Lab",
        "duration": "12 Hours",
        "url": "#"
    },
    "HTML": {
        "title": "Modern HTML5 & Semantic Web Design",
        "platform": "SkillBridge Academy",
        "duration": "4 Hours",
        "url": "#"
    },
    "CSS": {
        "title": "CSS3, Flexbox, Grid & UI Animations",
        "platform": "SkillBridge Academy",
        "duration": "6 Hours",
        "url": "#"
    },
    "JavaScript": {
        "title": "Modern JavaScript (ES6+) Complete Bootcamp",
        "platform": "SkillBridge Academy",
        "duration": "10 Hours",
        "url": "#"
    },
    "React": {
        "title": "React.js Front-End Engineering",
        "platform": "SkillBridge Academy",
        "duration": "12 Hours",
        "url": "#"
    },
    "Git": {
        "title": "Git & GitHub Version Control Essentials",
        "platform": "SkillBridge Academy",
        "duration": "3 Hours",
        "url": "#"
    },
    "Docker": {
        "title": "Docker Containers for Beginners",
        "platform": "SkillBridge Cloud",
        "duration": "5 Hours",
        "url": "#"
    },
    "AWS": {
        "title": "AWS Cloud Practitioner & Deployment Essentials",
        "platform": "SkillBridge Cloud",
        "duration": "14 Hours",
        "url": "#"
    },
    "Deep Learning": {
        "title": "Deep Learning & Neural Networks with PyTorch",
        "platform": "SkillBridge AI Lab",
        "duration": "18 Hours",
        "url": "#"
    }
}


def recommend_jobs(user_skills):
    """
    Step 6: Job Recommendation using Scikit-Learn TF-IDF + Cosine Similarity
    """
    if not user_skills:
        user_skills = []
        
    user_skill_str = " ".join(user_skills)
    job_texts = [" ".join(job["required_skills"]) for job in JOB_PROFILES]
    
    # Corpus: User skills + Job profiles
    corpus = [user_skill_str] + job_texts
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calculate Cosine Similarity of User (index 0) with all Jobs (indices 1..)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    recommendations = []
    for idx, job in enumerate(JOB_PROFILES):
        # Calculate overlap-based match & TF-IDF match combined
        user_set = set(s.lower() for s in user_skills)
        job_req_set = set(s.lower() for s in job["required_skills"])
        
        matched_skills = [s for s in job["required_skills"] if s.lower() in user_set]
        missing_skills = [s for s in job["required_skills"] if s.lower() not in user_set]
        
        # Raw overlap percentage
        overlap_score = (len(matched_skills) / len(job["required_skills"])) * 100.0 if job["required_skills"] else 0
        
        # TF-IDF Cosine Similarity percentage
        tfidf_score = similarities[idx] * 100.0
        
        # Combined match percentage (weighted)
        final_match_pct = round(0.6 * overlap_score + 0.4 * tfidf_score, 1)
        
        recommendations.append({
            "title": job["title"],
            "category": job["category"],
            "description": job["description"],
            "badge": job["badge"],
            "match_pct": final_match_pct,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "required_skills": job["required_skills"]
        })
        
    # Sort recommendations by match percentage descending
    recommendations.sort(key=lambda x: x["match_pct"], reverse=True)
    return recommendations


def recommend_courses(missing_skills):
    """
    Step 7: Recommend courses based on missing skills.
    """
    courses = []
    seen = set()
    for skill in missing_skills:
        if skill not in seen:
            seen.add(skill)
            if skill in COURSE_CATALOG:
                course_info = COURSE_CATALOG[skill]
                courses.append({
                    "missing_skill": skill,
                    "course_title": course_info["title"],
                    "platform": course_info["platform"],
                    "duration": course_info["duration"],
                    "url": course_info["url"]
                })
            else:
                courses.append({
                    "missing_skill": skill,
                    "course_title": f"Complete Guide to {skill}",
                    "platform": "SkillBridge Learning Hub",
                    "duration": "6 Hours",
                    "url": "#"
                })
    return courses
