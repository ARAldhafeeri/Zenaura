import traceback
from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.hydrator import HydratorTasker
from .lifecycles.render import RenderLifeCycle
from zenaura.client.algorithm import DiffingAlgorithm
from pyscript import document
import asyncio


class Render(
    GracefulDegenerationLifeCycleWrapper,
    RenderLifeCycle, 
    DiffingAlgorithm,
    HydratorTasker
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

            # update steps 1-3: on_mutation -> update -> on_settled
            # update 1: lifecycle method to be called before updating
            self.on_mutation(comp)
            comp_id = comp.componentId
            task_queue = self.hyd_tsk_get_or_create_task_queue(comp_id)
            
            prev_tree = self.zen_dom_table[prev_tree]
            new_tree = comp.node()

            patches = self.search(prev_tree, new_tree, comp_id)

            self.update(patches)

            while not task_queue.empty():
                await asyncio.sleep(0.01) # at rate of 60 update per second
                if self.hyd_rdom_is_interactive():
                    task = await self.hyd_tsk_dequeue_task(comp_id)
                    await task()
                    
            # without tasker working code
            # # update 2: update the component in the DOM
            # prevTree = self.zen_dom_table[comp.componentId]
            # print("changed", comp.componentId)
            # print(prevTree)
            # newTree = comp.node()

            # diff = self.search(prevTree, newTree, comp.componentId)
            
            # print(len(diff))
            # async def apply_diff_chunk(chunk_size=5):
            #     for _ in range(chunk_size):
            #         if not diff:
            #             break
            #         prevNodeId, newNodeChildren, path = diff.pop()
            #         compiled_html = self.hyd_comp_compile_children(newNodeChildren, comp.componentId, True)
            #         self.hyd_rdom_attach_to_mounted_comp(prevNodeId, compiled_html)

            # while diff:
            #     await apply_diff_chunk()
                
            self.hyd_vdom_update(comp)

            # update 3  : on_settled method to be called after updating
            self.on_settled(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())