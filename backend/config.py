"""Application config"""
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'gpnu-eval-secret-key-change-in-production')
    JWT_ACCESS_EXPIRES = 2 * 3600       # 2 hours
    JWT_REFRESH_EXPIRES = 7 * 86400     # 7 days

    # Railway provides: MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD, MYSQLDATABASE
    # Local fallback uses explicit DB_* vars
    DB_HOST = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST', 'localhost')
    DB_PORT = int(os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT', 3306))
    DB_USER = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD', '626957')
    DB_NAME = os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME', 'railway')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset=utf8mb4'

    PER_PAGE_COURSES = 12
    PER_PAGE_REVIEWS = 10
