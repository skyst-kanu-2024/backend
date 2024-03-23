import kanu
import kanu.database
from kanu.user import User

class HobbyName:
    id: int
    name: str

class HobbyMatch:
    hobbyname: HobbyName.name
    userid: User.id

def setup(): # TABLE setup
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE 'hobby_name'(
            'id' INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            'name' VARCHAR(20) NOT NULL 
        )
        
        """
    )
    cursor.execute(
        """CREATE TABLE 'hobby_match'(
            'user_id' VARCHAR(32) NOT NULL,
            'hobby_name' VARCHAR(20)
        )
        """
    )

def create_hobby( #만약 hobby가 존재하지 않으면 추가
    name: str,
) -> HobbyName:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO hobby_name(name) VALUES (%s)", (name)
    )
    pass

def get_hobby( #hobby들이 뭐 있는지 불러옴.
    hobbyname: str = None,
) -> HobbyName:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM hobby_name"
    )
    data: list[tuple[int, str]] = cursor.fetchall()
    ndata: list[HobbyName] = [HobbyName(id=id, name=name) for id, name in data]
    return ndata
        
    

def update_hobby( #아마 쓰지는 않을 거 같은데... admin 계정이 할 수 있는 것일듯?
    id: id,
    hobbyname: HobbyName,
    )-> HobbyName:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE hobby_name
            SET name=%s
            WHERE id=%d
        """, (hobbyname), (id)
    )
    pass

def delete_hobby( #마찬가지 admin에서 hobby 종류 삭제할 때 
    hobbyname: str,
)-> HobbyName:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM hobby_name
            WHERE name=%s
        """, (hobbyname)
    )
    pass

def get_user_hobby( #userHobby 가져올 때
    userid: User.id,
) -> HobbyMatch:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM hobby_match
            WHERE user_id=%s
        """, (userid)
    )
    data: list[tuple[int, str]] = cursor.fetchall()
    ndata = [HobbyMatch(userid=user_id, hobbyname=hobby_name) for user_id, hobby_name in data]
    return ndata

def update_user_hobby( #user가 본인 hobby update 할 때, 근데 이건 사용하면 안 될 듯!!!!!!!
    userid: User.id,
    hobbyname: HobbyName.name,
) -> HobbyMatch:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE hobby_match
            SET hobbyname=%s
            WHERE id=%s
        """, (hobbyname), (userid)
    )
    pass

def delete_user_hobby( #user가 본인 hobby 삭제 할 때
    userid: User.id,
    hobbyname: HobbyName.name,
)-> HobbyMatch:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM hobby_match
            WHERE user_id=%s AND name=%s
        """, (userid),(hobbyname)
    )
    pass

