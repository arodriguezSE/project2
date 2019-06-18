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
# @app.route("/newchat", methods=["POST"])
# def newchat():
#
#     newChatName=request.form.get("chatname")
#     print("got request to create" + newChatName)
#
#     if newChatName in chats:
#         #return jsonify({"success": False})
#         emit("new",{"success": False}, broadcast=True)
#         print("used name")
#
#     else:
#         chats.append(newChatName)
#         print("not used name")
#         return jsonify({"success": True })
#         print("trying")
#         emit("new", {"success": True, "newChatName" : newChatName}, broadcast=True)
#         #emit("chat added", {"newChatName" : newChatName}, broadcast=True)
#         print("event emited")

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
        emit("new chat", {"success": True, "newChatName" : newChatName}, broadcast=True)
        print("Available "+ newChatName)
    #print(newchatname)
    #emit("announce vote", {"selection": selection}, broadcast=True)







if __name__ == '__main__':
    socketio.run(app, debug=True)
