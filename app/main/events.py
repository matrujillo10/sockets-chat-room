"""Socket events"""

from flask import session, request
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from .. import socketio, db
from ..models.message import Message


def parse_message(message):
    """Parse Message to dict"""
    return {
        "msg": message.message,
        "sender": message.sender.name,
        "sent_on": message.sent_on.strftime("%b %d %y - %H:%M:%S"),
    }


@socketio.on("joined", namespace="/chat")
def joined(_):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    join_room(room)
    emit("status", {"msg": current_user.name + " has entered the room."}, room=room)
    messages = [
        parse_message(m)
        for m in db.session.query(Message)
        .filter(Message.room == room)
        .order_by(Message.sent_on.desc())
        .limit(50)
    ][::-1]
    emit("message", messages, room=request.sid)


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    # TODO: Check if message is commmand
    # add the new message to the database
    msg = Message(message=message["msg"], room=room, sender=current_user)
    db.session.add(msg)
    db.session.commit()
    emit("message", [parse_message(msg)], room=room)


@socketio.on("left", namespace="/chat")
def left(_):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    print("Exiting...")
    room = session.get("room")
    leave_room(room)
    emit("status", {"msg": current_user.name + " has left the room."}, room=room)
