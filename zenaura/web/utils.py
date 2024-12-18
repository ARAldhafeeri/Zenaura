"""
Pyodide and pyscript is intended to work in the browser. 
This file have conditional imports so it works magically
on server and client.

On the server pyodide, pyscript will be missing.

Users of zenaura don't need to know about this,

they just import from this file 
e.g. 
from zenaura.web.utils import document 

This is used across the source code as well.

"""
in_browser = False

try:
    from pyscript import document, window
    in_browser = True 
except:
    from zenaura.mocks.browser_mocks import MockDocument, MockWindow
    document = MockDocument()
    window = MockWindow()
    in_browser = False
    

try : 
    from pyodide.ffi import create_proxy, to_js
    in_browser = True

except:
    # TODO: need to create mocks
    create_proxy = lambda x: x 
    to_js = lambda x: x 
    in_browser = False

