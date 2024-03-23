import kanu
from kanu import user
import kanu.database
from kanu import room
from uuid import uuid4
import time

class Message:
    message:str
    created_at:str
    userid:str
    
def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS message(
    id char(32) NOT NULL
    message char(1000) NOT NULL,
    created_at number NOT NULL,
    userid str(32) NOT NULL
    )
    """)
    
def create_message(
    id:str,
    message:str,
    userid : str
)->Message:
    created_at = int(time.time())
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO message(id,message,created_at,userid) VALUES (%s,%s,%s)",(id,message,created_at,userid))
    msg = Message()
    msg.id = id
    msg.message = message
    msg.created_at = created_at
    msg.userid = userid
    return msg

def get_message(
    id:str,
    page:int
)->list[Message]:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT (id,message,created_at,userid) FROM message WHERE id = %s ORDER BY created_at DESC LIMIT 100 OFFSET %s
    """,(id,page))
    msglist = cursor.fetchall()
    data = []
    for onemsg in msglist:
        msg = Message()
        msg.message = onemsg[1]
        msg.created_at = onemsg[2]
        msg.userid = onemsg[3]
        data.append(msg)
    return data

    
'''def delete_message(
    id:str,
    created_at : int,
    userid:str
):
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM message WHERE id = %s and created_at = %s and userid = %s
    """,id,created_at,userid)'''