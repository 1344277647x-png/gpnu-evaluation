"""Flask application entry"""
from flask import Flask, g
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

engine = create_engine(conf.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = conf.SECRET_KEY

CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'], supports_credentials=True)

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(reviews_bp, url_prefix='/api')
app.register_blueprint(teachers_bp, url_prefix='/api/teachers')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(my_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')


@app.before_request
def open_db():
    g.db_session = SessionLocal()


@app.teardown_request
def close_db(exc):
    session = g.pop('db_session', None)
    if session:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
