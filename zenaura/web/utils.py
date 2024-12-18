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

global document
global window
global create_proxy 
global to_js

try:
    from pyscript import document as pyscript_doc, window as pyscript_window
    in_browser = True 
    document = pyscript_doc
    window = pyscript_window
except:
    from zenaura.mocks.browser_mocks import MockDocument, MockWindow
    document = MockDocument()
    window = MockWindow()
    in_browser = False
    

try : 
    from pyodide.ffi import create_proxy_pyodide, to_js_poyodide
    create_proxy = create_proxy_pyodide
    to_js = to_js_poyodide
    in_browser = True

except:
    # TODO: need to create mocks
    create_proxy = lambda x: x 
    to_js = lambda x: x 
    in_browser = False

