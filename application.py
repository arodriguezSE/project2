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
@app.route("/newchat", methods=["POST"])
def newchat():

    newChatName=request.form.get("chatname")

    if newChatName in chats:
        return jsonify({"success": False})

    else:
        chats.append(newChatName)
        return jsonify({"success": True })





if __name__ == '__main__':
    socketio.run(app, debug=True)
