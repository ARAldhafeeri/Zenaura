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
    def patches_builder(self, prev_child_node, new_child_node, id, child_id):
        return [
                self.hyd_comp_get_keyed_uuid(
                    id=id, 
                    child_id=child_id
                ),
                new_child_node, 
                child_id,
                self.updater_context_builder(
                    name=REMOVE_NODE,
                    context={"children" : prev_child_node}
                )
            ]
    def search(self, prevNode: Node, newNode: Node, id: str) -> List[List[any]]:
        # error handling :
        if not prevNode and not newNode:
            return []
        if not isinstance(prevNode, Node) or not isinstance(newNode, Node):
            return []

        differences = []
        def helper(prev_child_node: Node, new_child_node: Node, id, prev_child_path: str, new_child_path) -> None:
            nonlocal differences
            if not prev_child_node and new_child_node:  # Added
                differences.append([
                self.hyd_comp_get_keyed_uuid(
                            id=id, 
                            key=prev_child_path
                    ),
                    new_child_node, 
                    prev_child_path,
                    self.updater_context_builder(
                        name=ADD_NODE,
                        context={"children" : new_child_node}
                    )
                ])
                return

            if prev_child_node and not new_child_node:  # Removed
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id, 
                        key=prev_child_path
                    ),
                    prev_child_node, 
                    prev_child_path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children" : prev_child_node}
                    )
                ])
                return
            
            if prev_child_node.name != new_child_node.name:  # Changed child by name
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id, 
                        key=prev_child_path
                    ),
                    prev_child_node, 
                    prev_child_path,
                    self.updater_context_builder(
                        name=REMOVE_NODE,
                        context={"children" : prev_child_node}
                    )
                ])
                differences.append([
                    self.hyd_comp_get_keyed_uuid(
                        id=id, 
                        key=new_child_path
                    ),
                    new_child_node, 
                    new_child_path,
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
                            id=id, 
                            key=prev_child_path
                        ),
                        new_child_node, 
                        prev_child_path,
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
                            id=id, 
                            key=new_child_path
                        ), 
                        new_child_node, 
                        new_child_path, 
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
                                id=id, 
                                key=prev_child_path
                            ),
                            new_child_node, 
                            prev_child_path,
                            self.updater_context_builder(
                                name=ADD_ATTRIBUTE,
                                context={"attr_name" : new_attr.key, "attr_value" : new_attr.value}
                            )
                        ])



            # Compare children
            for idx, (prev_child, new_child) in enumerate(zip_longest(prev_child_node.children, new_child_node.children)):
                # leaf text nodes
                if prev_child and new_child:
                    if prev_child.is_text_node and new_child.is_text_node and (prev_child.text != new_child.text):
                        differences.append([
                            self.hyd_comp_get_keyed_uuid(
                                id=id, 
                                key=prev_child_path
                            ),
                            new_child_node,
                            prev_child_path,
                            self.updater_context_builder(
                                name=NODE_INNER_TEXT,
                                context={"text" : new_child.text}
                            )
                        ])
                        continue
                new_child_path = new_child.path if isinstance(new_child, Node) else ""
                prev_child_path = prev_child.path if isinstance(prev_child, Node) else ""
                helper(prev_child, new_child, id, prev_child_path=prev_child_path, new_child_path=new_child_path)

        helper(prevNode, newNode, id, 0, 0)
        return differences