import kanu
import kanu.database
import time
import json

class Message:
    message: str
    created_at: int
    userid: str

    def __init__(
        self,
        message: str = None,
        created_at: int = None,
        userid: str = None
    ):
        self.message = message
        self.created_at = created_at
        self.userid = userid

    def to_dict(self) -> dict:
        return {
            "message": self.message,
            "created_at": self.created_at,
            "userid": self.userid
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())
    
def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS message (
    id CHAR(32) NOT NULL,
    userid CHAR(32) NOT NULL,
    message VARCHAR(1000) NOT NULL,
    created_at INT NOT NULL,
    FOREIGN KEY(userid) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY(id) REFERENCES room(id) ON DELETE CASCADE
)
    """)
    
def create_message(
    id:str,
    message:str,
    userid : str
) -> Message:
    created_at = int(time.time())
    conn = kanu.database.Database()
    cursor = conn.cursor()
    query = "INSERT INTO message(id,message,created_at,userid) VALUES (%s,%s,%s,%s)"
    cursor.execute(query,(id,message,created_at,userid))
    msg = Message()
    msg.id = id
    msg.message = message
    msg.created_at = created_at
    msg.userid = userid
    return msg

def get_message(
    id: str,
    page: int = 0
)->list[Message]:
    conn = kanu.database.Database()
    cursor = conn.cursor()
    query = "SELECT id, message, created_at, userid FROM message WHERE id = %s ORDER BY created_at DESC LIMIT 100 OFFSET %s"
    cursor.execute(query,(id,page))
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