import uuid

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
def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room(
    id char(32) NOT NULL,
    userM char(32) NOT NULL,
    userF char(32) NOT NULL,
    created_at number NOT NULL,
    loc_agree_both boolean DEFAULT FALSE,
    PRIMARY KEY (id),
    unique (id,userM,userF)
    )
    """)
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_room_people ON room(userM,userF)
    """)
    
def create_room(
    userM:str,
    userF:str,
)-> Room:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, userM,userF, created_at from room WHERE userM = %s and userF = %s
    """,(userM,userF))
    exist = cursor.fetchone()
    if exist:
        room = Room()
        room.id = exist[0]
        room.userM = exist[1]
        room.userF = exist[2]
        room.created_at = exist[3]
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
    return room
    
def get_room(
    user: kanu.user.User
) -> list[Room]:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    if user.gender == kanu.gender.M:
        cursor.execute("""
        SELECT (id,userM,userF,created_at) FROM room WHERE userM = %s
        """,(user.id))
        roomlist = cursor.fetchall()

    elif user.gender == kanu.gender.F:
        cursor.execute("""
        SELECT * FROM room WHERE userF = %s
        """,(user.id))
        roomlist = cursor.fetchall()
    else:
        raise ValueError("User is not Male/Female")
    data = []
    for oneroom in roomlist:
        room = Room()
        room.id = oneroom[0]
        room.userM = oneroom[1]
        room.userF = oneroom[2]
        room.create_at = oneroom[3]
        data.append(room)
    return data


    