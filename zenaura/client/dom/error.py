
from zenaura.client.component import Component, Reuseable
from zenaura.client.tags import Node 
from zenaura.client.compiler import compiler
from zenaura.client.hydrator import Hydrator

@Reuseable
class DefaultDomErrorComponent(Component):
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message
    def render(self):
        return Node("div", children=[Node(text=str(self.error_message))])


class GracefulDegenerationLifeCycleWrapper(
    Hydrator
):
    
    def componentDidCatchError(self, comp, error) -> None:
        """
            Graceful degradation of component lifecycle methods.
        """
        # cleanup
        self.zen_dom_table.clear()

        if hasattr(comp, "componentDidCatchError"):
            # call componentDidCatchError method
            # mount the error message component 
            error_comp = comp.componentDidCatchError(str(error))
            compiled_comp =  self.hyd_comp_compile_render(
                 error_comp
            )
            
            # attach to real dom
            self.hyd_rdom_attach_to_root(compiled_comp)

            # update virtual dom
            self.hyd_vdom_update_with_new_render(comp, error_comp.render())

        else:
            # mount the default error message component
            error_comp  = DefaultDomErrorComponent(error_message=str(error))
            
            #compile the comp
            compiled_comp =  self.hyd_comp_compile_render(
                 error_comp
             )
            
            # attach to real dom
            self.hyd_rdom_attach_to_root(compiled_comp)

            # update virtual dom
            self.hyd_vdom_update_with_new_render(comp, error_comp.render())
