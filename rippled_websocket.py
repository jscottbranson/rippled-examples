# Code by rabbit:
#   * https://rabbitkick.club or @rabbitkickclub on Twitter

# This script provides an example/template using python3 to connect to a rippled
# node via websocket (WS). WS must also be configured in the node's rippled.cfg file.
# This script uses the 'websocket' module, which is available via pip.
# This script is based on this example: https://github.com/websocket-client/websocket-client

# This is offered 'as is'. Users will likely need to modify the script to meet their
# individual needs.

# Subscriptions provide ongoing information on the XRP ledger's state, including transactions.
# One use for this script is monitoring transaction flows or other data from the ledger.

import numpy #makes websocket faster
import websocket
import json
#import ssl #only need ssl to disable wss cert verification.

# Specify the server to connect to
ws_address = "wss://s1.ripple.com:443"

# Tailor subscriptions here
# Subscriptions are described in the rippled documentation:
# https://ripple.com/build/rippled-apis/#subscribe
ledger = '{"id": "1", "command": "subscribe", "streams": ["ledger"]}'
server = '{"id": "1", "command": "subscribe", "streams": ["server"]}'
validations = '{"id": "1", "command": "subscribe", "streams": ["validations"]}'

# Use the following variable to define which subscription to use
ws_command = ledger

# Change what information is displayed by adding code to the appropriate 'parse_xxxxx' methods'
class ws:
    def __init__(self):
        self.command = ws_command
        self.address = ws_address
        self.record_txl_high = int()

    def parse_ledger(self, message):
        m = message
        if m['txn_count'] > self.record_txl_high:
            self.record_txl_high = m['txn_count']
        print("Ledger ID:", m['ledger_index'], "contained", m['txn_count'], 'transactions.')
        print("Record high tx/ledger:", self.record_txl_high)
        print("-------------------------------------------")

    def parse_server(self, message):
        print(message)
        print("-------------------------------------------")

    def parse_validations(self, message):
        print(message)
        print("-------------------------------------------")

    def on_message(self, ws, message):
        message = json.loads(message)
        #Decide which method to use to parse the message
        if self.command == ledger:
            self.parse_ledger(message)
        elif self.command == server:
            self.parse_server(message)
        elif self.command == validations:
            self.parse_validations(message)

    def on_error(self, ws, error):
        print("Error:", error)

    def on_close(self, ws):
        print("WS connection closed.")

    def on_open(self, ws):
        ws.send(self.command)

    def websocket_launch(self):
        ws = websocket.WebSocketApp(self.address,
                                    on_message = self.on_message,
                                    on_error = self.on_error,
                                    on_close = self.on_close)
        ws.on_open = self.on_open

        # To disable ssl verification:
        #   1. Uncomment 'import ssl' at the top of this file
        #   2. Uncomment the first line that starts with 'ws.run_forever(sslopt=...'
        #   3. Comment/remove the second 'ws.run_forever()' line 
        #ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.run_forever()

ws().websocket_launch()
