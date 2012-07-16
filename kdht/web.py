from twisted.internet import reactor
from twisted.web import static, server
from twisted.web.resource import Resource

import json

class Hello(Resource):

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        data = dict( (k,str(v)) for k,v in request.__dict__.items() )
        request.setHeader('Content-Type','text/plain')

        if 'qs' in request.args:
            return self.debug_eval(request.args['qs'][0])

        return json.dumps(  data, indent=2 )

    def debug_eval(self, qs):
        if qs:
            try:
                try:
                    result = eval(qs)
                    try:
                        return result.__repr__()
                    except:
                        return str(result)
                except SyntaxError:
                    exec(qs)
                    return ''
            except Exception, e:
                import traceback
                return traceback.format_exc()


site = server.Site(Hello())
reactor.listenTCP(8000, site)
reactor.run()
