import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'skillbridge_ai_super_secret_key_2026')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}

    # Database setup: SQLite as fallback for zero-config run, PyMySQL for MySQL
    DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')  # 'sqlite' or 'mysql'
    
    # SQLite config
    SQLITE_DB_PATH = os.path.join(BASE_DIR, 'skillbridge.db')
    
    # MySQL config
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'skillbridge_db')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
