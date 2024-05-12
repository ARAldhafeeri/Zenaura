from zenaura.client.compiler import Compiler, ZENAURA_DOM_ATTRIBUTE
from zenaura.client.tags import Node
from collections import defaultdict
from zenaura.client.component import Component
from pyscript import document 
from functools import wraps
import inspect

compiler = Compiler()

class DefaultDomErrorComponent(Component):
    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message
    def node(self):
        return Node("div", children=[Node("p", children=[str(self.error_message)])])

class Dom:

    def __init__(self):
        """
        initialize zenaura dom
        attributes:
            - self.zen_dom_table: A dictionary that maps component IDs to their node trees.
            - self.mounted_component_id: currently mounted container component identifier.
        """
        self.zen_dom_table = defaultdict(str)
        self.prev_component_id = None
        self.prev_component_instance = None
        self.mounted_component_id = None


    def componentDidCatchError(self, comp, error) -> None:
        """
            Graceful degradation of component lifecycle methods.
        """
        if hasattr(comp, "componentDidCatchError"):
             # call componentDidCatchError method
             # mount the error message component 
             error_comp = comp.componentDidCatchError(str(error))
             compiled_comp = compiler.compile(
                 error_comp, 
                 componentName=comp.__class__.__name__,
                 zenaura_dom_mode=True
             )
             dom_node = document.getNodeById("root")
             dom_node.innerHTML = compiled_comp
             self.prev_component_id = comp.componentId
             self.zen_dom_table[comp.componentId] = error_comp
        else:
            # mount the default error message component 
            error_comp  = DefaultDomErrorComponent(error_message=str(error))
            error_comp = error_comp.node()
            compiled_comp = compiler.compile(
                 error_comp, 
                 componentName=comp.__class__.__name__,
                 zenaura_dom_mode=True
             )
            dom_node = document.getNodeById("root")
            dom_node.innerHTML = compiled_comp
            self.prev_component_id = comp.componentId
            self.zen_dom_table[comp.componentId] = error_comp
            self.mounted_component_id = comp.componentId


    # mounting 
    def mount(self, comp  ) -> None:
        """
            Mount the component, goes through the life cycle methods and mounts the component to the DOM.
            try : 
                - mount the component.
            except:
                - call componentDidCatchError method.
            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        # wrapped life cycle method componentDidCatchError 
        # mount steps 1-4: componentWillMount -> mount -> unmount -> componentWillUnmount -> componentDidMount
        # mount 1: lifecycle method to be called before mounting
        try : 
            self.componentWillMount(comp)

            # mount 2: mount the component to the DOM
            comp_tree = comp.node()
            compiled_comp = compiler.compile(
                comp_tree, 
                componentName=comp.__class__.__name__,
                zenaura_dom_mode=True
            )

            dom_node = document.getNodeById("root") 
            dom_node.innerHTML = compiled_comp

            self.zen_dom_table[comp.componentId] = comp_tree

            # mount 3: lifecycle method the component will be unmountted
            # assign the component id to the mounted component id
            self.unmount(self.prev_component_instance)

            # mount 4 : lifecycle method to be called after mounting
            self.mounted_component_id = comp.componentId

            self.componentDidMount(comp)

        except Exception as e:
            self.componentDidCatchError(comp, str(e))

    def unmount(self, comp) -> None:
        """
        Unmounts the component and performs cleanup operations.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # no component mounted
        if not comp:
            return 
        # if component has componentWillUnmount methd call it before unmounting
        if hasattr(comp, 'componentWillUnmount'):
            comp.componentWillUnmount()  
        # Perform virtual dom cleanup operations here
        del self.zen_dom_table[comp.componentId]

    def componentWillMount(self, comp) -> None:
        """
        Method called before the component is mounted to the DOM.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        if hasattr(comp, 'componentWillMount') and self.mounted_component_id != comp.componentId:
            comp.componentWillMount()

    def componentWillUnmount(self, comp) -> None:
        """
        Method called before the component is unmounted from the DOM.
        """
        if hasattr(comp, 'componentWillUnmount'):
            comp.componentWillUnmount()

    def componentDidMount(self, comp) -> None:
        """
        Method called after the component is mounted to the DOM.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        if hasattr(comp, 'componentDidMount'):
            comp.componentDidMount()


    # updating
    def render(self, comp ) -> None:
        """
            Renders the component by updating the DOM based on the differences between the previous and new component trees.

            Parameters:
            - comp: An instance of the Component class.

            Returns:
            None
        """
        try:

            # update steps 1-3: componentWillUpdate -> update -> componentDidUpdate
            # update 1: lifecycle method to be called before updating
            self.componentWillUpdate(comp)

            # update 2: update the component in the DOM
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

                document.querySelector(f'[{ZENAURA_DOM_ATTRIBUTE}="{prevNodeId}"]').innerHTML  = compiled_comp
                self.update(prevTree, prevNodeId, newNodeChildren)
            self.zen_dom_table[comp.componentId] = prevTree

            # update 3  : componentDidUpdate method to be called after updating
            self.componentDidUpdate(comp)

        except Exception as e:
            print("render error: ", str(e))
            self.componentDidCatchError(comp, str(e))       

    def componentWillUpdate(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'componentWillUpdate'):
            comp.componentWillUpdate()

    def componentDidUpdate(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'componentDidUpdate'):
            comp.componentDidUpdate()

    # dom diffing algorithm
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


