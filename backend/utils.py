"""工具函数：统一响应、JWT、校验器"""
import re
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g

from config import Config

conf = Config()


# ── 统一响应 ──────────────────────────────────

def success(data=None, message='ok', code=200):
    return jsonify({'code': code, 'data': data, 'message': message}), code


def error(message='error', code=400, data=None):
    return jsonify({'code': code, 'data': data, 'message': message}), code


def paginated(items, total, page, per_page):
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': max(1, (total + per_page - 1) // per_page)
    }


# ── JWT ───────────────────────────────────────

def create_access_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(seconds=conf.JWT_ACCESS_EXPIRES)
    }
    return jwt.encode(payload, conf.SECRET_KEY, algorithm='HS256')


def create_refresh_token(user):
    payload = {
        'user_id': user.id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(seconds=conf.JWT_REFRESH_EXPIRES)
    }
    return jwt.encode(payload, conf.SECRET_KEY, algorithm='HS256')


def decode_token(token):
    return jwt.decode(token, conf.SECRET_KEY, algorithms=['HS256'])


# ── 装饰器 ────────────────────────────────────

def login_required(f):
    """需要登录"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return error('请先登录', 401)
        token = auth_header[7:]
        try:
            payload = decode_token(token)
            if payload.get('type') != 'access':
                return error('无效的令牌', 401)
            g.user_id = payload['user_id']
            g.user_role = payload['role']
        except jwt.ExpiredSignatureError:
            return error('令牌已过期，请刷新', 401)
        except jwt.InvalidTokenError:
            return error('无效的令牌', 401)
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """需要管理员"""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if g.user_role != 'admin':
            return error('权限不足', 403)
        return f(*args, **kwargs)
    return decorated


# ── 校验器 ────────────────────────────────────

USERNAME_RE = re.compile(r'^[a-zA-Z0-9_]{3,20}$')
PASSWORD_RE = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')


def validate_username(username):
    if not username or not USERNAME_RE.match(username):
        return False, '用户名须为3-20位字母、数字或下划线'
    return True, None


def validate_password(password):
    if not password or not PASSWORD_RE.match(password):
        return False, '密码须至少8位，包含大小写字母和数字'
    return True, None


def validate_rating(rating):
    try:
        r = int(rating)
        if 1 <= r <= 5:
            return True, None
    except (ValueError, TypeError):
        pass
    return False, '评分须为1-5的整数'


def validate_required(value, name, max_len=200):
    if not value or not str(value).strip():
        return False, f'{name}不能为空'
    if len(str(value).strip()) > max_len:
        return False, f'{name}不能超过{max_len}个字符'
    return True, None


def validate_comment(comment):
    if comment and len(comment) > 2000:
        return False, '评语不能超过2000字'
    return True, None
