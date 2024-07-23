"""
Server that is the base of the main application
It serves the pre-built vue frontend

Server: Flask

Task:
[In Progress] merge this with the local application so we do not need to have the unnecessary traffic between local application and the server
"""
from flask import Flask, render_template, request, jsonify
from flask import before_render_template
from flask_socketio import SocketIO, emit
from flask_executor import Executor
from werkzeug.serving import WSGIRequestHandler
import logging
import subprocess
import shlex
import sys
from time import sleep

flask_app = Flask(__name__, 
                  template_folder='.',
                  static_url_path='')
flask_app.logger.setLevel(logging.DEBUG)
socketio = SocketIO(flask_app)
executor = Executor(flask_app)

useShell = False
running = True
allow_http_commands = False
command_file = 'commands.txt'
command_dict = dict()


def usage(return_val: int):
    print("""
please write this...

""")
    sys.exit(return_val)

def parse_file(file: str) -> dict:
    """
    Read in commands from a file

    One command per line, lines formatted like this:
    [key] [sleep_period] [commands]...

    NOTE: at the moment, it is assumed that you are ok with whatever command you have being executed here
    The command is not checked for safety.

    In the future we might need to clean this, but at the moment I think it is fine
    """
    command_dict = dict()
    try:
        with open(file, 'r') as cmd_file:
            lines = cmd_file.readlines()
            for line in lines:
                cleaned = line.rstrip().split(' ')
                assert len(cleaned) >= 3, f"malformed line: {line.rstrip()}"
                key = cleaned.pop(0)
                sleep_period = cleaned.pop(0)
                try:
                    sleep_period = int(sleep_period)
                except ValueError:
                    logging.error(f"sleep value: {sleep_period} could not be converted into an integer")
                
                # please make this better
                if '|' not in cleaned:
                    command = shlex.split(' '.join(cleaned))
                else:
                    command = [ ' '.join(cleaned) ]
                command_dict[key] = (sleep_period, command)
    except FileNotFoundError:
        logging.error(f"invalid file {file}")
        usage(1)
    
    return command_dict

def process_command(command) -> str:
    """
    Run the given command and return the output

    The program will split the command for you if necessary

    TODO: test on windows
    """
    assert type(command) is list, f"command parser failed! - invalid command type {type(command)} only str and list are allowed"
    if useShell:
        logging.warning("Using shell=True opens program to shell injections")
    flask_app.logger.info(f"Running command {command}")
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=useShell)
    return result.stdout.decode('utf-8').rstrip()

@executor.job
def command_thread(key, sleep_period, command) -> bool:
    """
    Thread that processes a given command.

    Calls the command, sends the output to the server, and sleeps for the specified time

    Returns a boolean - true if the process was killed normally, false if the process ended
    prematurely (e.g. if the server did not respond)

    NOTE: the frontend is responsible for handling whatever is sent to it
    """
    global running
    while running:
        result = process_command(command)
        jresult = {
            key: result
        }
        flask_app.logger.info(f"Update: {key} ({sleep_period}) : {result}")
        socketio.emit('incoming_data', jresult)
        sleep(sleep_period)
    return True

@flask_app.route("/")
def main_page():
    """
    The only thing that should ever be called by the end user
    """
    return render_template('index.html')

@flask_app.route("/commands", methods=['GET'])
def see_commands():
    """
    Get a list of all currently running commands
    """
    return jsonify(command_dict)

@flask_app.route("/commands/add", methods=['POST'])
def add_command():
    """
    Add a command to the command dict and immediately start a job for the new command

    NOTE: since this lets anyone on the network add commands, might want to check to make sure they are acceptable commands

    On the other hand, that is a pain so it might be simpler to let the user turn off this feature
    """
    if not allow_http_commands:
        flask_app.logger.info("A POST request was sent to /commands/add but was blocked")
        return jsonify({'error': '/commands/add is turned off for this application'})
    data = request.json
    if not all(i in {'key', 'sleep_period', 'command'} for i in data):
        flask_app.logger.warning(f"Malformed request to /commands/add: {data}")
        return jsonify({'error': 'see creativity-optional wiki for information about /commands/add'})
    
    # TODO: parse the command so it is in the right format
    command_dict[data['key']] = (data['sleep_period'], data['command'])
    flask_app.logger.info(f"added command to be executed: {data['key']} ({data['sleep_period']}) : {data['command']}")
    command_thread.submit(data['key'], data['sleep_period'], data['command'])

@flask_app.route("/general_in", methods=['POST'])
def general_in():
    """
    Recieve misc information of the form
    { 
        key: data
    }

    the server emits a 'incoming_data' message to all connected websockets when new data is added

    NOTE: should probably keep this route open as a way for other things on the network to contribute data
    """
    data = request.json
    # just send the data to the frontend, no need to record it here
    socketio.emit('incoming_data', data)
    response = {"message": f"received data: {data}"}
    return jsonify(response)

@flask_app.route("/output/stream", methods=['GET'])
def output_stream():
    """
    Serve next frame of video

    Plan:
    use the server-side rendering aspects of threejs
    that most likely means we will have a node application constantly rendering the scene that output images to a folder
    this method then grabs the most recent one and sends it to the client

    this would *only* be useful when running the server on a second device because it would introduce more overhead
    that and, why send it back and forth if you are just rendering locally anyways
    """
    return jsonify({'error': 'not implemented, look at creativity-optional wiki'})

@flask_app.route("/shutdown", methods=['GET'])
def shutdown_server():
    """
    Tell the process threads to quit and shut the server down
    """
    global running
    running = False
    flask_app.logger.warning("/shutdown tells all of the execution threads to stop but does not actually stop the server")
    return jsonify({'message': 'shutting down server'})

@flask_app.errorhandler(404)
def page_not_found(error):
    """
    Error page.
    May someone please make this
    """
    return "page not found", 404

# sockets!
@socketio.on('connect')
def connect():
    """
    This gets called when something connects via websocket

    This log message is just a formality since the server does not do anything when recieving messages, it just sends them
    """
    flask_app.logger.info("Someone connected to the websocket!")
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def disconnect():
    """
    Client disconnected, turn off execution threads
    """
    flask_app.logger.info("Socket disconnected, turning off threads")
    global running
    running = False

def command_setup(sender, template, context, **extra):
    """
    Called when a new connection is made
    """
    sender.logger.debug('Rendering template "%s" with context %s',
                        template.name or 'string template',
                        context)
    command_dict = parse_file(command_file)
    sender.logger.info(f"Command dictionary: {command_dict}")
    for name in command_dict:
        sleep_period, command = command_dict[name]
        sender.logger.info(f"Adding command: {name} ({sleep_period}) : {command}")
        command_thread.submit(name, sleep_period, command)
    

before_render_template.connect(command_setup, flask_app)

if __name__ == "__main__":
    """
    Start the server


    NOTE: this is a development server, for now it is probably fine
    """
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    socketio.run(flask_app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=8000)