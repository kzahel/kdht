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

foobar = 99

reactor.listenTCP(2222, getManholeFactory(globals()))
reactor.run()
