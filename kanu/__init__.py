import enum
import os

class gender(enum.IntEnum):
    MALE = 1
    M = 1
    FEMALE = 2
    F = 2

import kanu.database
import kanu.user
import kanu.auth
import kanu.hobby
import kanu.room
import kanu.message
import kanu.location
class Config:
    host: str
    port: int
    user: str
    password: str
    database: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")



def setup():
    kanu.config = Config()

    kanu.database.setup()
    kanu.user.setup()
    kanu.auth.setup()
    kanu.hobby.setup()
    kanu.room.setup()
    kanu.message.setup()