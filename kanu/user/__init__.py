import kanu

class User:
    name: str
    email: str
    gender: kanu.gender
    age: int
    nickname: str

def create_user(
    name: str,
    email: str,
    gender: kanu.gender,
    age: int,
    nickname: str = None,
) -> User:
    pass

def get_user(
    userid: str = None,
    email: str = None,
) -> User:
    pass

def update_user(
    user: User,
):
    pass
