"""Application Enrty Point"""

from app import create_app, socketio


app = create_app()  # pylint: disable=invalid-name

if __name__ == "__main__":
    socketio.run(app)
