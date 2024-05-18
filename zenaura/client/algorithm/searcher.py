from zenaura.client.tags import Node
from typing import List
from zenaura.client.hydrator.compiler_adapter import HydratorCompilerAdapter
from zenaura.client.tags import Data
from itertools import zip_longest
from .operations import *
class Searcher(
    HydratorCompilerAdapter
):
    """
        searching step of zenaura virtual dom algorithm.
    """
    def updater_context_builder(self, name: str, context: dict) -> dict:
        return {
            "name": name,
            "context": context
        }

    def search(self, prevNode: Node, newNode: Node, componentId: str) -> List[List[any]]:
        # error handling :
        if not prevNode and not newNode:
            return []
        if not isinstance(prevNode, Node) or not isinstance(newNode, Node):
            return []

        differences = []
        def helper(prev_child_node: Node, new_child_node: Node, componentId, path: str = "", level=0) -> None:
            nonlocal differences

            if not prev_child_node and new_child_node:  # Added
                differences.append([
                self.hyd_comp_get_keyed_uuid(
                            componentId=componentId, 
                            path=path
                    ),
                    new_child_node, 
                    path,
                    self.updater_context_builder(
                        name=ADD_NODE,
                        context={"children" : new_child_node}
                    )
                ])
                return

            if prev_child_node and not new_child_node:  # Removed
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        componentId=componentId, 
                        path=path
                    ),
                    new_child_node, 
                    path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children" : prev_child_node}
                    )
                ])
                return
            
            if prev_child_node.name != new_child_node.name:  # Changed child by name
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        componentId=componentId, 
                        path=path
                    ),
                    new_child_node, 
                    path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children" : new_child_node}
                    )
                ])
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        componentId=componentId, 
                        path=path
                    ),
                    new_child_node, 
                    path,
                    self.updater_context_builder(
                        name=ADD_NODE,
                        context={"children" : new_child_node}
                    )
                ])
                return

            # Compare attributes
            for [prev_attr, new_attr] in zip_longest(prev_child_node.attributes, new_child_node.attributes):
                
                # removed attribute
                if prev_attr and not new_attr:
                    differences.append([
                        self.hyd_comp_get_keyed_uuid(
                            componentId=componentId, 
                            path=path
                        ),
                        new_child_node, 
                        path,
                        self.updater_context_builder(
                            name=REMOVE_ATTRIBUTE,
                            context={"attr_name" : prev_attr.key}
                        )
                    ])
                    continue
                
                # added attribute
                if not prev_attr and new_attr:
                    differences.append([
                        self.hyd_comp_get_keyed_uuid(
                            componentId=componentId, 
                            path=path
                        ), 
                        new_child_node, 
                        path, 
                        self.updater_context_builder(
                            name=ADD_ATTRIBUTE,
                            context={"attr_name" : new_attr.key, "attr_value" : new_attr.value}
                        )
                    ])
                    continue

                # replaced value attr
                if prev_attr and new_attr:
                    if prev_attr.value != new_attr.value:
                        differences.append([
                           self.hyd_comp_get_keyed_uuid(
                                componentId=componentId, 
                                path=path
                            ),
                            new_child_node, 
                            path,
                            self.updater_context_builder(
                                name=ADD_ATTRIBUTE,
                                context={"attr_name" : new_attr.key, "attr_value" : new_attr.value}
                            )
                        ])



            # Compare children
            for idx, (prev_child, new_child) in enumerate(zip_longest(prev_child_node.children, new_child_node.children)):
                # leaf text nodes
                if not isinstance(prev_child, Node) or not isinstance(new_child, Node):
                    if prev_child != new_child:
                        differences.append([
                            self.hyd_comp_get_keyed_uuid(
                                componentId=componentId, 
                                path=path
                            ),
                            new_child_node,
                            path,
                            self.updater_context_builder(
                                name=NODE_INNER_TEXT,
                                context={"text" : new_child}
                            )
                        ])
                    continue 
                path += f"{level}{idx}"
                helper(prev_child, new_child, componentId, path, level)
                level += 1

        helper(prevNode, newNode, componentId,"", 0)
        return differences