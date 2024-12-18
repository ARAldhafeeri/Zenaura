import traceback
from zenaura.client.dom.error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.hydrator import HydratorTasker
from .lifecycles.render import RenderLifeCycle
from zenaura.client.algorithm import DiffingAlgorithm

class Render(
    GracefulDegenerationLifeCycleWrapper,
    RenderLifeCycle, 
    DiffingAlgorithm,
    HydratorTasker
):
    """
    Renders components by updating the DOM based on the differences between the previous and new component trees.

    This class provides methods for:

    - **Lifecycle:** Calling lifecycle methods for components during rendering.
    - **Diffing:** Calculating the differences between the previous and new component trees.
    - **Updating:** Applying the calculated differences to the DOM.
    - **Scheduling:** Scheduling updates with the browser.
    - **Virtual DOM Update:** Updating the virtual DOM with the new component tree.
    - **Error Handling:** Handling errors gracefully and displaying an error message component.

    **Attributes:**

    - `zen_dom_table`: A dictionary that stores the virtual DOM for each component.
    - `hyd_tsk_task_queues`: A dictionary that stores task queues for each component.

    **Methods:**

    - `render(comp)`: Renders the given component by updating the DOM.
    - `on_mutation(comp)`: Calls the `on_mutation` lifecycle method for the component.
    - `on_settled(comp)`: Calls the `on_settled` lifecycle method for the component.
    - `search(prev_tree, new_tree, comp_id)`: Calculates the differences between the previous and new component trees.
    - `update(patches, comp_id)`: Applies the calculated differences to the DOM.
    - `hyd_vdom_update(comp)`: Updates the virtual DOM with the new component tree.
    - `on_error(comp, error)`: Handles errors gracefully and displays an error message component.
    """
    async def render(self, comp ) -> None:
        """
        Renders the component by updating the DOM based on the differences between the previous and new component trees.

        This method performs the following steps:

        1. **Lifecycle:** Calls the `on_mutation` lifecycle method for the component.
        2. **Diffing:** Calculates the differences between the previous and new component trees using the `search` method.
        3. **Update:** Applies the calculated differences to the DOM using the `update` method.
        4. **Scheduling:** Schedules the updates with the browser using the `hyd_rdom_is_complete` and `hyd_tsk_dequeue_task` methods.
        5. **Virtual DOM Update:** Updates the virtual DOM with the new component tree using the `hyd_vdom_update` method.
        6. **Lifecycle:** Calls the `on_settled` lifecycle method for the component.

        **Error Handling:**

        - If an error occurs during rendering, the `on_error` method is called with the error message.
        - This method allows components to handle errors gracefully by returning a new component to display in place of the original component.
        - If the component does not have a `on_error` method, a default error message component is displayed.

        **Parameters:**

        - `comp`: An instance of the `Component` class.

        **Returns:**

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
                task = self.hyd_tsk_dequeue_task(comp_id)
                await task()

                
            self.hyd_vdom_update(comp)

            # update 3  : on_settled method to be called after updating
            await self.on_settled(comp)

        except Exception as e:
            self.on_error(comp, traceback.format_exc())