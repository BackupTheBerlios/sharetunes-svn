"""
the original first attempt at the server.  Now is currently unused.  maybe
should bring back for more sophisticated networking
"""

import twisted.internet.reactor
import twisted.web.server
from twisted.web import static, resource

static.File.contentTypes.update( {'.mp3' : 'audio/x-mp3'})
static.File.contentTypes.update( {'.css' : 'text/css'})


class StaticFileResource(static.File):
    def getChild(self, path, request):
        if request.path == '/':
            return InterfaceResource()
        return static.File.getChild(self, path, request)

class InterfaceResource:
    def render(self, request):
        global template
        part1, part2 = template.split("%TRACKS_TABLE%")
        return part1 + open('tracks_table').read() + part2

class TopResource(resource.Resource):
    def __init__(self, playerFileRoot, musicFileRoot):
        resource.Resource.__init__(self)
        self.musicFileRoot = musicFileRoot
        self.playerFileRoot = playerFileRoot

    def render_GET(self):
        return open('interface.html').read()

    def getChild(self, path, request):
        if request.path == '/':
            return InterfaceResource()

        if path == 'musicroot':
            return StaticFileResource(self.musicFileRoot)
        if path == 'player':
            return StaticFileResource(self.playerFileRoot)
        else: raise Exception, "Dont know how to handle path: "+path+" --- "+str(request)

## import BaseHTTPServer
## import SimpleHTTPServer
## class MyReqHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
##     def do_GET(self):
##         if self.path == '/':
##             self.send_header('Content-Type', 'text/html')
##             self.send_header('Ooga', 'booga')
##             self.end_headers()
##             self.wfile.write(open('interface.html').read())
##             return
##         return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def startServer():
    PORT = 8000
    LOG = "servlet.log"
    twisted.internet.reactor.listenTCP(PORT,
      twisted.web.server.Site(TopResource('.', open('musicpath').read() )))
    print "Running as standalone server on port %d" %PORT
    print "Go to http://localhost:%d/" %PORT
    twisted.internet.reactor.run()

