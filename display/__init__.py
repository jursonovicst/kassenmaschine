from .basedisplay import BaseDisplay

import os
if os.uname()[4][:3] == 'arm':
    from .lcd2004 import LCD2004 as Display
else:
    from .console import Console as Display
