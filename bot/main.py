"""Bot for processing commands"""

import logging
from cmds import server
from cmds.stock import stock


if __name__ == "__main__":
    logging.info("Server started. Waiting for RPC's")
    server.run()
