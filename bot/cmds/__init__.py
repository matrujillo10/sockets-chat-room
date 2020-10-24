"""Commands module"""

import os
from rabbitmq_rpc import server as Server


server = Server.RPCServer(
    queue_name="default", amqp_url=os.environ["AMQP_URL"], threaded=True
)
