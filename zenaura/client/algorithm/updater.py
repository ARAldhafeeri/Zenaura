from zenaura.client.hydrator import Hydrator
from .operations import *
from typing import List
from zenaura.client.tags.attribute import Attribute

class Updater(
    Hydrator
    ):

    async def update(self, patches : List, id : str) -> None:
        """
            1. receive patches with rich context information from searcher
            2. create new task as coroutines based on operation name and context
            2. enqueue tasks for the component in hyderator tasker \
            args :
                patches -> list of differences by zenaura diffing algorithm
                id -> component with state mutation.
        """
        while patches:
            prev_node_id, diffed_node, path, op = patches.pop(0)
            print("operation", op, prev_node_id)
            if op["name"] == ADD_NODE:
                async def task(dn=diffed_node, ci=id):
                    compiled_html = self.hyd_comp_compile_children(dn, ci, True)
                    parent_id = id + dn.path[0:-2] # last two digit in keyed uid is always level, index, so parent lives at the before
                    child_id = id + dn.path
                    self.hyd_rdom_append_child_after(parent_id, child_id, compiled_html)
                self.hyd_tsk_enqueue_task(id, task)
            
            if op["name"] == REMOVE_NODE:
                async def task(d=diffed_node, c=prev_node_id):
                    compiled_html = self.hyd_comp_compile_children(d, c, True)
                    # print("ADD_NODE compiled html", compiled_html)
                    self.hyd_rdom_remove_child(prev_node_id)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == NODE_INNER_TEXT:
                # avoid late binding 
                async def task(id=prev_node_id, c=op["context"]["text"]):       
                    self.hyd_rdom_replace_inner_text(id, c)
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == ADD_ATTRIBUTE:
                async def task(id=prev_node_id, op1=Attribute(op["context"]["attr_name"],op["context"]["attr_value"])):
                    self.hyd_rdom_set_attribute(prev_node_id, op1 )
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == REMOVE_ATTRIBUTE:
                async def task(id=prev_node_id, op1=op["context"]["attr_name"]):
                    self.hyd_rdom_remove_attribute(id, op1 )
                self.hyd_tsk_enqueue_task(id, task)

            if op["name"] == REPLACE_ATTRIBUTE:
                async def task(id=prev_node_id, op1=op["context"]["attr_name"]):
                    self.hyd_rdom_remove_attribute(prev_node_id, op1 )
                self.hyd_tsk_enqueue_task(id, task)


                
