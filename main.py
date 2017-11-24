print "importing modules"
try:
    from init import *
    print "Modules Imported Successfully."
    cls()
    Current =  startscreen()
except ImportError:
    print "Import error! Is init file in same folder/referenced by main file?"
