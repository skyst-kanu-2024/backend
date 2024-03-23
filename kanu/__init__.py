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


def setup():
    kanu.config = Config()
    kanu.config.host = os.getenv("MYSQL_HOST")
    kanu.config.user = os.getenv("MYSQL_USER")
    kanu.config.password = os.getenv("MYSQL_PASSWORD")
    kanu.config.database = os.getenv("MYSQL_DATABASE")
    kanu.database.setup()
    kanu.user.setup()
    kanu.auth.setup()
    kanu.hobby.setup()
    kanu.room.setup()
    kanu.message.setup()