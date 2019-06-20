import os

from flask import Flask, render_template,request,jsonify
from flask_socketio import SocketIO, emit
from collections import deque
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


class Message:
    idCount=0
    def __init__(self, text, user,date,time):
        self.text = text
        self.user = user
        self.date = date
        self.time = time
        self.id =Message.idCount
        Message.idCount += 1

chats=[]
#this will be a list of deques
messages=[]

@app.route("/")
def index():

    return render_template("index.html",chats=chats)

@socketio.on("new chat petition")
def newchat(data):
    #print("petition")
    newChatName = data["newchatname"]

    if newChatName in chats:
        emit("new chat",{"success": False}, broadcast=True)

    else:
        chats.append(newChatName)
        newIndex = len(chats)-1
        #create deque of messages for new chat
        messages.append(deque(maxlen=100))

        emit("new chat", {"success": True, "newChatName" : newChatName, "newIndex": newIndex}, broadcast=True)


@socketio.on("send message")
def newmessage(data):
    print("message in server")
    newmessage=data["newmessage"]
    username=data["username"]
    chatnumber=data["chatnumber"]
    date=data["date"]
    time=data["time"]
    m=Message(newmessage,username,date,time)
    #qMsg=messages[chatnumber]
    messages[chatnumber].append(m)
    emit("new message", {"newmessage": newmessage, "username": username, "chatnumber": chatnumber,  "date":date,"time": time, "id":m.id}, broadcast=True)
    print("message broadcasted")

@socketio.on("delete message")
def delete(data):
    msgId=data["id"]
    chatnumber = data["chatnumber"]
    chatmessages = messages[chatnumber]

    index=0
    for m in chatmessages:
        if m.id == msgId:
            print(json.dumps(m.__dict__))
            break
        index += 1
    del messages[chatnumber][index]

    #prepare messages for json, convert to dict
    messagesindict=[]
    for m in messages[chatnumber]:
        messagesindict.append(m.__dict__)

    emit("load messages",{"chatmessages":messagesindict,"chatnumber":chatnumber})

@socketio.on("load request")
def load(data):

    chatnumber = data["chatnumber"]
    chatmessages = messages[chatnumber]
    messagesindict=[]
    for m in chatmessages:
        messagesindict.append(m.__dict__)
    emit("load messages",{"chatmessages":messagesindict,"chatnumber":chatnumber})

@app.route("/<int:chatnumber>")
def chatroom(chatnumber):
    qMsg=messages[chatnumber]
    return (render_template("chatview.html",chatnumber=chatnumber,messages=qMsg))




if __name__ == '__main__':
    socketio.run(app, debug=True)
