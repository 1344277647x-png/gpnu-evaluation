"""管理蓝图"""
from flask import Blueprint, request, g
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import User, Course, Review
from utils import success, error, paginated, admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def list_users():
    session: Session = g.db_session
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = (request.args.get('search') or '').strip()

    query = select(User)
    if search:
        query = query.where(
            func.lower(User.username).contains(search.lower()) |
            func.lower(User.nickname).contains(search.lower())
        )
    query = query.order_by(User.created_at.desc())

    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    users = session.execute(query.offset((page - 1) * per_page).limit(per_page)).scalars().all()

    items = [{
        'id': u.id, 'username': u.username, 'nickname': u.nickname,
        'student_id': u.student_id, 'role': u.role, 'is_active': u.is_active,
        'created_at': u.created_at.isoformat() if u.created_at else None
    } for u in users]

    return success(paginated(items, total, page, per_page))


@admin_bp.route('/admin/users/<int:user_id>/toggle', methods=['PUT'])
@admin_required
def toggle_user(user_id):
    session: Session = g.db_session
    user = session.get(User, user_id)
    if not user:
        return error('用户不存在', 404)
    if user.role == 'admin':
        return error('不能禁用管理员账号', 400)
    user.is_active = 1 - user.is_active
    session.commit()
    return success(message='用户已禁用' if not user.is_active else '用户已启用')


@admin_bp.route('/admin/stats', methods=['GET'])
@admin_required
def stats():
    session: Session = g.db_session

    course_count = session.execute(select(func.count()).select_from(Course)).scalar()
    approved_count = session.execute(
        select(func.count()).where(Course.status == 'approved')
    ).scalar()
    pending_count = session.execute(
        select(func.count()).where(Course.status == 'pending')
    ).scalar()
    review_count = session.execute(select(func.count()).select_from(Review)).scalar()
    user_count = session.execute(select(func.count()).select_from(User)).scalar()

    return success({
        'course_count': course_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'review_count': review_count,
        'user_count': user_count
    })
