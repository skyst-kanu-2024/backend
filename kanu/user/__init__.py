import kanu
import kanu.database

import hashlib
import time

class User:
    id: str
    name: str
    email: str
    gender: kanu.gender
    age: int
    nickname: str
    
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        gender: kanu.gender,
        age: int,
        nickname: str = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.gender = gender,
        self.age = age
        self.nickname = nickname

    def check_differenct(self, user: "User") -> bool:
        return (
            self.gender != user.gender or
            self.age != user.age or
            self.nickname != user.nickname
        )


def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id CHAR(32) NOT NULL,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL,
    gender INTEGER NOT NULL,
    age INTEGER NOT NULL,
    nickname VARCHAR(20),
    PRIMARY KEY(id),
    UNIQUE(id, email)
);
    """)
    conn.commit()
    conn.close()
    

def create_user(
    name: str,
    email: str,
    gender: kanu.gender,
    age: int,
    nickname: str = None,
) -> User:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    # {name}{email}{time.time()}
    userid = hashlib.md5(f"{name}{email}{time.time()}".encode()).hexdigest()
    query = "INSERT INTO user (id, name, email, gender, age, nickname) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (userid, name, email, gender, age, nickname))
    conn.commit()
    conn.close()
    return User(userid, name, email, gender, age, nickname)


def get_user(
    userid: str = None,
    email: str = None,
) -> User:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    basequery = "SELECT id, name, email, gender, age, nickname FROM user"
    if userid:
        query += " WHERE id = %s"
        cursor.execute(query, (userid,))
    elif email:
        query += " WHERE email = %s"
        cursor.execute(query, (email,))
    else:
        raise ValueError("Either userid or email must be provided")
    user = cursor.fetchone()
    conn.close()
    return User(*user)

def update_user(
    user: User,
) -> bool:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    dbuser = get_user(userid=user.id)
    if dbuser.email != user.email:
        raise ValueError("Email cannot be changed")
    if dbuser.name != user.name:
        raise ValueError("Name cannot be changed")
    if user.check_differenct(dbuser):
        query = "UPDATE user SET gender = %s, age = %s, nickname = %s WHERE id = %s"
        cursor.execute(query, (user.gender, user.age, user.nickname, user.id))
        conn.commit()
    conn.close()

    return True
