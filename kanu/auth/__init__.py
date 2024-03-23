import kanu
import kanu.database
import kanu.user

import hashlib
import time


def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user_pass (
    id CHAR(32) NOT NULL,
    password VARCHAR(64) NOT NULL,
    PRIMARY KEY(id)
);
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user_session (
    id CHAR(32) NOT NULL,
    session CHAR(32) NOT NULL,
    PRIMARY KEY(session),
    UNIQUE(session),
);
    """)
    conn.commit()
    conn.close()


def create_user(
    id: int,
    password: str
) -> None:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    query = "INSERT INTO user_pass(id, password) VALUES (%s, %s)"
    password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(query, (id, password))
    conn.commit()
    conn.close()

def is_session_valid(session: str) -> bool:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_session WHERE session = %s", (session,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def login(email: str, password: str) -> str | None:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT user.id FROM user JOIN user_pass ON user.id = user_pass.id WHERE user.email = %s AND user_pass.password = %s", (email, hashlib.sha256(password.encode()).hexdigest()))
    result = cursor.fetchone()
    if result is None:
        return None
    session = hashlib.md5(f"{result['id']}{time.time()}".encode()).hexdigest()
    cursor.execute("INSERT INTO user_session (id, session) VALUES (%s, %s)", (result['id'], session))
    conn.commit()
    conn.close()
    return session

def get_userid_by_session(session: str) -> str:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_session WHERE session = %s", (session,))
    result = cursor.fetchone()
    if result is None:
        return None
    return result[0]