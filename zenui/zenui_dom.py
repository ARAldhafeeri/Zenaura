from zenui.compiler import ZenuiCompiler
# compile zenui html dataclasses to html text
from pyscript import document 
from zenui.tags import Element
from collections import defaultdict
compiler = ZenuiCompiler()

compiler = ZenuiCompiler()

class ZenUIDom:

    def __init__(self):
        self.zen_dom_table = defaultdict(str)


    def render(self, comp ) -> None:
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        prevTree = self.zen_dom_table[comp.componentId]
        k = isinstance(prevTree, Element)
        print(k, type(prevTree))
        newTree = comp.element()
        oldNode, newNode = self.search(prevTree, newTree)

        compiled_comp = compiler.compile(
            newNode.children, 
            componentName=comp.__class__.__name__,
            zenui_dom_mode=True
        )
        document.querySelector(f'[data-zenui-id="{oldNode.elementId}"]').outerHTML  = compiled_comp

    def mount(self, comp  ) -> None:
        """
            comp : recieve instance of ZenUIComponent 
            1. create element tree
            2. compiles html
            3. attach container to root node 
            4. used in zenui simple router to mount elements
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
            return parent of deepest level where
            change in childreen tree ocurred
            old : component old tree before change
            new : component new tree after change
            returns: deepest level of change [newNode, oldNode ]
        """
        max_depth = -1
        max_level_parent_old = prevComponentTree
        max_level_parent_new = newComponentTree
        def helper(prevTreeNode : Element, newTreeNode : Element, depth):
            nonlocal max_depth, max_level_parent_old, max_level_parent_new
            if (not prevTreeNode) or (not newTreeNode):
                return
            if (not isinstance(prevTreeNode, Element )) or (not isinstance(newTreeNode, Element )):
                return  
            if prevTreeNode.children != newTreeNode.children:
                if depth > max_depth:
                    max_depth = depth
                    max_level_parent_new = newTreeNode
                    max_level_parent_old = prevTreeNode
            for prev, curr in zip(prevTreeNode.children, newTreeNode.children):
                helper(prev, curr, depth + 1)
            
        helper(prevComponentTree, newComponentTree, 0)
        return [max_level_parent_new, max_level_parent_old]


zenui_dom = ZenUIDom()


