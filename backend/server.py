"""Production server - Waitress + static files"""
import os
from flask import Flask, send_from_directory, g
from flask_cors import CORS
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from waitress import serve

from config import Config
from auth import auth_bp
from courses import courses_bp
from reviews import reviews_bp
from teachers import teachers_bp
from categories import categories_bp
from admin import admin_bp
from my import my_bp
from chat import chat_bp

conf = Config()

print(f'DB: {conf.SQLALCHEMY_DATABASE_URI[:60]}...')

engine = create_engine(conf.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)


def init_database():
    try:
        inspector = inspect(engine)
        existing = inspector.get_table_names()
        print(f'Tables: {existing}')
        if 'users' not in existing:
            from models import Base
            Base.metadata.create_all(engine)
            print(f'Created: {inspect(engine).get_table_names()}')
        else:
            print('DB OK')

        sql_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        count = 0
        with engine.begin() as conn:
            for stmt in content.split(';'):
                stmt = stmt.strip()
                if stmt.upper().startswith('INSERT'):
                    try:
                        conn.execute(text(stmt))
                        count += 1
                    except Exception:
                        pass
        print(f'Seeded {count} rows')
    except Exception as e:
        print(f'Init error: {e}')


init_database()

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend', 'dist'))

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')
app.config['SECRET_KEY'] = conf.SECRET_KEY

CORS(app, origins='*', supports_credentials=True)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(courses_bp, url_prefix
