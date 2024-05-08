from zenui.compiler import ZenuiCompiler
# compile zenui html dataclasses to html text
from pyscript import document 

compiler = ZenuiCompiler()

class ZenUIDom:

    def __init__(self):
        self.zen_dom_table = {}


    def render(self, comp ):
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById("root").innerHTML = compiled_comp

    def mount(self, comp ):
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById("root").innerHTML = compiled_comp

zenui_dom = ZenUIDom()


