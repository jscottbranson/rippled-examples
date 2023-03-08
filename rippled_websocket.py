'''
This script provides an example/template using python3 to connect to a rippled
node via websocket (WS). It's designed to get novice developers subscribed and engaged with
minimal effort. In order to subscribe, WS must be configured in the remote node's rippled.cfg file.
This script uses the 'websocket' module, which is available via pip.
This script is based on this example: https://github.com/websocket-client/websocket-client

This is offered 'as is'. Users will likely need to modify the script to meet their
individual needs.

Subscriptions provide ongoing information on the XRP Ledger's state, including transactions.
'''

import sys
import ssl # This is only used to disable wss cert verification.
import json

import websocket # 'pip install websocket-client'

# Specify the server to connect to
WS_ADDRESS = "wss://xrplcluster.com:443"

# Tailor subscriptions here
# Subscriptions are described in the rippled documentation:
# https://ripple.com/build/rippled-apis/#subscribe
LEDGER = {"id": "example_ws", "command": "subscribe", "streams": ["ledger"]}
SERVER = {"id": "example_ws", "command": "subscribe", "streams": ["server"]}
VALIDATIONS = {"id": "example_ws", "command": "subscribe", "streams": ["validations"]}
TRANSACTIONS = {"id": "example_ws", "command": "subscribe", "streams": ["transactions", "transactions_proposed"]}
CONSENSUS = {"id": "example_ws", "command": "subscribe", "streams": ["consensus"]}
MANIFESTS = {"id": "example_ws", "command": "subscribe", "streams": ["manifests"]}
BOOKS = {
    "command": "subscribe",
    "books": [
        {
            "taker_pays": {
                "currency": "XRP"
            },
            "taker_gets": {
                "currency": "USD",
                "issuer": "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"
            },
            "snapshot": "true"
        },
        {
            "taker_pays": {
                "currency": "USD",
                "issuer": "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq"
            },
            "taker_gets": {
                "currency": "XRP"
            },
            "snapshot": "true"
        },
        ]
}

# Use the following variable to define which subscription to use
WS_COMMAND = json.dumps(MANIFESTS)

class Ws:
    '''
    Open a websocket connection, send the subscription command,
    and parse messages from the web server.
    '''
    def __init__(self):
        self.websocket_launch()

    def on_message(self, ws, message):
        message = json.loads(message)
        print(json.dumps(message, indent=4, sort_keys=True))

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WS connection closed. Status code: {close_status_code}.\nMessage: {close_msg}")

    def on_open(self, ws):
        '''
        Initial command to send after opening the websocket.
        '''
        self.socket.send(WS_COMMAND)

    def websocket_launch(self):
        '''
        Construct and open the websocket connection.
        To disable ssl verification:
          1. Comment/remove the first 'ws.run_forever()' line below
          2. Uncomment the second line that starts with 'ws.run_forever(sslopt=...'
        '''
        self.socket = websocket.WebSocketApp(
            WS_ADDRESS,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open,
        )

        try:
            self.socket.run_forever()
            #self.socket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except KeyboardInterrupt:
            sys.exit()

try:
    Ws()
except KeyboardInterrupt:
    sys.exit()
