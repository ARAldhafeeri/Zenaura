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
            recieve instance of Component child, rerender it.
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
            comp : recieve instance of Component 
            1. create node tree
            2. compiles html
            3. attach container to root node 
            4. used in zenui simple router to mount nodes
            5. create blueprint for diffing algorithm in re-render mode.
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
            receive old, new component tree
            compare the old to new.
            return a stack of all diff nodes
            in the following format
           [ [prevNode.nodeId, newNode] ]
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

            helper(prevTreeNode.children, newTreeNode.children)
            
        helper(prevComponentTree, newComponentTree)
        return diff

    def update(self, prevTree, prevNodeId, newNodeChildren):
        """
            recieve previous zenui dom tree
            update the previous tree changed node children
            with the new node children
            return the previous tree
            this opration is done after successfully updating the real dom
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


