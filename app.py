from flask import Flask, request
from flask_cors import CORS

import kanu
import kanu.auth
import kanu.user
import kanu.hobby
import kanu.room
import kanu.location


app = Flask(__name__)
CORS(app)

roomreq: dict[kanu.user.User: list[kanu.user.User]] = {}

def arg_check(required_fields: list[str], args: dict) -> bool:
    return all(field in args for field in required_fields)
    

def is_session_valid(headers: dict) -> bool:
    print(headers)
    if "session_id" not in headers:
        return False
    session = headers.get("session_id")
    return kanu.auth.is_session_valid(session)

# AUTH API ENDPOINTS

#@app.route("/api/login", methods=["POST"])
def login():
    reuqired_fields = ["email", "password"]
    if not arg_check(reuqired_fields, request.json):
        return {"message": "missing required fields"}, 400
    email = request.json["email"]
    password = request.json["password"]
    session = kanu.auth.login(email, password)
    if session is None:
        return {"message": "invalid email or password"}, 401
    return {"session_id": session}

#@app.route("/api/signup", methods=["POST"])
def signup():
    required_fields = ["name", "email", "gender", "age", "nickname", "password"]
    if not arg_check(required_fields, request.json):
        return {"message": "missing required fields"}, 400
    
    user = kanu.user.create_user(**request.json)
    return {"message": "success"}, 200

@app.route("/api/session", methods=["GET"])
def check_session():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    return {"message": "valid session"}, 200

@app.route("/api/auth", methods=["POST"])
def google_auth():
    if "token" not in request.json:
        return {"message": "missing required field 'token'"}, 400
    
    token = request.json["token"]
    session = kanu.auth.login(token)
    if session is None:
        return {"message": "invalid token"}, 401
    return {"session_id": session}, 200

# USER API ENDPOINTS

@app.route("/api/me", methods=["GET"])
def get_user():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    return user.with_profile(), 200

@app.route("/api/me", methods=["POST"])
def update_user():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    required_fields = ["name", "gender", "age", "nickname", "loc_agree"]
    if not arg_check(required_fields, request.json):
        return {"message": "missing required fields"}, 400
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    user.change(**request.json)
    kanu.user.update_user(user)
    return {"message": "success"}, 200

@app.route("/api/user", methods=["GET"])
def get_user_by_id():
    if not is_session_valid(request.headers):
        print(request.headers)
        return {"message": f"invalid session {request.headers.get('session_id')} / {kanu.auth.is_session_valid(request.headers.get('session_id'))}"}, 401
    
    if "id" not in request.args:
        return {"message": "missing required fields 'id'"}, 400
    
    user = kanu.user.get_user(id=request.args.get("id"))
    if user is None:
        return {"message": "user not found"}, 204
    return user.with_profile(), 200


# Hobby Name API ENDPOINTS

@app.route("/api/hobbylist", methods=["GET"])
def get_hobby_list():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    hobbies = kanu.hobby.get_hobby_list()
    return {"hobbies": hobbies}, 200

@app.route("/api/hobbylist", methods=["POST"])
def create_hobby():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    if "name" not in request.json:
        return {"message": "missing required field 'name'"}, 400
    
    if not kanu.hobby.is_hobby_exist(request.json["name"]):
        kanu.hobby.create_hobby(request.json["name"])
        return {"message": "success"}, 200
    else:
        return {"message": "hobby already exists"}, 409

# Hobby Match API ENDPOINTS

@app.route("/api/userhobby", methods=["GET"])
def get_user_hobby():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    hobbies = kanu.hobby.get_user_hobby(user)
    return {"hobbies": hobbies}, 200

@app.route("/api/userhobby/<hobbyName>", methods=["DELETE"])
def delete_user_hobby(hobbyName):
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    session = request.headers.get("session_id")
    user = kanu.auth.get_user_by_session(session)
    kanu.hobby.delete_user_hobby(user, hobbyName)

@app.route('/api/nearLocations', methods=['GET']) #해당 유저가 다른 사람 location을 보는 로직
def get_nearby_users():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    session = request.headers.get("session_id")
    user = kanu.auth.get_user_by_session(session)

    # user_id와 max_distance를 검증하는 간단한 로직
    if not user.id is None:
        return {"message": "missing required field 'user id'"}, 400

    # 실제 환경에서는 user_id로 User 객체를 찾는 로직이 필요함
    try:
        near_users = kanu.location.get_near_user_distance(user)
        return {"near users": near_users}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    
@app.route('/api/nearLocations', methods=['POST']) #유저 본인의 location update하는 로직
def update_user_location():
    if not is_session_valid(request. headers):
        return {"message": "invalid session"}, 401
    
    session = request.headers.get("session_id")
    user = kanu.auth.get_user_by_session(session)
    
    required_fields = ["lat", "lng"]
    if not arg_check(required_fields, request.json):
        return {"message": "missing required fields"}, 400

    # user_id와 max_distance를 검증하는 간단한 로직
    if not user.id is None:
        return {"message": "missing required field 'user id'"}, 400

    # 실제 환경에서는 user_id로 User 객체를 찾는 로직이 필요함
    try:
        kanu.location.update_user_location(user)
        return {"message": "update user location success"}, 200
    except Exception as e:
        return {'error': str(e)}, 500

# ROOM API ENDPOINTS
    
@app.route("/api/room", methods=["POST"])
def request_room():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    required_fields = ["otheruserid"]
    if not arg_check(required_fields, request.json):
        return {"message": "missing required fields"}, 400
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    
    if user.id == request.json["otheruserid"]:
        return {"message": "cannot request room with yourself"}, 400
    
    otheruser = kanu.user.get_user(id=request.json["otheruserid"])
    if user in roomreq and otheruser in roomreq[user]:
        userM = user if user.gender == kanu.gender.M else otheruser
        userF = user if user != userM else otheruser
        room = kanu.room.create_room(userM, userF)
        return {"message": "room created", "room_id": room.id}, 201
    if otheruser in roomreq:
        if user in roomreq[otheruser]:
            return {"message": "already requested"}, 208
        roomreq[otheruser].append(user)
    else:
        roomreq[otheruser] = [user]

    return {"message": "requested"}, 200

@app.route("/api/room", methods=["GET"])
def get_room():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    rooms = kanu.room.get_room_by_user(user)
    return {"rooms": [room.id for room in rooms]}, 200

@app.route("/api/room_requests", methods=["GET"])
def get_room_requests():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    user = kanu.user.get_user(session=request.headers.get("session_id"))
    if user not in roomreq:
        return {"message": "no requests", "requests": []}, 200
    requests = [user.id for user in roomreq[user]]
    return {"requests": requests}, 200


if __name__ == "__main__":
    kanu.setup()
    app.run(host="0.0.0.0", port=5000, debug=True)