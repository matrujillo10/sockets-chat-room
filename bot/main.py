"""Bot for processing commands"""

from cmds import server
from cmds.stock import stock

if __name__ == "__main__":
    print("[x] Server started... Waiting for RPC's")
    server.run()
