# Step 8: Interview Question Generator & Knowledge Bank

INTERVIEW_QUESTION_BANK = {
    "Python": [
        {"q": "What is a list in Python, and how does it differ from a tuple?", "a": "A list is a mutable ordered sequence of elements, while a tuple is immutable once created."},
        {"q": "Explain the difference between deep copy and shallow copy in Python.", "a": "Shallow copy creates a new object but references inner nested objects; deep copy recursively copies all nested objects."},
        {"q": "What are decorators in Python and how do they work?", "a": "A decorator is a design pattern used to modify or extend the behavior of a function or class without altering its source code."},
        {"q": "How does memory management and garbage collection work in Python?", "a": "Python uses reference counting as its primary GC mechanism, supplemented by a generational cyclic garbage collector."}
    ],
    "SQL": [
        {"q": "What is a JOIN in SQL? Explain INNER JOIN vs LEFT JOIN.", "a": "A JOIN combines rows from two or more tables based on a related column. INNER JOIN returns only matching rows; LEFT JOIN returns all rows from the left table and matched rows from the right."},
        {"q": "Explain Primary Key vs Foreign Key.", "a": "A Primary Key uniquely identifies each row in a table. A Foreign Key is a field in one table that refers to the Primary Key in another table to enforce referential integrity."},
        {"q": "What is the difference between WHERE and HAVING clauses?", "a": "WHERE filters individual rows before grouping; HAVING filters aggregated group data after GROUP BY."},
        {"q": "What is Database Indexing and why is it used?", "a": "An index is a data structure (e.g., B-Tree) that speeds up data retrieval operations on a table at the cost of additional storage and write speed."}
    ],
    "Flask": [
        {"q": "What is Flask and how does request routing work in Flask?", "a": "Flask is a lightweight WSGI web framework in Python. Routing matches URL paths to view functions using the @app.route() decorator."},
        {"q": "Explain Flask application contexts and request contexts.", "a": "Request context keeps track of request-level data like request.args or session. Application context manages app-level state like g or current_app."},
        {"q": "How do you handle user authentication and session security in Flask?", "a": "Using Werkzeug password hashing, secure session cookies (SECRET_KEY), and session dicts or Flask-Login extension."}
    ],
    "Machine Learning": [
        {"q": "What is the difference between Supervised and Unsupervised Learning?", "a": "Supervised learning trains on labeled data to predict target outputs; unsupervised learning discovers patterns and clusters in unlabeled data."},
        {"q": "Explain Overfitting and Underfitting, and how to prevent them.", "a": "Overfitting occurs when a model learns noise in training data; underfitting happens when a model is too simple. Prevent overfitting using cross-validation, regularization, and dropout."},
        {"q": "What is Bias-Variance Tradeoff?", "a": "Bias is error from wrong assumptions; variance is sensitivity to small fluctuations in training data. Optimal models balance both for low total error."}
    ],
    "Data Science": [
        {"q": "What is Data Normalization vs Standardization?", "a": "Normalization scales features to a [0,1] range; Standardization centers data to zero mean and unit variance (z-score)."},
        {"q": "Explain the steps involved in exploratory data analysis (EDA).", "a": "EDA includes inspecting distributions, checking missing values, identifying outliers, finding feature correlations, and visualizing trends."}
    ],
    "HTML": [
        {"q": "What are semantic HTML tags and why are they important?", "a": "Semantic tags like <header>, <article>, and <footer> clearly describe their meaning to browsers, developers, and search engines for better accessibility and SEO."},
        {"q": "What is the difference between block-level and inline elements?", "a": "Block-level elements start on a new line and take up full container width; inline elements take up only as much width as necessary."}
    ],
    "CSS": [
        {"q": "Explain CSS Flexbox vs CSS Grid.", "a": "Flexbox is designed for 1-dimensional layouts (rows or columns); CSS Grid is designed for 2-dimensional layouts (rows and columns simultaneously)."},
        {"q": "What is the CSS Box Model?", "a": "The box model consists of content, padding, border, and margin that dictate element dimensions and layout spacing."}
    ],
    "JavaScript": [
        {"q": "What is the Event Loop in JavaScript?", "a": "The event loop is a single-threaded loop that monitors the call stack and callback queue to handle asynchronous non-blocking executions."},
        {"q": "What is the difference between let, const, and var?", "a": "var is function-scoped and hoisted; let and const are block-scoped. const variables cannot be reassigned."}
    ],
    "Git": [
        {"q": "What is the difference between git merge and git rebase?", "a": "git merge combines branches with a merge commit maintaining history; git rebase rewrites commits sequentially onto another branch for a linear history."},
        {"q": "How do you resolve merge conflicts in Git?", "a": "Inspect conflicted files, manually select desired code blocks, remove conflict markers, stage changes with git add, and commit."}
    ],
    "Docker": [
        {"q": "What is the difference between a Docker Image and a Docker Container?", "a": "A Docker Image is an immutable read-only blueprint; a Docker Container is a running instance of an image."}
    ],
    "AWS": [
        {"q": "What is AWS EC2 vs S3?", "a": "EC2 provides scalable cloud virtual computing servers; S3 provides secure object storage for files and assets."}
    ]
}

def generate_interview_questions(extracted_skills):
    """
    Step 8: Generate targeted interview questions according to student's extracted skills.
    """
    if not extracted_skills:
        extracted_skills = ["Python", "SQL"]  # Default starter set if no skills extracted yet
        
    result = []
    for skill in extracted_skills:
        if skill in INTERVIEW_QUESTION_BANK:
            result.append({
                "skill": skill,
                "questions": INTERVIEW_QUESTION_BANK[skill]
            })
        else:
            # Fallback dynamic generic questions for uncommon skills
            result.append({
                "skill": skill,
                "questions": [
                    {"q": f"Explain the core concepts and use cases of {skill}.", "a": f"{skill} is utilized for specialized software tasks, automation, or enterprise architecture."},
                    {"q": f"What are best practices when building applications with {skill}?", "a": "Focus on modular architecture, security, performance optimization, and clean documentation."}
                ]
            })
            
    return result
