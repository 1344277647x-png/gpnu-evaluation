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

print(f'DB URI: {conf.SQLALCHEMY_DATABASE_URI[:80]}...')

engine = create_engine(conf.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)

def init_database():
    try:
        inspector = inspect(engine)
        existing = inspector.get_table_names()
        print(f'Existing tables: {existing}')
        if 'users' in existing and 'courses' in existing:
            print('Database OK')
            return
        print('Creating tables via SQLAlchemy...')
        from models import Base
        Base.metadata.create_all(engine)
        
        # Run only the INSERT data from init_db.sql
        sql_path = os.path.join(os.path.dirname(__file__), 'init_db.sql')
        with open(sql_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with engine.begin() as conn:
            for stmt in content.split(';'):
                stmt = stmt.strip()
                if stmt.upper().startswith('INSERT'):
                    try:
                        conn.execute(text(stmt))
                    except Exception as e:
                        print(f'  Skip INSERT: {str(e)[:100]}')
        
        final = inspect(engine).get_table_names()
        print(f'Tables after init: {final}')
    except Exception as e:
        print(f'DB init failed: {str(e)[:200]}')
