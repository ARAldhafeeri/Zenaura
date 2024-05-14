from zenaura.client.tags import Node, Data
from typing import List

class Updater:
    """
        update step in zenaura virtual dom algorithm
    """
    def update(
        self, 
        prevTree : Node, 
        prevNodeId : str, 
        newNodeChildren: List[Node],
    ) -> Node:
        """
            Updates the previous zenui dom tree by replacing the changed node children with the new node children.

            Parameters:
            - prevTree: The previous zenui dom tree.
            - prevNodeId: The id of the node to be updated.
            - newNodeChildren: The new node children to replace the old ones.

            Returns:
            The previous tree after the update.
        """
        stack = [prevTree]
        while stack:
            curr = stack.pop()
            if isinstance(curr, Node):
                if curr.nodeId == prevNodeId:
                    curr.children = newNodeChildren.children
                for i in curr.children:
                    stack.append(i)
        return prevTree