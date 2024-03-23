import kanu
import kanu.database
from kanu import user
from uuid import uuid4
import time


class Room:
    id: str
    userM : str
    userF : str
    created_at : int
    detail_loc_agree_M : bool
    detail_loc_agree_F: bool
def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room(
    id char(32) NOT NULL,
    userM char(32) NOT NULL,
    userF char(32) NOT NULL,
    created_at int NOT NULL,
    detail_loc_agree_M boolean DEFAULT FALSE,
    detail_loc_agree_F boolean DEFAULT FALSE,
    PRIMARY KEY (id),
    unique (id,userM,userF)
    )
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_room_people ON room(userM,userF)
    """)
    
def create_room(
    userM:str,
    userF:str
)-> Room:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id, userM,userF, created_at,detail_loc_agree_M,detail_loc_agree_F) from room WHERE userM = %s and userF = %s
    """,(userM,userF))
    exist = cursor.fetchone()
    if exist:
        room = Room()
        room.id = exist[0]
        room.userM = exist[1]
        room.userF = exist[2]
        room.created_at = exist[3]
        room.detail_loc_agree_M = exist[4]
        room.detail_loc_agree_M = exist[5]
        return room
    id = uuid4().hex
    created_at = int(time.time())
    cursor.execute("""
    INSERT INTO room(id,userM,userF,created_at) VALUES (%s,%s,%s,%s)
    """,(id,userM,userF,created_at)
    )
    room = Room()
    room.id = id
    room.userM = userM
    room.userF = userF
    room.created_at = created_at
    room.detail_loc_agree_M = False
    room.detail_loc_agree_F = False
    return room
    
def get_room_by_user(
    user: kanu.user.User
) -> list[Room]:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    if user.gender == kanu.gender.M:
        cursor.execute("""
        SELECT (id,userM,userF,created_at) FROM room WHERE userM = %s
        """,user.id)
        roomlist = cursor.fetchall()

    elif user.gender == kanu.gender.F:
        cursor.execute("""
        SELECT (id,userM,userF,created_at,detail_loc_agree_M,detail_loc_agree_F) FROM room WHERE userF = %s
        """,user.id)
        roomlist = cursor.fetchall()
    else:
        raise ValueError("User is not Male/Female")
    data = []
    for oneroom in roomlist:
        room = Room()
        room.id = oneroom[0]
        room.userM = oneroom[1]
        room.userF = oneroom[2]
        room.created_at = oneroom[3]
        room.detail_loc_agree_M = oneroom[4]
        room.detail_loc_agree_F = oneroom[5]
        data.append(room)
    return data

def get_room_by_id(
    id : str
):
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,userM,userF,created_at,detail_loc_agree_M,detail_loc_agree_F) FROM room WHERE id = %s
    """,(id))
    oneroom = cursor.fetchone()
    room = Room()
    room.id = oneroom[0]
    room.userM = oneroom[1]
    room.userF = oneroom[2]
    room.created_at = oneroom[3]
    room.detail_loc_agree_M = oneroom[4]
    room.detail_loc_agree_F = oneroom[5]
    return room

def update_allow_user_loc(
    user:kanu.user.User,
    id:str,
    agree:bool
):
    conn = kanu.database.Database()
    cursor = conn.cursor()
    if user.gender == kanu.gender.M:
        cursor.execute("""
        UPDATE room SET detail_loc_agree_M = %s WHERE id = %s and userM = %s
        """,(agree,id,user.id))
    elif user.gender == kanu.gender.F:
        cursor.execute("""
        UPDATE room SET detail_loc_agree_F = %s WHERE id = %s and userF = %s
        """, (agree, id, user.id))
    else:
        raise ValueError("User is not Male/Female")

def is_user_in_room(
    user : kanu.user.User,
    id : str
):
    room = get_room_by_id(id)
    if user.gender == kanu.gender.M and room.userM == user.id:
        return True
    elif user.gender == kanu.gender.F and room.userF == user.id:
        return True
    else:
        return False