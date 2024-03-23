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
    mbti char(4) NOT NULL,
    introduce char(300) NOT NULL
    )
    """)
    
def create_profile(
    id:kanu.user.User.id,
    mbti:str,
    introduce:str
) ->Profile:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,mbti,introduce) FROM profile WHERE id = %s
    """,id)
    exist = cursor.fetchone()
    if exist:
        profile = Profile()
        profile.id = exist[0]
        profile.mbti = exist[1]
        profile.introduce = exist[2]
        return profile
    cursor.execute("""
    INSERT INTO profile(id,mbti,introduce) VALUES (%s,%s,%s)
    """,(id,mbti,introduce))
    profile = Profile()
    profile.id = id
    profile.mbti = mbti
    profile.introduce = introduce
    return profile
    
def get_profile(
    id:kanu.user.User.id,
) -> Profile:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,mbti,introduction) FROM profile WHERE id = %s
    """,id)
    oneprofile = cursor.fetchone()
    profile = Profile()
    profile.id = oneprofile[0]
    profile.mbti = oneprofile[1]
    profile.introduce = oneprofile[2]
    return profile