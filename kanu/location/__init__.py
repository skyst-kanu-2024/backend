import kanu
import kanu.database
import kanu.user
from kanu.user import User
from kanu.room import Room
from math import radians, cos, sin, sqrt, atan2

class UserLocation:
    user: User
    lat: float
    lng: float

    def __init__(self, user: User, lat: float, lng: float):
        self.user = user
        self.lat = lat
        self.lng = lng

class UserDeviceToken:
    user: User
    room: Room
    devicetoken: str

    def __init__(self, user: User, room: Room, devicetoken: str):
        self.user = user
        self.room = room
        self.devicetoken = devicetoken

from math import radians, cos, sin, sqrt, atan2

# Haversine 공식을 사용하여 두 지점 사이의 거리를 계산하는 함수 (결과 단위: 미터)
def calculate_distance(lat1, lng1, lat2, lng2):
    # 지구 반지름 (미터 단위)
    R = 6371.0 * 1000  # 킬로미터를 미터로 변환

    # 위도와 경도를 라디안 단위로 변환
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # 두 지점의 위도와 경도 차이
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # Haversine 공식
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # 계산된 거리 (미터 단위)
    return distance


def setup():
    conn = kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_location(
            user_id CHAR(32) NOT NULL PRIMARY KEY,
            lat DOUBLE,
            lng DOUBLE,
            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS user_device_token(
            user_id CHAR(32) NOT NULL PRIMARY KEY,
            devicetoken VARCHAR(64),
            FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
        )
        """
    )

def add_user_device_token(
    user: User,
    devicetoken: str
):
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_device_token(user_id, devicetoken) VALUES (%s, %s)", (user.id, devicetoken)
    )

def get_user_device_token(
    user: User
)->UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM user_device_token
            WHERE user_id=%s
        """, (user.id)
    )
    data = cursor.fetchone()
    return UserDeviceToken(user=user, room=kanu.room.get_room_by_id(data["room_id"]), devicetoken=data["devicetoken"])

def create_user_location(
    user: User,
    lat: float,
    lng: float
) -> UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_location(user_id, lat, long) VALUES (%s, %f, %f)", (user.id, lat, lng)
    )
    pass

def get_all_user_location(    
)->list[UserLocation]:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, lat, lng FROM user_location"
    )
    data = cursor.fetchall()
    ndata = []
    for dt in data:
        ndata.append(UserLocation(user=kanu.user.get_user(userid=dt["user_id"]), lat=dt["lat"], lng=dt["lng"]))
    
    return ndata
    
def get_near_user_distance(
        user: User,
    ):
    mylocation = get_user_location(user)
    alluserlocation = get_all_user_location()
    max_distance=1000
    near_users = []
    for location in alluserlocation:
        # 현재 사용자일 경우 건너뛰기
        if location.user.id == user.id:
            continue

        distance = calculate_distance(mylocation.lat, mylocation.lng, location.lat, location.lng)
        if distance <= max_distance:
            near_users.append({"userid":location.user.id, "distance":distance})
    return near_users
    

def get_user_location(
    user: User
)->UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM user_location
            WHERE user_id=%s
        """, (user.id)
    )
    data = cursor.fetchone()
    return UserLocation(user=user, lat=data["lat"], lng=data["lng"])

def update_all_user_location( # 안 씀 절대로
    alluser:list[UserLocation]
)->UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    for user in alluser:
        cursor.execute(
            """UPDATE user_location
                SET lat=%s, lng=%s
                WHERE user_id=%s
            """, (user.lat, user.lng, user.user.id)
        )
    

def update_user_location(
    user: kanu.user.User,
    lat: float,
    lng: float
)->UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    if get_user_location(user) is None:
        create_user_location(user, lat, lng)
    cursor.execute(
        """UPDATE user_location
            SET lat=%s, lng=%s
            WHERE user_id=%s
        """, (lat, lng, user.id)
    )

def delete_user_hobby( #user가 본인 hobby 삭제 할 때
    user: User
)-> UserLocation:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM user_location
            WHERE user_id=%s
        """, (user.id)
    )
    pass


def create_user_device_token(
    user: User,
    room: Room,
    devicetoken: str
) -> UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO 
        user_device_token(user_id, room_id, device_token) 
        VALUES (%s, %f, %f)""",
        (user.id, room.id, devicetoken)
        )
    pass

def get_user_device_token(
    user: User
)->UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM user_device_token
            WHERE user_id=%s
        """, (user.id)
    )
    data = cursor.fetchone()
    return UserDeviceToken(user=user, room=kanu.room.get_room_by_id(data["room_id"]), devicetoken=data["devicetoken"])

def update_user_device_token(
    user: User,
    room: Room,
    devicetoken: str
)->UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE user_device_token
            SET roomid=%s, lng=%s
            WHERE user_id=%s
        """, (room.id, devicetoken, user.id)
    )
    pass

def delete_user_device_token( #user가 본인 hobby 삭제 할 때
    user: User
)-> UserDeviceToken:
    conn= kanu.database.Database()
    cursor = conn.cursor()
    cursor.execute(
        """DELETE FROM user_device_token
            WHERE user_id=%s
        """, (user.id)
    )
    pass

