import os

from flask import Flask, render_template,request,jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

chats=[]

@app.route("/")
def index():
    #return "Project 2: TODO"
    return render_template("index.html",chats=chats)

@socketio.on("new chat petition")
def newchat(data):
    print("petition")
    newChatName = data["newchatname"]
    #se puede hacer sin broadcast?
    if newChatName in chats:
        emit("new chat",{"success": False}, broadcast=True)
        print("Taken "+ newChatName)
    else:
        chats.append(newChatName)
        newIndex = len(chats)-1
        print("New index number: "+str(newIndex))
        emit("new chat", {"success": True, "newChatName" : newChatName, "newIndex": newIndex}, broadcast=True)
        print("Available "+ newChatName)

@app.route("/<int:chatnumber>")
def chatroom(chatnumber):
    return (render_template("chatview.html",chatnumber=chatnumber))




if __name__ == '__main__':
    socketio.run(app, debug=True)
