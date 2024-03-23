from flask import Flask, request
from flask_cors import CORS

import kanu
import kanu.auth
import kanu.user
import kanu.hobby


app = Flask(__name__)
CORS(app)

def arg_check(required_fields: list[str], args: dict) -> bool:
    return all(field in args for field in required_fields)
    

def is_session_valid(headers: dict) -> bool:
    if "session" not in headers:
        return False
    session = headers.get("session")
    return kanu.auth.is_session_valid(session)

# AUTH API ENDPOINTS

@app.route("/api/login", methods=["POST"])
def login():
    reuqired_fields = ["email", "password"]
    if not arg_check(reuqired_fields, request.json):
        return {"message": "missing required fields"}, 400
    email = request.json["email"]
    password = request.json["password"]
    session = kanu.auth.login(email, password)
    if session is None:
        return {"message": "invalid email or password"}, 401
    return {"session": session}

@app.route("/api/signup", methods=["POST"])
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


# USER API ENDPOINTS

@app.route("/api/me", methods=["GET"])
def get_user():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    user = kanu.user.get_user(session=request.headers.get("session"))
    return user.to_json(), 200

@app.route("/api/me", methods=["POST"])
def update_user():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    required_fields = ["name", "gender", "age", "nickname", "loc_agree"]
    if not arg_check(required_fields, request.json):
        return {"message": "missing required fields"}, 400
    
    user = kanu.user.get_user(session=request.headers.get("session"))
    user.change(**request.json)
    kanu.user.update_user(user)
    return {"message": "success"}, 200

@app.route("/api/user", methods=["GET"])
def get_user_by_id():
    if not is_session_valid(request.headers):
        return {"message": "invalid session"}, 401
    
    if "id" not in request.args:
        return {"message": "missing required fields 'id'"}, 400
    
    user = kanu.user.get_user(id=request.args.get("id"))
    return user.to_json(), 200


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
    
    user = kanu.user.get_user(session=request.headers.get("session"))
    hobbies = kanu.hobby.get_user_hobby(user)
    return {"hobbies": hobbies}, 200
