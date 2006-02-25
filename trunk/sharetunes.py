#!python
"""
sharetunes, the music player and server (through the web!)

see README.txt and http://sharetunes.berlios.de for more info

there are some commandline options, look at the bottom.  
'nost' is helpful for development
"""
__license__ = "Affero GPL version 1: http://www.affero.org/oagpl.html"


import xml.sax
import sys, os, socket, cgi, copy, urllib
import webbrowser, threading

import PListReader
import web  # comments poor, but docs good at http://webpy.org
import simplejson

WIN32 = sys.platform == 'win32'
MAC = 'darwin' in sys.platform
LINUX = sys.platform == 'linux' #@@ untested

if WIN32:
    from SysTrayIcon import SysTrayIcon



#fill this in if automatic detection doesn't work

ITUNES_FILE = ''



#ITUNES_FILE = r'C:\Documents and Settings\Administrator\My Documents\My Music\iTunes\iTunes Music Library.xml'


def reprload(filename):
    text = safereadfile(filename)
    if not text: return None
    return eval(text)

def reprsave(filename, obj):
    fp = open(filename, 'wb')
    fp.write(repr(obj))
    fp.close()

def loadConfig():
    global config
    config = reprload('config')
    if not config: config = makeDefaultConfig()
    print config

def saveConfig():
    global config
    reprsave('config', config)

def makeDefaultConfig():
    #note: keep keys as python/js legal names.. _ not -
    return {
        'iTunesFile': getITunesXMLFile(),
        'allowRemoteHosts': True
    }   


######################## Utilities


def urlunescape(urltext):
    """ Unescape a URL text part containing %xx-character encodings
        adapted from mxURL
        @@ replace with url.unquote() it looks like
    """
    hl = urltext.split('%') ##charsplit(urltext,'%')
    if len(hl) > 1:
        rest = hl[1:]
        for i,text in enumerate(rest):
            rest[i] = chr(int(text[:2], 16)) + text[2:]
        return hl[0] + ''.join(rest)
    return urltext
## print urlunescape("hello%27world")

def urlToFile(url):
    if url.startswith('file://localhost/'):
        rest = url[ len('file://localhost/'): ]
    elif url.startswith('file://'):
        rest = url[ len('file://'): ]
    else: raise Exception, "cant handle url: %s" %url

    #have to do things for windows pipe-colon "C|\blabla" ?
    #  but that form doesnt seem to be used in itunes' xml 
    #and, just keep forward slashes, python i/o on win can handle
    return urlunescape(rest)

## print urlToFile("file:///var/svn")
## print urlToFile("file://localhost/C:/media/itunes-music/")
##@@ need to test url's out of mac itunes


def filesuffix(filename):
    return filename[filename.rfind('.')+1 : ]

## print filesuffix("asdf.gif")

def safereadfile(filename):
    try: return open(filename, 'rb').read()
    except IOError: return ''

## print safereadfile("ooga booga.txt")
## print safereadfile("main.py")[:50]

def getSelfHostname():
    return socket.gethostbyaddr(socket.gethostname())[0]

#######################################################

