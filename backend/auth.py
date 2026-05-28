"""认证蓝图"""
import bcrypt
import jwt
from flask import Blueprint, request, g
from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User
from utils import (
    success, error, create_access_token, create_refresh_token,
    decode_token, login_required, validate_username, validate_password
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    nickname = (data.get('nickname') or '').strip()
    student_id = (data.get('student_id') or '').strip()

    ok, msg = validate_username(username)
    if not ok:
        return error(msg, 400)

    ok, msg = validate_password(password)
    if not ok:
        return error(msg, 400)

    if not nickname or not student_id:
        return error('昵称和学号不能为空', 400)

    if len(nickname) > 50 or len(student_id) > 20:
        return error('昵称或学号超出长度限制', 400)

    session: Session = g.db_session
    existing = session.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if existing:
        return error('用户名已被注册', 409)

    pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username=username, password_hash=pw_hash, nickname=nickname, student_id=student_id)
    session.add(user)
    session.commit()
    return success(message='注册成功', code=201)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if not username or not password:
        return error('用户名和密码不能为空', 400)

    session: Session = g.db_session
    user = session.execute(select(User).where(User.username == username)).scalar_one_or_none()

    if not user or not user.is_active:
        return error('用户名或密码错误', 401)

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return error('用户名或密码错误', 401)

    return success({
        'access_token': create_access_token(user),
        'refresh_token': create_refresh_token(user),
        'user': {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'student_id': user.student_id,
            'role': user.role
        }
    })


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json(silent=True) or {}
    refresh_token = data.get('refresh_token', '')
    if not refresh_token:
        return error('缺少 refresh_token', 400)
    try:
        payload = decode_token(refresh_token)
        if payload.get('type') != 'refresh':
            return error('无效的刷新令牌', 401)
    except jwt.ExpiredSignatureError:
        return error('刷新令牌已过期，请重新登录', 401)
    except jwt.InvalidTokenError:
        return error('无效的令牌', 401)

    session: Session = g.db_session
    user = session.get(User, payload['user_id'])
    if not user or not user.is_active:
        return error('用户不存在或已被禁用', 401)

    return success({
        'access_token': create_access_token(user),
        'refresh_token': create_refresh_token(user)
    })


@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    session: Session = g.db_session
    user = session.get(User, g.user_id)
    if not user:
        return error('用户不存在', 404)
    return success({
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'student_id': user.student_id,
        'role': user.role
    })


@auth_bp.route('/password', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json(silent=True) or {}
    old_pw = data.get('old_password', '')
    new_pw = data.get('new_password', '')

    session: Session = g.db_session
    user = session.get(User, g.user_id)

    if not bcrypt.checkpw(old_pw.encode('utf-8'), user.password_hash.encode('utf-8')):
        return error('原密码错误', 400)

    ok, msg = validate_password(new_pw)
    if not ok:
        return error(msg, 400)

    user.password_hash = bcrypt.hashpw(new_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    session.commit()
    return success(message='密码修改成功')


@auth_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json(silent=True) or {}
    nickname = (data.get('nickname') or '').strip()
    student_id = (data.get('student_id') or '').strip()

    if not nickname or not student_id:
        return error('昵称和学号不能为空', 400)
    if len(nickname) > 50 or len(student_id) > 20:
        return error('昵称或学号超出长度限制', 400)

    session: Session = g.db_session
    user = session.get(User, g.user_id)
    user.nickname = nickname
    user.student_id = student_id
    session.commit()
    return success(message='个人信息已更新')
