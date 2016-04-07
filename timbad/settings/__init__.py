from .base import *

try:
    from .local import *
    live = False

except:
    live = True
    print "LIVE"

if live:
    from .production import *
