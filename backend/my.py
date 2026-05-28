"""个人中心蓝图"""
from flask import Blueprint, request, g
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Review, Course, Teacher, Category
from utils import success, paginated, login_required

my_bp = Blueprint('my', __name__)


@my_bp.route('/my/reviews', methods=['GET'])
@login_required
def my_reviews():
    session: Session = g.db_session
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = select(Review).where(Review.user_id == g.user_id)
    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    reviews = session.execute(
        query.order_by(Review.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    ).scalars().all()

    items = []
    for r in reviews:
        course = session.get(Course, r.course_id)
        items.append({
            'id': r.id,
            'course_id': r.course_id,
            'course_name': course.name if course else '(已删除)',
            'rating_teaching': r.rating_teaching,
            'rating_content': r.rating_content,
            'rating_exam': r.rating_exam,
            'rating_fairness': r.rating_fairness,
            'comment': r.comment,
            'created_at': r.created_at.isoformat() if r.created_at else None
        })

    return success(paginated(items, total, page, per_page))


@my_bp.route('/my/courses', methods=['GET'])
@login_required
def my_courses():
    session: Session = g.db_session
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = select(Course).where(Course.created_by == g.user_id)
    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    courses = session.execute(
        query.order_by(Course.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    ).scalars().all()

    items = []
    for c in courses:
        teacher = session.get(Teacher, c.teacher_id)
        category = session.get(Category, c.category_id)
        items.append({
            'id': c.id,
            'name': c.name,
            'teacher': {'id': teacher.id, 'name': teacher.name} if teacher else None,
            'category': {'id': category.id, 'name': category.name} if category else None,
            'semester': c.semester,
            'status': c.status,
            'reject_reason': c.reject_reason,
            'created_at': c.created_at.isoformat() if c.created_at else None
        })

    return success(paginated(items, total, page, per_page))
