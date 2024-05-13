from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.compiler import compiler
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from .lookup import LookupTable
from .lifecycles.render import RenderLifeCycle
from .algorithm import DiffingAlgorithm
import traceback
from pyscript import document 


class Render(
    GracefulDegenerationLifeCycleWrapper,
    LookupTable,
    RenderLifeCycle, 
    DiffingAlgorithm
    ):
    def render(self, comp ) -> None:
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
            diff = self.search(prevTree, newTree)
            while diff:
                prevNodeId, newNodeChildren = diff.pop()
                compiled_comp = compiler.compile(
                    newNodeChildren, 
                    componentName=comp.__class__.__name__,
                    zenaura_dom_mode=True
                )

                foundNode = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{prevNodeId}"]')
                foundNode.outerHTML = compiled_comp
                self.update(prevTree, prevNodeId, newNodeChildren)
            self.zen_dom_table[comp.componentId] = newTree

            # update 3  : componentDidUpdate method to be called after updating
            self.componentDidUpdate(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())