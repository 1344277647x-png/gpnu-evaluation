"""初始化数据库 — 用 Python 执行 SQL"""
import re
import pymysql

DB_CONFIG = {
    'host': 'localhost', 'user': 'root', 'password': '626957',
    'charset': 'utf8mb4'
}

SQL_FILE = r'D:\gpnu教师评价web\backend\init_db.sql'

with open(SQL_FILE, 'r', encoding='utf-8') as f:
    raw = f.read()

# Remove comments, split by semicolons
cleaned = re.sub(r'--.*$', '', raw, flags=re.MULTILINE)
statements = [s.strip() for s in cleaned.split(';') if s.strip()]

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

for stmt in statements:
    try:
        cursor.execute(stmt)
        print(f'  OK')
    except Exception as e:
        err = str(e)
        if 'Duplicate' in err or 'already exists' in err:
            print(f'  SKIP (exists)')
        elif 'Unknown database' in err:
            print(f'  SKIP (will create DB)')
        else:
            print(f'  ERR: {e}')

conn.commit()
conn.close()

# Verify
conn = pymysql.connect(**DB_CONFIG, database='gpnu_evaluation')
cursor = conn.cursor()
for t in ['users', 'categories', 'teachers', 'courses', 'reviews']:
    cursor.execute(f"SELECT COUNT(*) FROM {t}")
    print(f'{t}: {cursor.fetchone()[0]} rows')
conn.close()
print('\nDatabase initialized successfully!')
