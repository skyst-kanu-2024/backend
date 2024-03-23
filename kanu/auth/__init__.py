import kanu
import kanu.database
import kanu.user

import hashlib
import time
from google.oauth2 import id_token
from google.auth.transport import requests


def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    '''cursor.execute("""
CREATE TABLE IF NOT EXISTS user_pass (
    id CHAR(32) NOT NULL,
    password VARCHAR(64) NOT NULL,
    FOREIGN KEY(id) REFERENCES user(id) ON DELETE CASCADE,
    PRIMARY KEY(id)
    
);
    """)'''
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user_session (
    id CHAR(32) NOT NULL,
    session CHAR(32) NOT NULL,
    PRIMARY KEY(session),
    FOREIGN KEY(id) REFERENCES user(id) ON DELETE CASCADE,
    UNIQUE(session)
);
    """)
    conn.commit()
    conn.close()

'''
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
    conn.close()'''

def is_session_valid(session: str) -> bool:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_session WHERE session = %s", (session,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

'''
def login(email: str, password: str) -> str | None:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT user.id FROM user JOIN user_pass ON user.id = user_pass.id WHERE user.email = %s AND user_pass.password = %s", (email, hashlib.sha256(password.encode()).hexdigest()))
    result = cursor.fetchone()
    if result is None:
        conn.close()
        return None
    session = hashlib.md5(f"{result['id']}{time.time()}".encode()).hexdigest()
    cursor.execute("INSERT INTO user_session (id, session) VALUES (%s, %s)", (result['id'], session))
    conn.commit()
    conn.close()
    return session'''

def login(token: str) -> str | None:
    # google login with ios
    # server google client id -> kanu.config.google_client_id
    # server google client secret -> kanu.config.google_client_secret
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), kanu.config.google_client_id)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        print(idinfo)
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        conn = kanu.database.Database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO user (id, name, email) VALUES (%s, %s, %s)", (userid, name, email))
            conn.commit()
        session = hashlib.md5(f"{userid}{time.time()}".encode()).hexdigest()
        cursor.execute("INSERT INTO user_session (id, session) VALUES (%s, %s)", (userid, session))
        conn.commit()
        conn.close()
        return session
    except ValueError:
        return None

def get_user_by_session(session: str) -> kanu.user.User | None:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_session WHERE session = %s", (session,))
    result = cursor.fetchone()
    if result is None:
        conn.close()
        return None
    user = kanu.user.get_user(userid=result, cursor=cursor)
    conn.close()
    return user