def processITunes():
    iTunesFile = config['iTunesFile']

    reader = PListReader.PListReader()
    try:
        xml.sax.parse(iTunesFile, reader)
    except IOError:
        print "Couldn't read file: %s" %iTunesFile
    result = reader.getResult()

    musicfolderurl = result['Music Folder']
    musicpath = urlToFile(musicfolderurl)
    open('musicpath','w').write(musicpath)

    tracks = result['Tracks'].values()
    # what formats does flash support?  maybe just mp3?
    tracks = [t for t in tracks 
        if filesuffix(t.get('Location','')).lower()[:-1] != 'm4a']

    OUT = open('tracks_table', 'w')

    def mycmp(t1, t2):
        def artist_get(track):
            a = track.get('Artist')
            if not a or a.isspace():
                a = 'ZZZZZZZZZZZZ'
            return a
        artist_cmp = cmp(artist_get(t1), artist_get(t2))
        if artist_cmp != 0:  return artist_cmp
        album_cmp = cmp(t1.get('Album'), t2.get('Album'))
        if album_cmp != 0:  return album_cmp
        #@@ should sort by track here.  this is tedious.  reason to switch
        #   to sqlite, or even in-memory sqlite just for sorting!
        name_cmp = cmp(t1.get('Name'), t2.get('Name'))
        if name_cmp != 0:  return name_cmp
        return 0

    tracks.sort(mycmp)

    for track in tracks:
        location = track['Location']
        if track['Location'].startswith(musicfolderurl):
            # chop down to absolute URL within musicfolderurl
            location = "/musicroot/" + location[len(musicfolderurl):]
        elif track['Location'].startswith('file://'):
            print "SKIPPING file not in the iTunes 'Music Folder'",
            print "%s  :  %s" % (musicfolderurl, location)
            continue
        if location.endswith('/'):
            location = location[:-1]

        print>>OUT, """<tr musicurl="%s" onclick="play(this)">""" % location

        linktext = '<a href="%s" class=downloadLink>[link]</a>' %location

        line = u'<td>%s' %linktext
        line += u"<td>%s <td>%s <td>%s" %tuple([cgi.escape(track.get(key,'')) or '&nbsp;' 
                for key in ('Name','Artist', 'Album')])
        print>>OUT, line.encode('utf-8')


#####################################################

urls = (
    '/',  'viewinterface',
    '/(musicroot|player)(.*)$',  'viewstatic',
    '/jcall/getConfig', 'jcall_getConfig',
    '/jcall/saveConfig', 'jcall_saveConfig',
    '/jcall/restoreDefaults', 'jcall_restoreDefaults',
    '/jcall/processITunes', 'jcall_processITunes',
)

class jcall_getConfig:
    def GET(self):
        web.output(simplejson.dumps(config))

class jcall_saveConfig:
    def GET(self):
        json = urllib.unquote(web.context.environ['QUERY_STRING'])
        newConfig = simplejson.loads(json)
        web.debug("new config IS ", newConfig)
        messages = validateConfig(newConfig)
        if messages:
            ret = {'success':False, 'messages':messages}
            web.output(simplejson.dumps(ret))
            return

        global config
        config = newConfig
        saveConfig()
        web.output(simplejson.dumps({'success':True}))

class jcall_restoreDefaults:
    def GET(self):
        global config
        config = makeDefaultConfig()
        web.debug(config)
        saveConfig()
        web.output(simplejson.dumps(config))

def validateConfig(newConfig):
    messages = {}
    s = web.storify(newConfig, *config.keys())
    try:
        fp = open(s.iTunesFile, 'rb')
        fp.close()
    except IOError:
        messages['iTunesFile'] = "Not a valid iTunes file."
    return messages

class jcall_processITunes:
    def GET(self):
        processITunes()
        web.debug("DONE processing itunes")

class viewinterface:
    def GET(self):
        template = open('template.html', 'rb').read()
        part1, part2 = template.split("%TRACKS_TABLE%")

        web.output(part1)
        web.output(safereadfile('tracks_table') or 
                """<tbody><tr><td colspan=3 style="padding:10px;">Need to index files...""")
        web.output(part2)



class viewstatic:
    def GET(self, urlroot, urlpath):
        fileroots = {
            'musicroot': safereadfile('musicpath'),
            'player': '.'
        }
        if not urlpath: return web.redirect(urlroot+'/')
        urlpath = urlpath[1:]

        rootpath = fileroots[urlroot]
        filepath = urlunescape(urlpath)
        if '../' in filepath or '/..' in filepath:
            return web.notfound() #security!
        fullpath = os.path.join(rootpath, urlpath)
        return servestatic(fullpath)


