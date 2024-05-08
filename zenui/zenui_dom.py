from zenui.compiler import ZenuiCompiler
# compile zenui html dataclasses to html text

compiler = ZenuiCompiler()

class ZenUIDom:

    def __init__(self):
        self.curr_mounted_element = None


    def render(self, comp ):
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
            componentId=comp.componentId
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById(comp.id).innerHTML = compiled_comp
        self.dom_comp_update(comp)

    
    def mount(self, comp):
        comp_element_handler = comp.element 
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
            componentId=comp.componentId
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById("root").innerHTML = compiled_comp
        # update zenui dom lookup for re-rendering
        self.curr_mounted_element = comp

zenui_dom = ZenUIDom()



