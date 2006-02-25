sharetunes, the music player and server (through the web!)
webpage is now at http://sharetunes.berlios.de

REQUIREMENTS

Python 2.4 is required, and no other libraries.

Windows: download it from http://python.org
Mac 10.4's preinstalled python 2.3 seems to work.  
Linux has python preinstalled as well.

The client needs flash version 6-ish, and currently firefox is known to work.

STARTING

Windows: double click ShareTunesWindows.pyw for a systray icon

Mac, Linux, and for development, type:

   python start.py


TODO

 * flashplay.swf can make ff/ie shoot up in cpu and disk activity while
    downloading the song.  Seems not to be streaming... musicplayer.sf.net
    seems stream correctly, check that out
 * The flash<->js bridge GET's JavaScriptFlashGateway.swf for *each*
    actionscript proxy call!  At each button click!  Bad for responsiveness.
    The code is by macromedia devs, so presumably its hard to do it without
    GET's... maybe implement headers there, to force the browser to cache.
 * Experment with using a database in a javascript structure: nested arrays,
    hashes for some indexing...  current everything-in-dom-table feels hacky,
    if convenient.  how will performance compare?
 * Experiment with using sqlite as our native store -- currently the statically
    rendered table is effectively our on-disk store.  iTunes xml, of course,
    is too slow to parse to be the native store.  this will facilitate
        + lots of columns (attributes).. may overload the table approach?
        + Very necessary to go beyond current read-only-ness
 * js indexing: could do prefix/suffix trie's for faster incremental search
 * incremental search: space should indicate an OR query
 * Fix IE, test Safari
 * Better js visual/widgets library 
    + The big ones seem to now be: dojo, rico, zimbra's, scriptaculous
        http://wiki.osafoundation.org/bin/view/Projects/AjaxLibraries
        http://edevil.wordpress.com/2005/11/14/javascript-libraries-roundup/
        mochikit maybe should go
 * Visual-ish things that may or may not be solved by better widgets library
    + table column widths should not shrink and so forth
    + table sorts
 * Automatically discover location of itunes xml.  platform specific...
    Windows: probably use registry (need python win32 extensions) or something
    Mac: just look in the right place in the home folder?
 * Desktop GUI: taskbar icon, and little popup to control the server,
    display the url, do indexing, etc.  which framework?
    + WX theoretically does all 3 platforms, but ick
    + gtk can do win32 taskbar if gaim is any guide.  i don't like win32 gtk
        but it works, does 2 platforms, and straight win32 has bad reputation
    + if use gtk, then need a separate pure cocoa gui for mac
    + XUL: firefox plugin, pure js.  (Or python when they get that
        together) ... hmm... can't do taskbar, however.
    + as much in localhost-only, html/js as possible: like early google
        desktop, the taskbar just pops up a browser window.  platform specific
        code then hopefully limited.
 * Our own filesystem indexer if you dont have itunes (shocking indeed)
    use os.path.walk() and then need an id3 library
 * More P2P-ish stuff, like autodiscover over your subnet, rendezvous, yadda
    yadda... probably would need to bring twisted back in.  But can lose
    the twisted.web since web.py theoretically will run on twisted via wsgi.
 * Switching to java or .net is still feasible, the python layer is quite thin
 * localhost & port number for local server


LICENSE

Licensed under the Affero GPL version 1: http://www.affero.org/oagpl.html
Contains components under other licenses as well.
