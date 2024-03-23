import kanu
import kanu.auth
import kanu.message
import kanu.user
import kanu.room
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins = '*')

# Global dictionary to store room_id and corresponding sockets
def arg_check(required_fields: list[str], args: dict) -> bool:
    return all(field in args for field in required_fields)


@socketio.on('connect')
def handle_connect(data):
    print('Client connected')
    #if not kanu.auth.is_session_valid(session_id):
    #    return jsonify({'status': 401, 'message': 'UnAuthorized'})



@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join')
def handle_join(data):
    room_id = data.get('room_id')
    '''user = kanu.auth.get_user_by_session(session_id)
    if not kanu.room.is_user_in_room(user,room_id):
        return jsonify({'status': 401, 'message' : 'UnAuthorized'})'''
    join_room(room_id)

    
@socketio.on('message')
def handle_message(data):
    print(data)
    room_id = data.get('room_id')
    message_content = data.get('message')
    userid = data.get('userid')
    
    if not arg_check(['room_id', 'message', 'userid'], data):
        # 필수 필드가 누락된 경우 처리
        return jsonify({'status': 400, 'message': 'Missing required fields'})
    
    # 메시지 생성
    kanu.message.create_message(room_id, message_content, userid)
    # 메시지가 생성되었다면 방 참여자에게 메시지 전송
    emit('message', data, room=room_id)
    

if __name__ == '__main__':
    socketio.run(app,allow_unsafe_werkzeug=True,host="0.0.0.0", port=5000, debug=True)
