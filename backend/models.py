"""SQLAlchemy model definitions"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Enum, ForeignKey, UniqueConstraint, Index, create_engine
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=False)
    student_id = Column(String(20), nullable=False)
    role = Column(Enum('student', 'admin'), nullable=False, default='student')
    is_active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.now)

    courses = relationship('Course', back_populates='creator')
    reviews = relationship('Review', back_populates='user')


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Integer, nullable=False, default=1)

    courses = relationship('Course', back_populates='category')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False, default='')
    created_at = Column(DateTime, default=datetime.now)

    courses = relationship('Course', back_populates='teacher')


class Course(Base):
    __tablename__ = 'courses'
    __table_args__ = (
        UniqueConstraint('name', 'teacher_id', 'semester', name='idx_course_unique'),
        Index('idx_course_status', 'status'),
        Index('idx_course_teacher', 'teacher_id'),
        Index('idx_course_category', 'category_id'),
        Index('idx_course_created', 'created_at'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    semester = Column(String(20), nullable=False, default='')
    description = Column(Text)
    status = Column(Enum('pending', 'approved', 'rejected', 'inactive'), nullable=False, default='pending')
    reject_reason = Column(String(500))
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    category = relationship('Category', back_populates='courses')
    teacher = relationship('Teacher', back_populates='courses')
    creator = relationship('User', back_populates='courses')
    reviews = relationship('Review', back_populates='course')


class Review(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        UniqueConstraint('user_id', 'course_id', name='idx_review_unique'),
        Index('idx_review_course', 'course_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating_teaching = Column(Integer, nullable=False)
    rating_content = Column(Integer, nullable=False)
    rating_exam = Column(Integer, nullable=False)
    rating_fairness = Column(Integer, nullable=False)
    comment = Column(Text)
    is_hidden = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)

    course = relationship('Course', back_populates='reviews')
    user = relationship('User', back_populates='reviews')


class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    __table_args__ = (
        Index('idx_chat_session', 'session_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(64), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('User')
