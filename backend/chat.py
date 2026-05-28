"""AI Chat blueprint - Ollama proxy with knowledge base RAG"""
import re
import json
import urllib.request
from flask import Blueprint, request, g
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from models import Course, Teacher, Category, Review, User, ChatMessage
from utils import success, error, admin_required

chat_bp = Blueprint('chat', __name__)

OLLAMA_URL = 'http://localhost:11434/api/chat'
MODEL = 'qwen2:latest'


def query_ollama(messages):
    body = json.dumps({'model': MODEL, 'messages': messages, 'stream': False}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=body,
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
    return data.get('message', {}).get('content', '')


def get_course_summary(session):
    courses = session.execute(
        select(Course).where(Course.status == 'approved')
    ).scalars().all()

    lines = []
    for c in courses:
        teacher = session.get(Teacher, c.teacher_id)
        category = session.get(Category, c.category_id)
        stats = session.execute(
            select(
                func.avg(Review.rating_teaching),
                func.avg(Review.rating_content),
                func.avg(Review.rating_exam),
                func.avg(Review.rating_fairness),
                func.count(Review.id)
            ).where(Review.course_id == c.id, Review.is_hidden == 0)
        ).one()

        t = float(stats[0] or 0)
        ct = float(stats[1] or 0)
        e = float(stats[2] or 0)
        f = float(stats[3] or 0)
        overall = round((t + ct + e + f) / 4, 1) if stats[4] else 0

        lines.append(
            f"- {c.name} | {teacher.name if teacher else '?'} | "
            f"{category.name if category else '?'} | "
            f"Score {overall} | {stats[4]} reviews | {c.semester}"
        )
    return '\n'.join(lines)


def search_knowledge(session, question):
    words = extract_keywords_simple(question)
    if not words:
        return []

    conditions = []
    params = {}
    for w in words[:3]:
        conditions.append(f"keywords LIKE :kw_{id(w)}")
        conditions.append(f"question LIKE :q_{id(w)}")
        params[f'kw_{id(w)}'] = f'%{w}%'
        params[f'q_{id(w)}'] = f'%{w}%'

    sql = f"""
        SELECT id, question, answer FROM chat_knowledge
        WHERE {' OR '.join(conditions)}
        ORDER BY usage_count DESC
        LIMIT 5
    """
    rows = session.execute(text(sql), params).fetchall()
    return [{'id': r[0], 'question': r[1], 'answer': r[2]} for r in rows]


def extract_keywords_simple(text):
    tokens = re.split(r'[^a-zA-Z0-9\u4e00-\u9fff]+', text)
    stop_words = {'de', 'le', 'shi', 'zai', 'wo', 'you', 'he', 'jiu', 'bu', 'ren', 'dou', 'yi', 'yige',
                  'shang', 'ye', 'hen', 'dao', 'shuo', 'yao', 'qu', 'ni', 'hui', 'zhe', 'meiyou', 'kan', 'hao',
                  'ziji', 'zhe', 'ta', 'na', 'ba', 'ma', 'ne', 'a', 'o', 'en'}
    keywords = []
    for t in tokens:
        t = t.strip()
        if len(t) >= 2 and t.lower() not in stop_words:
            keywords.append(t)
    return keywords[:8]


def extract_keywords_via_ai(question, answer):
    prompt = f"Extract 3-5 keywords from this Q\u0026A, comma separated, keywords only:\nQ: {question[:200]}\nA: {answer[:300]}\nKeywords:"
    try:
        result = query_ollama([{'role': 'user', 'content': prompt}])
        result = result.strip().replace('Keywords:', '').replace('keywords:', '')
        kws = [k.strip() for k in re.split(r'[,;]+', result) if k.strip()]
        return ','.join(kws[:5])
    except Exception:
        ks = extract_keywords_simple(question + ' ' + answer[:100])
        return ','.join(ks[:3])


def save_to_knowledge(session, question, answer):
    keywords = extract_keywords_via_ai(question, answer)
    session.execute(
        text("INSERT INTO chat_knowledge (question, answer, keywords, usage_count) VALUES (:q, :a, :kw, 0)"),
        {'q': question, 'a': answer, 'kw': keywords[:500]}
    )
    session.commit()


def bump_usage(session, kb_hits):
    if not kb_hits:
        return
    ids = tuple(h['id'] for h in kb_hits)
    session.execute(
        text("UPDATE chat_knowledge SET usage_count = usage_count + 1 WHERE id IN :ids"),
        {'ids': ids}
    )
    session.commit()


@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get('messages', [])
    if not messages:
        return error('No messages', 400)

    user_msg = messages[-1].get('content', '') if messages else ''
    if not user_msg.strip():
        return error('Empty message', 400)

    session_id = data.get('session_id', '')
    user_id = getattr(g, 'user_id', None)

    db_session: Session = g.db_session

    # Save user message
    if session_id and user_msg.strip():
        try:
            db_session.execute(text(
                "INSERT INTO chat_messages (session_id, user_id, role, content) VALUES (:sid, :uid, 'user', :ct)"
            ), {'sid': session_id, 'uid': user_id, 'ct': user_msg[:5000]})
            db_session.commit()
        except Exception:
            pass

    # Step 1: Search knowledge base
    kb_hits = search_knowledge(db_session, user_msg)
    if kb_hits:
        bump_usage(db_session, kb_hits)

    # Step 2: Build course summary
    course_summary = get_course_summary(db_session)

    kb_context = ''
    if kb_hits:
        kb_lines = [f"- Q: {h['question'][:200]}\n  A: {h['answer'][:300]}" for h in kb_hits]
        kb_context = '\n'.join(kb_lines)

    system_prompt = f"""You are an AI admin assistant for the GPnu elective course evaluation system. Answer questions about courses, ratings, and system usage. Be friendly and helpful, like a senior student.

Current course data:
{course_summary if course_summary else 'No courses yet'}

Knowledge base:
{kb_context if kb_context else 'No knowledge base entries yet'}

If your answer contains useful information about courses, ratings, or system features, end with <!--SAVE--> to save it to the knowledge base. Do NOT add <!--SAVE--> for greetings or casual chat."""

    ollama_messages = [
        {'role': 'system', 'content': system_prompt},
        *[{'role': m.get('role', 'user'), 'content': m.get('content', '')} for m in messages]
    ]

    try:
        full_reply = query_ollama(ollama_messages)
    except Exception as e:
        return error(f'AI service unavailable: {str(e)}', 500)

    saved = False
    clean_reply = full_reply
    if '<!--SAVE-->' in full_reply:
        saved = True
        clean_reply = full_reply.replace('<!--SAVE-->', '').strip()
        try:
            save_to_knowledge(db_session, user_msg, clean_reply)
        except Exception:
            pass

    # Save AI reply
    if session_id and clean_reply.strip():
        try:
            db_session.execute(text(
                "INSERT INTO chat_messages (session_id, user_id, role, content) VALUES (:sid, :uid, 'assistant', :ct)"
            ), {'sid': session_id, 'uid': user_id, 'ct': clean_reply[:5000]})
            db_session.commit()
        except Exception:
            pass

    return success({'reply': clean_reply, 'saved': saved})


# ===== Admin: chat history =====

@chat_bp.route('/admin/chat/sessions', methods=['GET'])
@admin_required
def admin_chat_sessions():
    """List all unique chat sessions"""
    db_session: Session = g.db_session

    sql = """
        SELECT cm.session_id, cm.user_id, u.nickname, u.username,
               MIN(cm.created_at) as first_msg, MAX(cm.created_at) as last_msg,
               COUNT(*) as msg_count
        FROM chat_messages cm
        LEFT JOIN users u ON cm.user_id = u.id
        GROUP BY cm.session_id, cm.user_id, u.nickname, u.username
        ORDER BY last_msg DESC
        LIMIT 100
    """
    rows = db_session.execute(text(sql)).fetchall()
    items = [{
        'session_id': r[0],
        'user_id': r[1],
        'nickname': r[2] or 'Anonymous',
        'username': r[3] or '',
        'first_msg': r[4].isoformat() if r[4] else None,
        'last_msg': r[5].isoformat() if r[5] else None,
        'msg_count': r[6]
    } for r in rows]
    return success({'items': items, 'total': len(items)})


@chat_bp.route('/admin/chat/sessions/<session_id>', methods=['GET'])
@admin_required
def admin_chat_session_detail(session_id):
    """Get all messages for a session"""
    db_session: Session = g.db_session

    rows = db_session.execute(text(
        "SELECT id, role, content, user_id, created_at FROM chat_messages "
        "WHERE session_id = :sid ORDER BY created_at ASC"
    ), {'sid': session_id}).fetchall()

    items = [{
        'id': r[0],
        'role': r[1],
        'content': r[2],
        'user_id': r[3],
        'created_at': r[4].isoformat() if r[4] else None
    } for r in rows]
    return success({'items': items})
