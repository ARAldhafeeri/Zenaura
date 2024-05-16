import traceback
from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.compiler import compiler
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from zenaura.client.hydrator import Hydrator
from .lifecycles.render import RenderLifeCycle
from zenaura.client.algorithm import DiffingAlgorithm
from pyscript import document 


class Render(
    GracefulDegenerationLifeCycleWrapper,
    Hydrator,
    RenderLifeCycle, 
    DiffingAlgorithm
    ):
    async def render(self, comp ) -> None:
        """
            Renders the component by updating the DOM based on the differences between the previous and new component trees.

            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        try:

            # update steps 1-3: componentWillUpdate -> update -> componentDidUpdate
            # update 1: lifecycle method to be called before updating
            self.componentWillUpdate(comp)
            
            # update 2: update the component in the DOM
            prevTree = self.zen_dom_table[comp.componentId]
            newTree = comp.node()

            diff = self.search(prevTree, newTree, comp.componentId)
            
            async def apply_diff_chunk(chunk_size=50):
                for _ in range(chunk_size):
                    if not diff:
                        break
                    prevNodeId, newNodeChildren, path = diff.pop()
                    compiled_html = self.hyd_comp_compile_children(newNodeChildren, comp.componentId, True, path)
                    self.hyd_rdom_attach_to_mounted_comp(prevNodeId, compiled_html)

            while diff:
                await apply_diff_chunk()    
            self.hyd_vdom_update_with_new_node(comp, newTree)

            # update 3  : componentDidUpdate method to be called after updating
            self.componentDidUpdate(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())