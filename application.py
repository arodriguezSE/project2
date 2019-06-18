import os

from flask import Flask, render_template,request,jsonify
from flask_socketio import SocketIO, emit
from collections import deque

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

class Message:
    def __init__(self, text, user,date,time):
        self.text = text
        self.user = user
        self.date = date
        self.time = time

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
    #se puede hacer sin broadcast?
    if newChatName in chats:
        emit("new chat",{"success": False}, broadcast=True)
        #print("Taken "+ newChatName)
    else:
        chats.append(newChatName)
        newIndex = len(chats)-1
        #create deque of messages for new chat
        messages.append(deque(maxlen=100))
        #print("New index number: "+str(newIndex))
        emit("new chat", {"success": True, "newChatName" : newChatName, "newIndex": newIndex}, broadcast=True)
        #print("Available "+ newChatName)

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
    emit("new message", {"newmessage": newmessage, "username": username, "chatnumber": chatnumber,  "date":date,"time": time}, broadcast=True)
    print("message broadcasted")


@app.route("/<int:chatnumber>")
def chatroom(chatnumber):
    qMsg=messages[chatnumber]
    return (render_template("chatview.html",chatnumber=chatnumber,messages=qMsg))




if __name__ == '__main__':
    socketio.run(app, debug=True)
