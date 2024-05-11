from zenaura.client.compiler import ZenuiCompiler
from zenaura.client.tags import Node
from collections import defaultdict
from pyscript import document 

compiler = ZenuiCompiler()

class Dom:

    def __init__(self):
        self.zen_dom_table = defaultdict(str)


    def render(self, comp ) -> None:
        """
            Renders the component by updating the DOM based on the differences between the previous and new component trees.

            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        prevTree = self.zen_dom_table[comp.componentId]
        newTree = comp.node()
        diff = self.search(prevTree, newTree)

        while diff:
            prevNodeId, newNodeChildren = diff.pop()
            compiled_comp = compiler.compile(
                newNodeChildren, 
                componentName=comp.__class__.__name__,
                zenaura_dom_mode=True
            )

            document.querySelector(f'[data-zenui-id="{prevNodeId}"]').innerHTML  = compiled_comp
            self.update(prevTree, prevNodeId, newNodeChildren)
        self.zen_dom_table[comp.componentId] = prevTree       

    def mount(self, comp  ) -> None:
        """
            Mounts the component by creating the node tree, compiling HTML, and attaching the container to the root node.

            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        comp_tree = comp.node()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__,
            zenaura_dom_mode=True
        )
        dom_node = document.getNodeById("root") 
        dom_node.innerHTML = compiled_comp
        self.zen_dom_table[comp.componentId] = comp_tree

    def search(self, prevComponentTree : Node, newComponentTree : Node) -> Node:
        """
            Compares the old and new component trees to identify the differences.

            Parameters:
            - prevComponentTree: The previous component tree.
            - newComponentTree: The new component tree.

            Returns:
            A stack of all different nodes in the format: [[prevNode.nodeId, newNode]]
        """
        diff = []
        def helper(prevTreeNode : Node, newTreeNode : Node):
            if not isinstance(prevTreeNode, Node):
                return
            nonlocal diff
            # base case prevTreeNode newTreeNode is none
            if (not prevTreeNode) or (not newTreeNode):
                return
            #  base case: not node instance
            if (not isinstance(prevTreeNode, Node )) or (not isinstance(newTreeNode, Node )):
                return 
            # base case find deepest level of change for effecient dom updates
            # if only text changed ignore
            if (prevTreeNode.children != newTreeNode.children) :
                diff.append([prevTreeNode.nodeId, newTreeNode])

            for i in range(min(len(prevTreeNode.children), len(newTreeNode.children))):
                helper(prevTreeNode.children[i], newTreeNode.children[i])
            
        helper(prevComponentTree, newComponentTree)
        return diff

    def update(self, prevTree, prevNodeId, newNodeChildren):
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

zenaura_dom = Dom()


