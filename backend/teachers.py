"""Teachers blueprint"""
from flask import Blueprint, request, g
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Teacher
from utils import success, error, paginated, admin_required, login_required, validate_required

teachers_bp = Blueprint('teachers', __name__)


@teachers_bp.route('', methods=['GET'])
def list_teachers():
    session: Session = g.db_session
    search = (request.args.get('search') or '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = select(Teacher)
    if search:
        query = query.where(Teacher.name.contains(search))
    query = query.order_by(Teacher.name.asc())

    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    teachers = session.execute(
        query.offset((page - 1) * per_page).limit(per_page)
    ).scalars().all()

    items = [{'id': t.id, 'name': t.name, 'department': t.department} for t in teachers]
    return success(paginated(items, total, page, per_page))


@teachers_bp.route('', methods=['POST'])
@login_required
def create_teacher():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    department = (data.get('department') or '').strip()

    ok, msg = validate_required(name, 'Teacher name', 100)
    if not ok:
        return error(msg, 400)

    session: Session = g.db_session
    teacher = Teacher(name=name, department=department)
    session.add(teacher)
    session.commit()
    return success({'id': teacher.id}, 'Teacher added', 201)


@teachers_bp.route('/<int:teacher_id>', methods=['PUT'])
@admin_required
def update_teacher(teacher_id):
    data = request.get_json(silent=True) or {}
    session: Session = g.db_session
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        return error('Teacher not found', 404)

    if 'name' in data:
        teacher.name = (data['name'] or '').strip()
    if 'department' in data:
        teacher.department = (data['department'] or '').strip()
    session.commit()
    return success(message='Teacher updated')
