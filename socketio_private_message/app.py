from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_session import Session
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

users = {}
groupMessages={}
groups=['group1', 'group2', 'group3']

for group in groups:
    groupMessages[group]=[]

id=0


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orginate')
def orginate():
    socketio.emit('server orginated', 'Something happened on the server!')
    return '<h1>Sent!</h1>'

############## group messages testing  ################
@app.route('/test')
def test():
    return f'messages  --- {groupMessages}   ______grup_______ {groups}__________________             username  --- {session["currentUserName"]}    ___ {users} _______________ {session["currentRoom"]}'
##############################


@socketio.on('message from user', namespace='/messages')
def receive_message_from_user(message):
    emit('from flask', message, broadcast=True)

@socketio.on('username', namespace='/private')
def receive_username(username):
    users[username] = request.sid
    session["currentUserName"]=username
    #users.append({username : request.sid})
    #print(users)
    #print('Username added!')
    emit('username added', username)


@socketio.on('autoUsername', namespace='/private')
def receive_autoUsername(msg):
    message='not logged in'
    if session.get('currentUserName') :
        users[session["currentUserName"]] = request.sid
        message=session["currentUserName"]
    emit('auto_username added', {'message' : message})


@socketio.on('private_message', namespace='/private')
def private_message(payload):
    recipient_session_id = users[payload['username']]
    message = payload['message']

    emit('new_private_message', {'message' : message, 'sended by' : payload['from_whom']}, room=recipient_session_id)


@socketio.on('joiningToRoom', namespace='/private')
def group_message(roomname):
    if roomname['kind']=='auto':
        if session.get('currentRoom') :
            join_room(session['currentRoom'])
            emit('previousMessages', {'previous_messages' : groupMessages[session['currentRoom']], 'showBlock' : 'yes', 'currentRoomName' :  session['currentRoom']}, room=session['currentRoom'])
    else:
        leave_room(session['currentRoom'])
        join_room(roomname['roomname'])
        session['currentRoom']=roomname['roomname']
        emit('previousMessages', {'previous_messages' : groupMessages[roomname['roomname']], 'showBlock' : 'not', 'currentRoomName' :  roomname['roomname']}, room=roomname['roomname'])


# *****************************   appendin ici ++
@socketio.on('group_messaging', namespace='/private')
def group_message(payload):
    message = payload['message']
    # *****************************   emitin ici ++
    if payload['group_name']=='':
        if session['currentRoom']:
            groupMessages[session['currentRoom']].append(message+' sended by '+payload['from_whom'] + 'in _____ '+payload['time'])
            emit('new_group_message', {'message' : message, 'sended by' : payload['from_whom'], 'time' : payload['time']}, room=session['currentRoom'])
    else:
        groupMessages[payload['group_name']].append(message+' sended by '+payload['from_whom'] + 'in _____ '+payload['time'])
        emit('new_group_message', {'message' : message, 'sended by' : payload['from_whom'], 'time' : payload['time']}, room=payload['group_name'])


############  group list  error ################
@socketio.on('show_groups', namespace='/private')
def group_message(msg):
    emit('group_list', groups)
#################################################


@socketio.on('addNewGroup', namespace='/private')
def addNewGroup(groupName):
    permis=1
    msg='not add'
    for i in range(0,len(groups)):
        if groups[i]==groupName:
            permis=0
    if permis==1:
        groups.append(groupName)
        groupMessages[groupName]=[]
        msg='add'
        emit('permission', msg)
    emit('permission', {'message': msg}, broadcast=True)




'''
@socketio.on('message')
def receive_message(message):
    print('########: {}'.format(message))
    send('This is a message from Flask.')

@socketio.on('custom event')
def receive_custom_event(message):
    print('THE CUSTOM MESSAGE IS: {}'.format(message['name']))
    emit('from flask', {'extension' : 'Flask-SocketIO'}, json=True)

'''

if __name__ == '__main__':
    socketio.run(app)
