import enum

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

kanu.database.setup()
kanu.user.setup()
kanu.auth.setup()
kanu.hobby.setup()
kanu.room.setup()
kanu.message.setup()