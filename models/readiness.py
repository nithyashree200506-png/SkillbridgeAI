# Resume Score & Placement Readiness Calculator

def calculate_resume_score(extracted_skills, raw_text=""):
    """
    Step 5: Calculate Resume Score out of 100% based on skill coverage & content signals.
    """
    skill_count = len(extracted_skills)
    
    # 1. Skill Score component (max 65 points)
    # Benchmark: 12 key technical skills for a top-tier profile
    skill_score = min(65.0, (skill_count / 12.0) * 65.0)
    
    # 2. Content & Structural Depth component (max 35 points)
    content_score = 0.0
    text_lower = raw_text.lower() if raw_text else ""
    word_count = len(text_lower.split())
    
    # Word count points (max 15 pts)
    if word_count > 300:
        content_score += 15
    elif word_count > 150:
        content_score += 10
    elif word_count > 50:
        content_score += 5
        
    # Structural keywords check (max 20 pts, 4 pts each)
    sections = ["education", "project", "experience", "certification", "skill"]
    for sec in sections:
        if sec in text_lower:
            content_score += 4.0

    total_score = round(skill_score + content_score, 1)
    return min(100.0, max(0.0, total_score))


def calculate_placement_readiness(resume_score, cgpa, skill_count):
    """
    Step 9: Calculate Placement Readiness Score (%) using CGPA, Resume Score, and Skills.
    Example:
      Resume Score: 80
      CGPA: 8.4
      Skills: 12
      Placement Readiness: ~87%
    """
    # 1. Resume Score Weight (45%)
    w_resume = (resume_score / 100.0) * 45.0
    
    # 2. CGPA Weight (35%) -> CGPA out of 10 scaled to 100
    cgpa_percentage = (min(10.0, max(0.0, float(cgpa))) / 10.0) * 100.0
    w_cgpa = (cgpa_percentage / 100.0) * 35.0
    
    # 3. Skill Count Weight (20%) -> 10+ skills gets max weight
    skill_percentage = min(100.0, (skill_count / 10.0) * 100.0)
    w_skill = (skill_percentage / 100.0) * 20.0
    
    readiness = round(w_resume + w_cgpa + w_skill, 1)
    return min(100.0, max(0.0, readiness))
