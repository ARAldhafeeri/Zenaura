from zenaura.client.tags import Node
from typing import List

class Searcher:
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
            diff = []
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

                nonlocal diff

                # base cases :
                if ( not prevNode) or (not newNode):
                    return
                
                # ignore Data, str because they are handled by parent  recursion call 
                if (not isinstance(prevNode, Node)) or (not isinstance(newNode, Node)):
                    return 
                
                if (not prevNode.children) or (not newNode.children):
                    return
                
                
                # compare and update diff stack
                # check if parent node attributes changed
                self.compare(
                    prevNode,
                    newNode, 
                    level, 
                    child_index,
                    componentId,
                    diff,
                    path
                    )

                        
                # recursivly call search on children nodes 
                for idx, [prevNodeChild, newNodeChild] in enumerate(zip(prevNode.children, newNode.children)):
                    # search and diff each child node
                    path += f"{level}{idx}"
                    helper(
                        prevNodeChild, 
                        newNodeChild, 
                        level, 
                        child_index,
                        path
                    )
                    child_index += 1
                    level += 1
                    
            # start comparison 
            helper(
                prevNode,
                newNode,
                0,
                0
            )
            return diff    