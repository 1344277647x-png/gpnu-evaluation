"""评价蓝图"""
from flask import Blueprint, request, g
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from models import Review, Course
from utils import success, error, paginated, login_required, admin_required, validate_rating, validate_comment

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/courses/<int:course_id>/reviews', methods=['GET'])
def list_reviews(course_id):
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course or course.status not in ('approved', 'inactive'):
        return error('课程不存在', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = select(Review).where(
        Review.course_id == course_id,
        Review.is_hidden == 0
    )
    total = session.execute(select(func.count()).select_from(query.subquery())).scalar()
    reviews = session.execute(
        query.order_by(Review.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
    ).scalars().all()

    items = []
    for r in reviews:
        items.append({
            'id': r.id,
            'user': {
                'id': r.user.id,
                'nickname': r.user.nickname,
            },
            'rating_teaching': r.rating_teaching,
            'rating_content': r.rating_content,
            'rating_exam': r.rating_exam,
            'rating_fairness': r.rating_fairness,
            'comment': r.comment,
            'created_at': r.created_at.isoformat() if r.created_at else None
        })

    return success(paginated(items, total, page, per_page))


@reviews_bp.route('/courses/<int:course_id>/reviews', methods=['POST'])
@login_required
def create_review(course_id):
    session: Session = g.db_session
    course = session.get(Course, course_id)
    if not course or course.status not in ('approved', 'inactive'):
        return error('课程不存在', 404)

    # 检查是否已评价
    existing = session.execute(
        select(Review).where(Review.course_id == course_id, Review.user_id == g.user_id)
    ).scalar_one_or_none()
    if existing:
        return error('您已评价过该课程，不可重复评价', 409)

    data = request.get_json(silent=True) or {}

    # 校验评分
    for field in ['rating_teaching', 'rating_content', 'rating_exam', 'rating_fairness']:
        ok, msg = validate_rating(data.get(field))
        if not ok:
            return error(msg, 400)

    comment = (data.get('comment') or '').strip()
    ok, msg = validate_comment(comment)
    if not ok:
        return error(msg, 400)

    review = Review(
        course_id=course_id,
        user_id=g.user_id,
        rating_teaching=int(data['rating_teaching']),
        rating_content=int(data['rating_content']),
        rating_exam=int(data['rating_exam']),
        rating_fairness=int(data['rating_fairness']),
        comment=comment or ''
    )
    session.add(review)
    session.commit()
    return success({'id': review.id}, '评价提交成功', 201)


@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    session: Session = g.db_session
    review = session.get(Review, review_id)
    if not review:
        return error('评价不存在', 404)
    if review.user_id != g.user_id and g.user_role != 'admin':
        return error('无权删除', 403)
    session.delete(review)
    session.commit()
    return success(message='评价已删除')


@reviews_bp.route('/reviews/<int:review_id>/hide', methods=['PUT'])
@admin_required
def hide_review(review_id):
    session: Session = g.db_session
    review = session.get(Review, review_id)
    if not review:
        return error('评价不存在', 404)
    review.is_hidden = 1 - review.is_hidden
    session.commit()
    return success(message='已隐藏' if review.is_hidden else '已取消隐藏')
