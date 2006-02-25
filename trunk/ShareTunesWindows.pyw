"""
With python installed, double clicking on this (or a shortcut to it) 
will launch ShareTunes.
"""
import sys,os
os.chdir( os.path.dirname(sys.argv[0]) )
execfile("start.py")
