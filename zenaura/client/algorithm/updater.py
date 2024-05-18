from zenaura.client.hydrator import HydratorRealDomAdapter, HydratorTasker
from .operations import *
from typing import List

class Updater(HydratorRealDomAdapter, HydratorTasker):

    async def update(self, patches : List, componentId : str) -> None:
        """
            1. receive patches with rich context information from searcher
            2. create new task as coroutines based on operation name and context
            2. enqueue tasks for the component in hyderator tasker \
            args :
                patches -> list of differences by zenaura diffing algorithm
                componentId -> component with state mutation.
        """
        while patches:
            prev_node_id, diffed_node, path, op = patches.pop(0)

            if op["name"] == ADD_NODE:
                async def task(): 
                    self.hyd_rdom_append_child(prev_node_id, op["context"]["children"])
                self.hyd_tsk_enqueue_task(componentId, task)
            
            if op["name"] == REMOVE_NODE:
                async def task():
                    self.hyd_rdom_remove_child(prev_node_id)
                self.hyd_tsk_enqueue_task(componentId, task)

            if op["name"] == NODE_INNER_TEXT:
                async def task():
                    self.hyd_rdom_replace_inner_text(prev_node_id, op["context"]["text"])
                self.hyd_tsk_enqueue_task(componentId, task)

            if op["name"] == ADD_ATTRIBUTE:
                async def task():
                    self.hyd_rdom_set_attribute(prev_node_id, op["context"]["attr_name"], op["context"]["attr_value"])
                self.hyd_tsk_enqueue_task(componentId, task)

            if op["name"] == REMOVE_ATTRIBUTE:
                async def task():
                    self.hyd_rdom_remove_attribute(prev_node_id, op["context"]["attr_name"])
                self.hyd_tsk_enqueue_task(componentId, task)

            if op["name"] == REPLACE_ATTRIBUTE:
                async def task():
                    self.hyd_rdom_remove_attribute(prev_node_id, op["context"]["attr_name"])
                self.hyd_tsk_enqueue_task(componentId, task)


                
