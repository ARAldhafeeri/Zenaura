import traceback
from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.compiler import compiler
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from zenaura.client.hyderator import Hyderator
from .lifecycles.render import RenderLifeCycle
from zenaura.client.algorithm import DiffingAlgorithm
from pyscript import document 


class Render(
    GracefulDegenerationLifeCycleWrapper,
    Hyderator,
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
            diff = self.search(prevTree, newTree, comp.componentId)
            print(len(diff))
            while diff:
                prevNodeId, newNodeChildren, path= diff.pop()
                compiled_comp = compiler.compile(
                    newNodeChildren, 
                    componentId=comp.componentId,
                    zenaura_dom_mode=True,
                    path = path
                )
                print(prevNodeId)
                print(compiled_comp)

                foundNode = document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{prevNodeId}"]')
                if foundNode:
                    foundNode.outerHTML = compiled_comp
            # self.update(prevTree, prevNodeId, newNodeChildren)
            self.zen_dom_table[comp.componentId] = newTree

            # update 3  : componentDidUpdate method to be called after updating
            self.componentDidUpdate(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())