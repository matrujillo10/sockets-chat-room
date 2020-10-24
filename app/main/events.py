"""Sockets events"""

import os
from datetime import datetime
from threading import Thread
from flask import session, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from rabbitmq_rpc.client import RPCClient
from rabbitmq_rpc.exceptions import RemoteCallTimeout, RemoteFunctionError
import pika

from .. import socketio, db
from ..models.message import Message
from ..models.command import Command


def parse_message(message):
    """Parse Message to dict"""
    return {
        "msg": message.message,
        "sender": message.sender.name,
        "sent_on": message.sent_on.strftime("%b %d %y - %H:%M"),
    }


@socketio.on("joined", namespace="/chat")
def joined(_):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room.
    And list of last 50 message of the room are sent to the
    client that just connected."""
    room = session.get("room")
    join_room(room)
    emit("status", {"msg": current_user.name + " has entered the room."}, room=room)
    messages = [
        parse_message(m)
        for m in db.session.query(Message)
        .filter(Message.room == room)
        .order_by(Message.sent_on.desc())
        .limit(50)
    ][
        ::-1
    ]  # List is reversed due do desc order
    emit("message", messages, room=request.sid)


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if message["msg"] == "":
        return
    room = session.get("room")
    # Command must have a the following structure: /command-name[=p1,p2,p3].
    # Command name can not have = symbol
    command = (
        db.session.query(Command)
        .filter(Command.cmd == message["msg"].split("=")[0])
        .first()
    )
    msg = Message(message=message["msg"], room=room, sender=current_user)

    if command:
        # Command detected: Send to RabbitMQ, then Bot must process it
        data = message["msg"].split("=")  # Split command from params
        # Delete slash and replace dash to create a valid function name
        cmd = data[0].replace("/", "").replace("-", "_")
        params = []
        if len(data) > 1:  # command has params
            params = data[1:]  # get params
            # Convert params to a string comma separated.
            # this is becuase possible existence of '=' char in params
            params = "".join(params)
            params = params.split("|")  # Split params using pipe sep

        @copy_current_request_context
        def rpc():
            client = RPCClient(amqp_url=os.environ["AMQP_URL"])
            try:
                res = getattr(client, f"call_{cmd}")(
                    params, __routing_key="default", __timeout=5
                )  # Call RPC command
                emit(
                    "message",
                    [
                        {
                            "msg": res,
                            "sender": command.bot_name,
                            "sent_on": datetime.now().strftime("%b %d %y - %H:%M"),
                        }
                    ],
                    room=room,
                )
            except (RemoteCallTimeout, RemoteFunctionError) as exc:
                print(str(exc))
                emit(
                    "message",
                    [
                        {
                            "msg": "Sorry! I was not able to process your request at this moment :/",
                            "sender": command.bot_name,
                            "sent_on": datetime.now().strftime("%b %d %y - %H:%M"),
                        }
                    ],
                    room=request.sid,
                )

        Thread(target=rpc).start()  # Call Async RPC
        msg.sent_on = datetime.now()
    else:
        # add the new message to the database
        db.session.add(msg)
        db.session.commit()

    emit("message", [parse_message(msg)], room=room)


@socketio.on("left", namespace="/chat")
def left(_):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    leave_room(room)
    emit("status", {"msg": current_user.name + " has left the room."}, room=room)
