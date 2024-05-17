from zenaura.client.tags import Node
from typing import List
from zenaura.client.hydrator.compiler_adapter import HydratorCompilerAdapter
from zenaura.client.tags import Data
from itertools import zip_longest
class Searcher(
    HydratorCompilerAdapter
):
    """
        searching step of zenaura virtual dom algorithm.
    """
    def search(self, prevNode: Node, newNode: Node, componentId: str) -> List[List[any]]:
        differences = []
        tracked = set()  # Track added/removed nodes

        def helper(prev_child_node: Node, new_child_node: Node, path: str = "") -> None:
            nonlocal differences, tracked

            if not prev_child_node and new_child_node:  # Added
                differences.append([None, new_child_node, path])
                return

            if prev_child_node and not new_child_node:  # Removed
                differences.append([prev_child_node.nodeId, new_child_node, path])
                return
            
            # Start tracking after checks for addition/removal are done.
            if isinstance(new_child_node, Node):
                if new_child_node.nodeId:
                    tracked.add(new_child_node.nodeId)

            if isinstance(prev_child_node, Node):
                if prev_child_node.nodeId in tracked:
                    tracked.remove(prev_child_node.nodeId)

            # Compare attributes
            for [prev_attr, new_attr] in zip_longest(prev_child_node.attributes, new_child_node.attributes):
                
                # removed attribute
                if prev_attr and not new_attr:
                    differences.append([prev_child_node.nodeId, new_child_node, path])
                    continue
                
                # added attribute
                if not prev_attr and new_attr:
                    differences.append([None, new_child_node, path])
                    continue

                # replaced value attr
                if prev_attr and new_attr:
                    if prev_attr.value != new_attr.value:
                        differences.append([prev_child_node.nodeId, new_child_node, path])



            # Compare children
            for idx, (prev_child, new_child) in enumerate(zip_longest(prev_child_node.children, new_child_node.children)):
                if not isinstance(prev_child, Node) or not isinstance(new_child, Node):
                    if prev_child != new_child:
                        differences.append([prev_child_node.nodeId, new_child_node, path])
                    continue 
                path += f"{path}{idx}"
                helper(prev_child, new_child, path)

        helper(prevNode, newNode)
        return differences