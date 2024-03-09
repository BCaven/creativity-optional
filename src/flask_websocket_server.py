from flask import Flask
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect(auth):
    print("connection...")
    emit('my response', {'data': 'Connected'})
    return True

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('audio_in')
def handle_message(data):
    print(f"recieved audio in: {data}")


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)