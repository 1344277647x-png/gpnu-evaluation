"""Application config"""
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gpnu-eval-secret-key-change-in-production')
    JWT_ACCESS_EXPIRES = 2 * 3600       # 2 hours
    JWT_REFRESH_EXPIRES = 7 * 86400     # 7 days

    PER_PAGE_COURSES = 12
    PER_PAGE_REVIEWS = 10

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # Railway provides MYSQL_URL as a complete connection string
        mysql_url = os.environ.get('MYSQL_URL')
        if mysql_url:
            return mysql_url.replace('mysql://', 'mysql+pymysql://', 1)
        # Fallback for local dev
        host = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST', 'localhost')
        port = int(os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT', 3306))
        user = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER', 'root')
        pwd = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD', '')
        db = os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME', 'gpnu_evaluation')
        return f'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8mb4'
