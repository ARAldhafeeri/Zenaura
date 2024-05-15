
from zenaura.client.component import Component
from zenaura.client.tags import Node 
from zenaura.client.compiler import compiler
from pyscript import document 

class DefaultDomErrorComponent(Component):
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message
    def node(self):
        return Node("div", children=[Node("p", children=[str(self.error_message)])])


class GracefulDegenerationLifeCycleWrapper:
    
    def componentDidCatchError(self, comp, error) -> None:
        """
            Graceful degradation of component lifecycle methods.
        """
        if hasattr(comp, "componentDidCatchError"):
             # call componentDidCatchError method
             # mount the error message component 
             error_comp = comp.componentDidCatchError(str(error))
             compiled_comp = compiler.compile(
                 error_comp, 
                 componentId=comp.componentId,
                 zenaura_dom_mode=True
             )
             dom_node = document.getElementById("root")
             dom_node.innerHTML = compiled_comp
             self.zen_dom_table[comp.componentId] = error_comp
        else:
            # mount the default error message component 
            error_comp  = DefaultDomErrorComponent(error_message=str(error))
            error_comp = error_comp.node()
            compiled_comp = compiler.compile(
                 error_comp, 
                 componentId=comp.componentId,
                 zenaura_dom_mode=True
             )
            dom_node = document.getElementById("root")
            dom_node.innerHTML = compiled_comp
            self.zen_dom_table[comp.componentId] = error_comp
