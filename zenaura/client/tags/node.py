import uuid
from typing import List, Optional
from zenaura.client.config import self_closing_tags
from .attribute import Attribute

class ChildrenList(list):
    def __init__(self, parent_node, children):
        super().__init__()
        self.parent_node = parent_node
        self.children = children
        self._child_counter = 0

        for child in self.children:
            self.append(child)

    def append(self, child):
        if isinstance(child, str):
            child = Node(text=child)
            child.is_text_node = True

        child._parent = self.parent_node
        child.level = self.parent_node.level + 1
        child.key = self._child_counter  # Assign a unique key
        self._child_counter += 1        # Increment the counter

        child.is_text_node = isinstance(child.text, str)
        child.is_leaf = len(child.children) == 0
        self.parent_node.is_leaf = len(self.children) == 0
        super().append(child)

    def __delitem__(self, index):
        """Handle deletion, but don't reset the counter."""
        deleted_child = self[index]
        super().__delitem__(index)
        deleted_child._parent = None
        self.parent_node.is_leaf = len(self.children) == 0

    def insert(self, index, child):
        """Handle insertion, assigning a new unique key."""
        if isinstance(child, str):
            child = Node(text=child)
            child.is_text_node = True

        child._parent = self.parent_node
        child.level = self.parent_node.level + 1
        child.key = self._child_counter
        self._child_counter += 1

        super().insert(index, child)
        self.parent_node.is_leaf = len(self.children) == 0

    
class Node:
    def __init__(
            self,name : str = None, 
            children: Optional[List["Node"]]=None, 
            attributes : Optional[List[Attribute]]=None,
            text: str = None,
            ):
        """
        Initializes a Node object with the given name, children, and attributes.

        Args:
        name (str): The name of the node.
        children (list, optional): List of children nodes. Defaults to None.
        attributes (list, optional): List of attributes. Defaults to None.
        """

        # calculated properties
        self._level = 0
        self._key = 0 # root key
        self._parent = None
        self._is_leaf = True

        self.name = name
        self.next_child_index = 0
        self.children =ChildrenList(self, children if children else [])
        self._children =ChildrenList(self, children if children else [])
        self.attributes = [] if attributes is None else attributes
        self.nodeId = uuid.uuid4().hex
        self.text = text        
        # calculated proerty depends on children, text
        self._is_text_node = isinstance(self.text, str)



    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level
        for child in self.children:
            child.level = new_level + 1  # Recursively update child levels

    @property
    def is_leaf(self):
        return self._is_leaf

    @is_leaf.setter
    def is_leaf(self, new_is_leaf):
        self._is_leaf = new_is_leaf

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        self._key = new_key

    @property
    def is_text_node(self):
        return self._is_text_node

    @is_text_node.setter
    def is_text_node(self, new_is_text_node):
        self._is_text_node = new_is_text_node

    @property
    def parent(self):
        """Read-only property referencing the node's parent."""
        return self._parent

    @parent.setter
    def parent(self, new_parent):
        self._parent = new_parent

    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, new_children):
        """Intercept assignment to update child relationships"""
        self._children = ChildrenList(self, new_children) # Handle None input
        self.is_leaf = len(new_children) == 0

    def to_dict(self) -> dict:
        """
            convert a node object into nested dictionary.
        """
        return {
            "name": self.name,
            "children": [child.to_dict() if isinstance(child, Node) else child for child in self.children],
        }
    
    def getAttributes(self, node) -> List[Attribute]:
        attrs = []
        for attr in node.attributes:
            attrs.append(f' {attr.key}="{attr.value}"')
        return "".join(attrs)
    
    def to_html(self) -> str:
        """
            convert a node object into html string.
        """
        if self.name in self_closing_tags:
            return f"<{self.name}{self.getAttributes(self)}>"
        
        html = f"<{self.name}"
        html += f"{self.getAttributes(self)}"
        html += ">"
        for child in self.children:
            if child.is_text_node:
                html += child.text
            elif isinstance(child, Node):
                html += child.to_html()
            else:
                html += str(child)
        html += f"</{self.name}>"
        return html
    
    def findChildByName(self, name : str) -> "Node":
        """
            find a child node by name.
            args :
                name - child name
            returns :
                None | Node
        """
        for child in self.children:
            if isinstance(child, Node):
                if child.name == name:
                    return child
        return None 
    
    def findAllByName(self, name) -> List["Node"]:
        """
            find all children by name.
            args :
                name - child name
            returns:
                List["Node"] | []
        """
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if child.name == name:
                    found.append(child)

        return found 
    
    def findByAttribute(self, key : str, value : str) -> "Node":
        """
            find a child node by attribute key and value.
            args :
                name - child name
            returns:
                "Node" | None
        """
        found = None
        for child in self.children:
            if isinstance(child, Node):
                for attribute in child.attributes:
                    if attribute.key == key and attribute.value == value:
                        return child
        return found 
    
    def findAllChildrenByAttributeKey(self, key : str) -> List["Node"]:
        """
            find all node children by attribute key.
            args :
                name - child name
            returns:
                list of nodes or empty list
        """
        found = []
        for child in self.children:
            if isinstance(child, Node):
                for attribute in child.attributes:
                    if attribute.key == key :
                        found.append(child)
                        break
        return found 
    
    def findAllChildrenByAttributeValue(self, value : str) -> List["Node"]:
        """
            find all node children by attribute key.
            args :
                name - child name
            returns:
                list of nodes or empty list
        """
        found = []
        for child in self.children:
            if isinstance(child, Node):
                for attribute in child.attributes:
                    if attribute.value == value :
                        found.append(child)
                        break
        return found
    
    def replace(self, oldNode : "Node", newNode: "Node") -> None:
        """
            replace node child with a new node
            args :
                name - child name
                newNew - new node to replace child with
            returns:
                None
        """
        found = self.getChildIndex(oldNode)
        if found:
            self.children[found] = newNode
    
    def getChildIndex(self,node : "Node") -> int :
        """
            get child index 
            args :
                name - child name
            returns:
                int
        """
        for idx, child in enumerate(self.children):
              if isinstance(child, Node):
                if child.nodeId == node.nodeId:
                    return idx
                
    def insertAfter(self, node : "Node", newNode : "Node") -> None:
        """
            insert new child node after a specific child
            args :
                name - child name
                newNode - node instance
            returns:
                int
        """
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            self.children.insert(foundIdx + 1, newNode)
    
    def insertBefore(self, node : "Node", newNode : "Node") -> None:
        """
            insert new child node before a specific child
            args :
                name - child name
            returns:
                int
        """
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            self.children.insert(foundIdx, newNode)

    def remove(self, node : "Node"):
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            del self.children[foundIdx]

    def appendAttributeToChild(self, node : "Node", attribute : "Attribute") -> None:
            """
                appendAttribute to child
                args :
                    name - child name
                    newNew - new node to replace child with
                returns:
                    None
            """
            for child in self.children:
              if isinstance(child, Node):
                if child.nodeId == node.nodeId:
                    child.attributes.append(attribute)
