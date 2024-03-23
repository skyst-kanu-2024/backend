import kanu
import kanu.user
import kanu.database


class Profile:
    id:str
    mbti:str
    introduce:str

def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
    id char(32) NOT NULL UNIQUE,
    mbti varchar(4) NOT NULL,
    introduce varchar(300) NOT NULL,
    PRIMARY KEY(id)
    )
    """)
    
def create_profile(
    user: kanu.user.User,
    mbti:str,
    introduce:str
) -> Profile:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,mbti,introduce) FROM profile WHERE id = %s
    """,(user.id))
    exist = cursor.fetchone()
    if exist:
        profile = Profile()
        profile.id = exist[0]
        profile.mbti = exist[1]
        profile.introduce = exist[2]
        return profile
    cursor.execute("""
    INSERT INTO profile(id,mbti,introduce) VALUES (%s,%s,%s)
    """,(user.id,mbti,introduce))
    profile = Profile()
    profile.id = user.id
    profile.mbti = mbti
    profile.introduce = introduce
    return profile
    
def get_profile(
    user: kanu.user.User
) -> Profile:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,mbti,introduction) FROM profile WHERE id = %s
    """,(user.id))
    oneprofile = cursor.fetchone()
    profile = Profile()
    profile.id = oneprofile[0]
    profile.mbti = oneprofile[1]
    profile.introduce = oneprofile[2]
    return profile
