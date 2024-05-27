import traceback
from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.hydrator import HydratorTasker
from .lifecycles.render import RenderLifeCycle
from zenaura.client.algorithm import DiffingAlgorithm
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
            await self.on_mutation(comp)
            comp_id = comp.id            
            prev_tree = self.zen_dom_table[comp_id]
            new_tree = comp.render()

            # create task queue for component
            task_que = self.hyd_tsk_get_or_create_task_queue(comp_id)

            # run diffing algorithm
            patches = self.search(prev_tree, new_tree, comp_id)
            await self.update(patches, comp_id)
            
            # schedule update with the browser
            while not task_que.empty():
                await asyncio.sleep(0.001)
                if self.hyd_rdom_is_complete():
                    task = self.hyd_tsk_dequeue_task(comp_id)
                    await task()

                
            self.hyd_vdom_update(comp)

            # update 3  : on_settled method to be called after updating
            await self.on_settled(comp)

        except Exception as e:
            self.componentDidCatchError(comp, traceback.format_exc())