MIMETYPES = {
    'mp3': 'audio/x-mp3',
    'css': 'text/css',
    'html': 'text/html',
    'js': 'text/javascript',
    'swf': 'application/x-shockwave-flash',
}
#@@ how do you determine a good value for this?
BLOCKSIZE = 100 * 1000

def servestatic(fullpath):
    if os.path.isdir(fullpath):
        filenames = os.listdir(fullpath)
        filenames.sort()
        filenames.insert(0, '..')
        for filename in filenames:
            dispname = filename
            if os.path.isdir(os.path.join(fullpath, filename)): 
                dispname = dispname + '/'
            print '<a href="%s">%s</a> <BR>' %(dispname, cgi.escape(dispname))
        return

    try:
        fp = None
        fp = open(fullpath, 'rb')
        mimetype = MIMETYPES.get(filesuffix(fullpath).lower(), 'text/plain')
        web.header('Content-Type', mimetype)

        def streamGen():
            while True:
                block = fp.read(BLOCKSIZE)
                if not block: break
                yield block
            fp.close()
        web.context.output = streamGen()
        
    except IOError:
        if fp: fp.close()
        raise
        #web.notfound()



def startServer():
    web.internalerror = web.debugerror
    if USE_SYSTRAY and WIN32:
        print "Quit via systray icon"
    elif not USE_SYSTRAY and WIN32:
        print "Control-C then page reload to quit"
    else: print "Control-C to quit"
    web.run(urls, web.reloader)

def spawnServer():
    class ServerThread(threading.Thread):
        def run(self):
            startServer()
    st = ServerThread()
    st.setDaemon(True)
    st.start()

def openBrowser(sysTrayIcon): 
    webbrowser.open("http://%s:8080" % getSelfHostname())

def doSysTray():
    if WIN32: doWinSysTray()
    elif MAC: raise Exception, "Desktop GUI unimplemented for mac"
    elif LINUX: raise Exception, "Desktop GUI unimplemented for linux"

def doWinSysTray():
    #icon looks ugly here?
    menu_options = (('Open ShareTunes', None, openBrowser),
##                     ('Process iTunes', None, lambda sti: processITunes()),
                    )
    SysTrayIcon('notes.ico', 'ShareTunes', menu_options)

def getMyDocuments():
    # http://www.blueskyonmars.com/2005/08/05/finding-a-users-my-documents-folder-on-windows/
    from win32com.shell import shell
    df = shell.SHGetDesktopFolder()
    pidl = df.ParseDisplayName(0, None,
        "::{450d8fba-ad25-11d0-98a8-0800361b1103}")[1]
    return shell.SHGetPathFromIDList(pidl)

## def getMyMusic():
##     from win32com import shell, shellcon
##     return shell.SHGetFolderPath(0, shellcon.CSIDL_MYMUSIC, 0, 0)
## 
## print getMyMusic()


def getITunesXMLFile():
    # this is where it is on my system at least...
    if WIN32:
        return os.path.join(getMyDocuments(), 'My Music', 
            'iTunes', 'iTunes Music Library.xml')
    elif MAC:
        #@@ partially tested!  from http://www.indyjt.com/blog/?p=51
        #   this isn't the correct way to get it (e.g. i18n)
        return os.path.join(os.environ['HOME'], 
                "Music/iTunes/iTunes Music Library.xml")


USE_SYSTRAY = WIN32 and 'nost' not in sys.argv

loadConfig()

def main():
    #dont do state settings in main() because its not run on autoreload
    print "CONFIG AT LOAD: ",config

    if 'make' in sys.argv:
        processITunes()
    elif USE_SYSTRAY:
        spawnServer()
        doSysTray()
    else: 
        startServer()


if __name__ == '__main__':
    print "Start via start.py"
    # running from in here screws up autoreloader
    #  you get two modules, 'sharetunes' and '__main__' with diff. globals
