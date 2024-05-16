from zenaura.client.tags import Node
from typing import List
from zenaura.client.hydrator.compiler_adapter import HydratorCompilerAdapter
from zenaura.client.tags import Data

class Searcher(
    HydratorCompilerAdapter
):
    """
        searching step of zenaura virtual dom algorithm.
    """
    def search(
        self, 
        prevNode : Node,
        newNode : Node,
        componentId : str
    ) -> List[List[any]]:
            """
                Compares the old and new component trees to identify the differences.

                Parameters:
                - prevNode: The previous component tree.
                - newNode: The new component tree.
                - componentId: The id of the component in virtual dom.

                Returns:
                    [[prevNode.nodeId, newNode, path]]
            """
            differences = []
            def helper(
                prevNode : Node, 
                newNode : Node,
                level : int,
                child_index : int,
                path : str = ""
            ) -> None:
                """
                    method perform dfs on the component tree
                    passing the current level to self.compare method
                    self.compare will mutate the diff stack
                    args:
                        prevNode: The previous component tree
                        newNode: The new component tree
                        level: The current level of the component tree
                        child_index: The index of the current child node in the component tree
                        path: unique path of the component tree to identify the nodes differences
                    return None
                """

                nonlocal differences

                if not isinstance(prevNode, Node) or not isinstance(newNode, Node):
                    return differences
                if prevNode is None or newNode is None:
                    differences.append((path, prevNode or newNode))  # Add the non-null node with its path
                    return differences
                
                if len(prevNode.children) and len(newNode.children) == 1:
                    if isinstance(prevNode.children[0], (Data, str)) and isinstance(newNode.children[0], (Data, str)):
                        differences.append([
                                self.hyd_comp_get_keyed_uuid(
                                    componentId=componentId, 
                                    level=level, 
                                    child_index=child_index, 
                                    path=path
                                ),
                                newNode,
                                path
                            ])
                    return differences

                # Attribute comparison
                for attr1 in prevNode.attributes:
                    attr2 = next((a for a in newNode.attributes if a.key == attr1.key), None)
                    if not attr2 or attr1.value != attr2.value:
                        differences.append((path, prevNode))
                        break
                
                # Update path for children

                # Children comparison (recursive)
                for idx, [child1, child2] in enumerate(zip(prevNode.children, newNode.children)):

                    path += f"{level}{idx}"
                    differences.extend(helper(child1, child2, level, child_index, path))
                    child_index += 1
                    level += 1
                return differences
                    
            # start comparison 
            helper(
                prevNode,
                newNode,
                0,
                0
            )
            return differences    