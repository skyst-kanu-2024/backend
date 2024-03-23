import kanu
import kanu.database
from kanu.user import User
from kanu.room import Room

class UserLocation:
    userid: User.id
    lat: float
    lng: float

class UserDeviceToken:
    userid: User.id
    roomid: Room.id
    devicetoken: str

def setup():
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE 'user_location'(
            'user_id' VARCHAR(32) NOT NULL PRIMARY KEY,
            'lat' DOUBLE
            'lng' DOUBLE
            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """
    )
    cursor.execute(
        """CREATE TABLE 'user_device_token'(
            'user_id' VARCHAR(32) NOT NULL PRIMARY KEY,
            'room_id' VARCHAR(32)
            'devicetoken' VARCHAR(64)
            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
            FOREIGN KEY(room_id) REFERENCES room(id) ON DELETE CASCADE
        )
        """
    )

def create_user_location(
    userid: User.id,
    lat: float,
    lng: float
) -> UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_location(user_id, lat, long) VALUES (%s, %f, %f)", (userid), (lat), (lng)
    )
    pass

def get_user_location(
    userid: User.id
)->UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM user_location
            WHERE user_id=%s
        """, (userid)
    )
    data: list[tuple[str, float, float]] = cursor.fetchall()
    ndata = [UserLocation(userid=user_id, lat=lat, lng=lng) for user_id, lat, lng, in data]
    return ndata

def update_user_location(
    userid: User.id,
    lat: float,
    lng: float
)->UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE user_location
            SET lat=%s, lng=%s
            WHERE user_id=%s
        """, (lat), (lng), (userid)
    )
    pass

def delete_user_hobby( #user가 본인 hobby 삭제 할 때
    userid: User.id,
)-> UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM user_location
            WHERE user_id=%s
        """, (userid)
    )
    pass


def create_user_device_token(
    userid: User.id,
    roomid: Room.id,
    devicetoken: str
) -> UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_device_token(user_id, room_id, device_token) VALUES (%s, %f, %f)", (userid), (roomid), (devicetoken)
    )
    pass

def get_user_device_token(
    userid: User.id
)->UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM user_device_token
            WHERE user_id=%s
        """, (userid)
    )
    data: list[tuple[str, str, str]] = cursor.fetchall()
    ndata = [UserLocation(userid=user_id, roomid=room_id, devicetoken=device_token) for user_id, room_id, device_token, in data]
    return ndata

def update_user_device_token(
    userid: User.id,
    roomid: Room.id,
    devicetoken: str
)->UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE user_device_token
            SET roomid=%s, lng=%s
            WHERE user_id=%s
        """, (roomid), (devicetoken), (userid)
    )
    pass

def delete_user_device_token( #user가 본인 hobby 삭제 할 때
    userid: User.id
)-> UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM user_device_token
            WHERE user_id=%s
        """, (userid)
    )
    pass

