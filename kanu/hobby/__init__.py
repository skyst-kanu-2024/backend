import kanu
from kanu.user import User

class Hobby:
    id: int
    name: str

class HobbyMatch:
    hobbyname: Hobby.name
    userid: User.id

def create_hobby( #만약 hobby가 존재하지 않으면 추가
    name: str,
) -> Hobby:
    pass

def get_hobby( #hobby들이 뭐 있는지 불러옴.
    hobbyname: str = None,
) -> Hobby:
    pass

def update_hobby( #아마 쓰지는 않을 거 같은데... admin 계정이 할 수 있는 것일듯?
    hobby: Hobby,
):
    pass

def delete_hoobby(
    hobbyname: str,
):
    pass

def get_user_hobby(
    hobbyname: Hobby.name,
    userid: User.id,
) -> HobbyMatch:
    pass

def update_user_hobby(
    userid: User.id,
    hobbyname: Hobby.name,
) -> HobbyMatch:
    pass

def delete_user_hobby(
    userid: User.id,
    hobbyname: Hobby.name,
)-> HobbyMatch:
    pass

