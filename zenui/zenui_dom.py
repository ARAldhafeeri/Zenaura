from zenui.compiler import ZenuiCompiler
# compile zenui html dataclasses to html text
from pyscript import document 
from zenui.tags import Element
from collections import defaultdict

compiler = ZenuiCompiler()

class ZenUIDom:

    def __init__(self):
        self.zen_dom_table = defaultdict(str)


    def render(self, comp ) -> None:
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        prevTree = self.zen_dom_table[comp.componentId]
        newTree = comp.element()
        diff = self.search(prevTree, newTree)

        while diff:
            prevNodeId, newNodeChildren = diff.pop()
            compiled_comp = compiler.compile(
                newNodeChildren, 
                componentName=comp.__class__.__name__,
                zenui_dom_mode=True
            )

            document.querySelector(f'[data-zenui-id="{prevNodeId}"]').innerHTML  = compiled_comp
        self.zen_dom_table[comp.componentId] = prevTree       

    def mount(self, comp  ) -> None:
        """
            comp : recieve instance of ZenUIComponent 
            1. create element tree
            2. compiles html
            3. attach container to root node 
            4. used in zenui simple router to mount elements
            5. create blueprint for diffing algorithm in re-render mode.
        """
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__,
            zenui_dom_mode=True
        )
        dom_element = document.getElementById("root") 
        dom_element.innerHTML = compiled_comp
        self.zen_dom_table[comp.componentId] = comp_tree

    def search(self, prevComponentTree : Element, newComponentTree : Element) -> Element:
        """
            receive old, new component tree
            compare the old to new.
            return a stack of all diff nodes
            in the following format
           [ [prevNode.elementId, newNode] ]
        """
        diff = []
        def helper(prevTreeNode : Element, newTreeNode : Element):
            if not isinstance(prevTreeNode, Element):
                return
            nonlocal diff
            # base case prevTreeNode newTreeNode is none
            if (not prevTreeNode) or (not newTreeNode):
                return
            #  base case: not element instance
            if (not isinstance(prevTreeNode, Element )) or (not isinstance(newTreeNode, Element )):
                return 
            # base case find deepest level of change for effecient dom updates
            # if only text changed ignore
            if (prevTreeNode.children != newTreeNode.children) :
                diff.append([prevTreeNode.elementId, newTreeNode])

            helper(prevTreeNode.children, newTreeNode.children)
            
        helper(prevComponentTree, newComponentTree)
        return diff

    # def update(self, prevTree, prevNode, newNode):
    #     """
    #         recieve previous zenui dom tree
    #         update the previous tree changed node children
    #         with the new node children
    #         return the previous tree
    #         this opration is done after successfully updating the real dom
    #     """
    #     stack = [prevTree]
    #     while stack:
    #         curr = stack.pop()
    #         if isinstance(curr, Element):
    #             if curr.elementId == prevNode.elementId:
    #                 curr.children = newNode.children
    #             for i in curr.children:
    #                 stack.append(i)
    #     return prevTree

zenui_dom = ZenUIDom()


