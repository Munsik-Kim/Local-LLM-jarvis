# db_handler.py - 자비스의 기억 저장소 (SQLite)
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), "chat_history.db")

def init_db():
    """
    데이터베이스와 테이블을 초기화하는 함수
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # history 테이블 생성: id, role(누가), content(내용), timestamp(시간)
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(role, content):
    """
    메시지 하나를 DB에 저장
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO history (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def load_messages():
    """
    DB에 저장된 모든 대화 내용을 리스트로 가져옴
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT role, content FROM history ORDER BY id ASC')
    rows = c.fetchall()
    conn.close()
    
    # Streamlit에서 쓰는 형식([{'role':..., 'content':...}])으로 변환
    messages = []
    for row in rows:
        messages.append({"role": row[0], "content": row[1]})
        
    return messages

def clear_db():
    """
    기억 삭제 (포맷)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM history')
    conn.commit()
    conn.close()