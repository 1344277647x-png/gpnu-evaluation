"""课程蓝图"""
from flask import Blueprint, request, g
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.orm import Session, joinedload

from models import Course, Review, Teacher, Category, User
from utils import success, error, paginated, login_required, admin_required, validate_required

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('', methods=['GET'])
def list_courses():
    session: Session = g.db_session

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    search = (request.args.get('search') or '').strip()
    category_id = request.args.get('category_id', type=int)
    teacher_id = request.args.get('teacher_id', type=int)
    semester = request.args.get('semester', '').strip()
    sort = request.args.get('sort', 'rating')  # rating | newest

    # 子查询：每个课程的平均评分
    avg_sub = (
        select(
            Review.course_id,
            (func.avg(
                (Review.rating_teaching + Review.rating_content + Review.rating_exam + Review.rating_fairness) / 4.0
            )).label('avg_rating'),
            func.count(Review.id).label('review_count')
        )
        .where(Review.is_hidden == 0)
        .group_by(Review.course_id)
        .subquery()
    )

    query = (
        select(Course, avg_sub.c.avg_rating, avg_sub.c.review_count)
        .outerjoin(avg_sub, Course.id == avg_sub.c.course_id)
        .where(Course.status == 'approved')
    )

    # 搜索
    if search:
        # 联合搜索课程名和教师名
        teacher_subq = select(Teacher.id).where(Teacher.name.contains(search)).subquery()
        query = query.where(
            or_(
                Course.name.contains(search),
                Course.teacher_id.in_(select(teacher_subq))
            )
        )

    if category_id:
        query = query.where(Course.category_id == category_id)
    if teacher_id:
        query = query.where(Course.teacher_id == teacher_id)
    if semester:
        query = query.where(Course.semester == semester)

    # 排序
    if sort == 'newest':
        query = query.order_by(Course.created_at.desc())
    else:
        query = query.order_by(func.coalesce(avg_sub.c.avg_rating, 0).desc())

    # 总数
    count_q = query.with_only_columns(func.count()).order_by(None)
    total = session.execute(count_q).scalar()

    # 分页
    rows = session.execute(query.offset((page - 1) * per_page).limit(per_page)).all()

    items = []
    for course, avg_r, r_count in rows:
        teacher = session.get(Teacher, course.teacher_id)
        category = session.get(Category, course.category_id)
        items.append({
            'id': course.id,
            'name': course.name,
            'teacher': {'id': teacher.id, 'name': teacher.name, 'department': teacher.department} if teacher else None,
            'category': {'id': category.id, 'name': category.name} if category else None,
            'semester': course.semester,
            'description': course.description,
            'avg_rating': round(float(avg_r), 1) if avg_r else 0,
            'review_count': r_count or 0,
            'created_at': course.created_at.isoformat() if course.created_at else None
        })

    return success(paginated(items, total, page, per_page))


@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course or course.status not in ('approved', 'inactive'):
        return error('课程不存在', 404)

    teacher = session.get(Teacher, course.teacher_id)
    category = session.get(Category, course.category_id)

    # 统计各维度平均分
    stats = session.execute(
        select(
            func.avg(Review.rating_teaching).label('avg_teaching'),
            func.avg(Review.rating_content).label('avg_content'),
            func.avg(Review.rating_exam).label('avg_exam'),
            func.avg(Review.rating_fairness).label('avg_fairness'),
            func.count(Review.id).label('review_count')
        )
        .where(Review.course_id == course_id, Review.is_hidden == 0)
    ).one()

    avg_teaching = round(float(stats.avg_teaching or 0), 1)
    avg_content = round(float(stats.avg_content or 0), 1)
    avg_exam = round(float(stats.avg_exam or 0), 1)
    avg_fairness = round(float(stats.avg_fairness or 0), 1)
    overall = round((avg_teaching + avg_content + avg_exam + avg_fairness) / 4, 1) if stats.review_count else 0

    return success({
        'id': course.id,
        'name': course.name,
        'teacher': {'id': teacher.id, 'name': teacher.name, 'department': teacher.department} if teacher else None,
        'category': {'id': category.id, 'name': category.name} if category else None,
        'semester': course.semester,
        'description': course.description,
        'status': course.status,
        'ratings': {
            'teaching': avg_teaching,
            'content': avg_content,
            'exam': avg_exam,
            'fairness': avg_fairness,
            'overall': overall
        },
        'review_count': stats.review_count
    })


