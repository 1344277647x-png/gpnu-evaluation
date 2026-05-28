"""分类蓝图"""
from flask import Blueprint, request, g
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Category
from utils import success, error, admin_required, validate_required

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('', methods=['GET'])
def list_categories():
    session: Session = g.db_session
    cats = session.execute(
        select(Category).where(Category.is_active == 1).order_by(Category.sort_order)
    ).scalars().all()
    items = [{'id': c.id, 'name': c.name, 'sort_order': c.sort_order} for c in cats]
    return success(items)


@categories_bp.route('', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    ok, msg = validate_required(name, '分类名称', 50)
    if not ok:
        return error(msg, 400)

    session: Session = g.db_session
    c = Category(name=name, sort_order=data.get('sort_order', 0))
    session.add(c)
    session.commit()
    return success({'id': c.id}, '添加成功', 201)


@categories_bp.route('/<int:cat_id>', methods=['PUT'])
@admin_required
def update_category(cat_id):
    data = request.get_json(silent=True) or {}
    session: Session = g.db_session
    c = session.get(Category, cat_id)
    if not c:
        return error('分类不存在', 404)

    if 'name' in data:
        c.name = (data['name'] or '').strip()
    if 'sort_order' in data:
        c.sort_order = data['sort_order']
    if 'is_active' in data:
        c.is_active = data['is_active']
    session.commit()
    return success(message='分类已更新')
