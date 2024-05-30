from zenaura.client.hydrator import Hydrator
from .operations import *
from typing import List
from zenaura.client.tags.attribute import Attribute

class Updater(
    Hydrator
    ):
    """
    This class is responsible for updating the real DOM based on the differences identified by the Searcher.

    It receives a list of patches from the Searcher and creates corresponding tasks for each patch. These tasks are then enqueued for execution by the Hydrator's tasker.

    Attributes:
        None
    """

    async def update(self, patches: List, id: str) -> None:
        """
        Updates the real DOM based on the provided patches.

        Args:
            patches: A list of patches containing the operation name, the new child node, the path of the child, and the context for the updater.
            id: The ID of the component to be updated.
        """

        while patches:
            prev_node_id, diffed_node, path, op = patches.pop(0)
            # print("operation", op, prev_node_id)

            if op["name"] == ADD_NODE:
                async def task(dn=diffed_node, ci=id):
                    """
                    Adds a new node to the real DOM.

                    Args:
                        dn: The new child node to be added.
                        ci: The ID of the component to which the node should be added.
                    """
                    compiled_html = self.hyd_comp_compile_children(dn, ci, True)
                    parent_id = id + dn.path[0:-2]  # last two digit in keyed uid is always level, index, so parent lives at the before
                    child_id = id + dn.path
                    self.hyd_rdom_append_child_after(parent_id, child_id, compiled_html)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == REMOVE_NODE:
                async def task(d=diffed_node, c=prev_node_id):
                    """
                    Removes a node from the real DOM.

                    Args:
                        d: The node to be removed.
                        c: The ID of the component containing the node.
                    """
                    compiled_html = self.hyd_comp_compile_children(d, c, True)
                    # print("ADD_NODE compiled html", compiled_html)
                    self.hyd_rdom_remove_child(prev_node_id)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == NODE_INNER_TEXT:
                # avoid late binding
                async def task(id=prev_node_id, c=op["context"]["text"]):
                    """
                    Updates the inner text of a node in the real DOM.

                    Args:
                        id: The ID of the node to be updated.
                        c: The new inner text.
                    """
                    self.hyd_rdom_replace_inner_text(id, c)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == ADD_ATTRIBUTE:
                async def task(id=prev_node_id, op1=Attribute(op["context"]["attr_name"], op["context"]["attr_value"])):
                    """
                    Adds an attribute to a node in the real DOM.

                    Args:
                        id: The ID of the node to be updated.
                        op1: The attribute to be added.
                    """
                    self.hyd_rdom_set_attribute(id, op1)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == REMOVE_ATTRIBUTE:
                async def task(id=prev_node_id, op1=op["context"]["attr_name"]):
                    """
                    Removes an attribute from a node in the real DOM.

                    Args:
                        id: The ID of the node to be updated.
                        op1: The name of the attribute to be removed.
                    """
                    self.hyd_rdom_remove_attribute(id, op1)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == REPLACE_ATTRIBUTE:
                async def task(id=prev_node_id, op1=op["context"]["attr_name"]):
                    """
                    Replaces an attribute on a node in the real DOM.

                    Args:
                        id: The ID of the node to be updated.
                        op1: The name of the attribute to be replaced.
                    """
                    self.hyd_rdom_remove_attribute(id, op1)
                self.hyd_tsk_enqueue_task(id, task)
