import kanu
import kanu.auth
import kanu.message
import kanu.user
import kanu.room
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Global dictionary to store roomid and corresponding sockets
room_sockets = {}
def arg_check(required_fields: list[str], args: dict) -> bool:
    return all(field in args for field in required_fields)

@app.route('/api/message', methods=['POST'])
def receive_message():
    data = request.json
    required_fields = ["roomid","sessionid","message"]
    if not arg_check(required_fields,data):
        return jsonify({'status': 400, 'message' : 'Some argument is not exist'})
    roomid = data.get('roomid')
    sessionid = data.get('sessionid')
    message = data.get('message')
    if not kanu.auth.is_session_valid(sessionid):
        return jsonify({'status': 401, 'message' : 'UnAuthorized'})
    if roomid and sessionid and message:
        user = kanu.auth.get_user_by_session(sessionid)
        if not kanu.room.is_user_in_room(user,roomid):
            return jsonify({'status': 401, 'message' : 'UnAuthorized'})
        # Save message to database
        kanu.message.create_message(roomid, message, sessionid)
        # Check if roomid exists in room_sockets dictionary
        if roomid in room_sockets:
            # Iterate over sockets in the room and send the message
            for sid in room_sockets[roomid]:
                socketio.emit('message', {'roomid': roomid, 'sessionid': sessionid, 'message': message}, room=sid)
        
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Missing roomid, sessionid, or message'}), 400


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('join')
def handle_join(data):
    roomid = data['roomid']
    sessionid = data['sessionid']
    join_room(roomid)
    
    # Add socket to room_sockets dictionary
    if roomid not in room_sockets:
        room_sockets[roomid] = set()
    room_sockets[roomid].add(request.sid)
    
    print(f'Session {sessionid} joined room {roomid}')


if __name__ == '__main__':
    socketio.run(app)
