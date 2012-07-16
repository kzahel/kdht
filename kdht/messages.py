import constants
import bencode
import struct

class RPCResponse(object):
    def __init__(self, payload):
        self.data = bencode.bdecode(payload)

    def get_transaction_id(self):
        return self.data['t']

    def get_message_type(self):
        if self.data['y'] == 'q':
            return 'query'
        elif self.data['y'] == 'r':
            return 'response'
        elif self.data['y'] == 'e':
            return 'error'

    def parse_ip(self, chars):
        return '.'.join( map(str, struct.unpack("!BBBB", chars)) )

    def get_response(self):
        return self.data['r']

    def __repr__(self):
        return '<RPCResponse %s>' % self.data

class RPCMessage(object):
    def __init__(self, query, arguments):
        self.query = query
        self.arguments = arguments

    def get_data(self):
        return {'t': chr(int(random.random()*256)) + chr(int(random.random()*256)),
                'q': self.query,
                'y': 'q',
                'a': self.arguments}

    def get_payload(self):
        return bencode.bencode(self.get_data())




ping_message = {"t":"aa", "y":"q", "q":"ping", "a":{"id":constants.MY_ID}}
