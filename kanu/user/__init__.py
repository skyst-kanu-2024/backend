import kanu
import kanu.database

import hashlib
import time
import json

class User:
    id: str
    name: str
    email: str
    gender: kanu.gender
    age: int
    nickname: str
    loc_agree: bool
    picture: str
    
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        gender: kanu.gender,
        age: int,
        picture: str = None,
        nickname: str = None,
        loc_agree: bool = False,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.gender = gender,
        self.age = age
        self.nickname = nickname
        self.loc_agree = loc_agree
        self.picture = picture

    def check_difference(self, user: "User") -> bool:
        return (
            self.gender != user.gender or
            self.age != user.age or
            self.nickname != user.nickname
        )
    
    def change(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid key: {key}")
            

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "gender": "M" if self.gender == kanu.gender.M else "F",
            "age": self.age,
            "nickname": self.nickname,
            "loc_agree": self.loc_agree,
            "picture_url": self.picture,
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    def with_profile(self) -> str:
        import kanu.profile
        this = self.to_dict()
        try:
            profile = kanu.profile.get_profile(self)
        except:
            return json.dumps(this, ensure_ascii=False)
        this.update({
            "mbti": profile.mbti,
            "introduce": profile.introduce,
        })

        return json.dumps(this, ensure_ascii=False)
        


def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id CHAR(32) NOT NULL,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL,
    gender INTEGER,
    age INTEGER,
    nickname VARCHAR(20),
    loc_agree BOOLEAN DEFAULT FALSE,
    picture VARCHAR(1000),
    PRIMARY KEY(id),
    UNIQUE(id, email)
);
    """)
    #cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_email ON user(email)")
    conn.commit()
    conn.close()
    

'''def create_user(
    name: str,
    email: str,
    gender: kanu.gender,
    age: int,
    password: str,
    nickname: str = None,
    loc_agree: bool = False,
) -> User:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    
    # Check that the email is not already in use
    cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
    if cursor.fetchone() is not None:
        raise ValueError("Email already in use")

    userid = hashlib.md5(f"{name}{email}{time.time()}".encode()).hexdigest()
    query = "INSERT INTO user (id, name, email, gender, age, nickname, loc_agree) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (userid, name, email, gender, age, nickname, loc_agree))
    kanu.auth.create_user(userid, password)
    conn.commit()
    conn.close()
    return User(userid, name, email, gender, age, nickname)'''

def get_as_session(session: str) -> User:
    import kanu.auth
    return kanu.auth.get_user_by_session(session)


def get_user(
    userid: str = None,
    email: str = None,
    session: str = None,
) -> User:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    query = "SELECT id, name, email, gender, age, nickname, loc_agree, picture FROM user"
    if session:
        user = get_as_session(session)
        conn.close()
        return user
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
    return User(**user)

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
    if user.check_difference(dbuser):
        query = "UPDATE user SET gender = %s, age = %s, nickname = %s, loc_agree = %s WHERE id = %s"
        cursor.execute(query, (user.gender, user.age, user.nickname, user.loc_agree, user.id))
        conn.commit()
    conn.close()

    return True

def get_all_user():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, gender, age, nickname, loc_agree, picture FROM user")
    users = cursor.fetchall()
    conn.close()
    return [User(**user) for user in users]