@courses_bp.route('', methods=['POST'])
@login_required
def create_course():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    teacher_id = data.get('teacher_id')
    category_id = data.get('category_id')
    semester = (data.get('semester') or '').strip()
    description = (data.get('description') or '').strip()

    ok, msg = validate_required(name, '课程名称', 200)
    if not ok:
        return error(msg, 400)
    if not teacher_id:
        return error('请选择教师', 400)
    if not category_id:
        return error('请选择分类', 400)
    ok, msg = validate_required(semester, '学期', 20)
    if not ok:
        return error(msg, 400)
    if description and len(description) > 2000:
        return error('课程简介不能超过2000字', 400)

    session: Session = g.db_session

    # 查重
    dup = session.execute(
        select(Course).where(
            Course.name == name,
            Course.teacher_id == teacher_id,
            Course.semester == semester
        )
    ).scalar_one_or_none()
    if dup:
        return error('该课程在相同学期已存在', 409)

    # 验证教师和分类存在
    if not session.get(Teacher, teacher_id):
        return error('教师不存在', 400)
    if not session.get(Category, category_id):
        return error('分类不存在', 400)

    course = Course(
        name=name, teacher_id=teacher_id, category_id=category_id,
        semester=semester, description=description, created_by=g.user_id
    )
    session.add(course)
    session.commit()
    return success({'id': course.id}, '提交成功，等待审核', 201)


@courses_bp.route('/<int:course_id>', methods=['PUT'])
@admin_required
def update_course(course_id):
    data = request.get_json(silent=True) or {}
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course:
        return error('课程不存在', 404)

    if 'name' in data:
        course.name = (data['name'] or '').strip()
    if 'teacher_id' in data:
        course.teacher_id = data['teacher_id']
    if 'category_id' in data:
        course.category_id = data['category_id']
    if 'semester' in data:
        course.semester = (data['semester'] or '').strip()
    if 'description' in data:
        course.description = (data['description'] or '').strip()

    session.commit()
    return success(message='课程信息已更新')


@courses_bp.route('/<int:course_id>/approve', methods=['PUT'])
@admin_required
def approve_course(course_id):
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course:
        return error('课程不存在', 404)
    course.status = 'approved'
    course.reject_reason = None
    session.commit()
    return success(message='课程已通过审核')


@courses_bp.route('/<int:course_id>/reject', methods=['PUT'])
@admin_required
def reject_course(course_id):
    data = request.get_json(silent=True) or {}
    reason = (data.get('reason') or '').strip()
    if not reason:
        return error('请填写驳回理由', 400)

    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course:
        return error('课程不存在', 404)
    course.status = 'rejected'
    course.reject_reason = reason
    session.commit()
    return success(message='已驳回')


@courses_bp.route('/<int:course_id>/inactive', methods=['PUT'])
@admin_required
def inactive_course(course_id):
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course:
        return error('课程不存在', 404)
    course.status = 'inactive'
    session.commit()
    return success(message='课程已下架')


@courses_bp.route('/pending', methods=['GET'])
@admin_required
def pending_courses():
    session: Session = g.db_session
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = select(Course).where(Course.status == 'pending')
    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    courses = session.execute(query.order_by(Course.created_at.asc()).offset((page - 1) * per_page).limit(per_page)).scalars().all()

    items = []
    for c in courses:
        teacher = session.get(Teacher, c.teacher_id)
        category = session.get(Category, c.category_id)
        creator = session.get(User, c.created_by)
        items.append({
            'id': c.id,
            'name': c.name,
            'teacher': {'id': teacher.id, 'name': teacher.name} if teacher else None,
            'category': {'id': category.id, 'name': category.name} if category else None,
            'semester': c.semester,
            'description': c.description,
            'created_by': creator.nickname if creator else '',
            'created_at': c.created_at.isoformat() if c.created_at else None
        })

    return success(paginated(items, total, page, per_page))
