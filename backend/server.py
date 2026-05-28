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
        print(f'Tables before: {existing}')
        if 'users' in existing and 'courses' in existing:
            print('DB OK')
        else:
            print('Creating tables...')
            from models import Base
            Base.metadata.create_all(engine)
            print(f'Created: {inspect(engine).get_table_names()}')

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
        print(f'Inserted {count} data blocks')
    except Exception as e:
        print(f'DB init error: {e}')

init_database()

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'frontend', 'dist'))

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')
app.config['SECRET_KEY'] = conf.SECRET_KEY

CORS(app, origins='*', supports_credentials=True)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(reviews_bp, url_prefix='/api')
app.register_blueprint(teachers_bp, url_prefix='/api/teachers')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(my_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, 'index.html')


@app.before_request
def open_db():
    g.db_session = SessionLocal()


@app.teardown_request
def close_db(exc):
    session = g.pop('db_session', None)
    if session:
        session.close()


if __name__ == '__main__':
    print(f'Static: {STATIC_DIR}')
    port = 5000
    print(f'Serving on http://0.0.0.0:{port}')
    serve(app, host='0.0.0.0', port=port, threads=8)
