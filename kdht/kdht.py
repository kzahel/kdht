import twisted
import twisted.internet.reactor
import util
import sys
import constants
import logging
import messages
import bencode
from twisted.internet import protocol, defer

class KademliaProtocol(protocol.DatagramProtocol):

    def datagramReceived(self, datagram, address):
        #logging.info ('recv datagram %s' % [datagram, address])
        message = messages.RPCResponse(datagram)
        logging.info ('parse datagram %s' % [message])

class Node(object):
    mine = None # my own node

    def __init__(self, address=None, network=None):
        self.network = network
        self.address = address

    def ping(self):
        self.network.send( messages.ping_message, self.address )

    def find_node(self, id):
        message = messages.RPCMessage('find_node', {"id":MY_ID, "target":hex_chr(MyNetwork.instance.id)})
        self.network.send( message, self.address )

class RoutingTable(object):
    def __init__(self):
        pass

from routingtable import OptimizedTreeRoutingTable

class MyNetwork(object):
    instance = None

    def __init__(self, port=4000):
        MyNetwork.instance = self
        self.port = port
        self._protocol = KademliaProtocol()
        self.id = constants.MY_ID

        self.routing = OptimizedTreeRoutingTable(self.id)

        twisted.internet.reactor.listenUDP(self.port, self._protocol)
        logging.info('listening on %s' % self.port)

        node = Node( network=self, address = ('67.180.11.105', 39265) )
        node.ping()

    def send(self, data, address):
        logging.info('send %s to addr %s' % (data, address))
        self._protocol.transport.write( bencode.bencode(data), address )

if __name__ == '__main__':
    node = MyNetwork()
    
    from twisted.internet import reactor
    from twisted.cred import portal, checkers 
    from twisted.conch import manhole, manhole_ssh 

    def getManholeFactory(namespace):
        realm = manhole_ssh.TerminalRealm()
        def getManhole(_): 
            return manhole.Manhole(namespace) 
        realm.chainedProtocolFactory.protocolFactory = getManhole
        p = portal.Portal(realm)
        p.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(admin='foobar'))
        f = manhole_ssh.ConchFactory(p)
        return f

    reactor.listenTCP(2222, getManholeFactory(globals()))
    reactor.run()

