import uuid
from typing import List, Optional
from zenaura.client.config import self_closing_tags
from .attribute import Attribute

def update_root_properties(root):
    """
        Upon intialization of a node or setting children
        This method create infromation rich tree nodes:
        1. link children to their parent
        2. assign level, key information 
        3. is_leaf_node, is_text node
        and so on
    """
    stack = [(root, None, 0, 0, root.path)] # (node, level_parent, level, index, path)

    while stack :
        curr, curr.parent, curr.level, curr.key, curr.path   = stack.pop()
        curr.is_leaf = len(curr.children) == 0
        for idx, child in enumerate(curr.children):
            if isinstance(child, str):
                child = Node(text=child)
                child.is_text_node = True
            child.is_leaf = len(child.children) == 0
            curr.children[idx] = child
            stack.append((child, child, curr.level + 1, idx, curr.path + str(curr.level) + str(idx)))
    return root

class NodeList(list):
    """Custom list subclass to trigger update on append."""

    def __init__(self, node, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node = node  # Reference to the parent Node

    def append(self, child):
        super().append(child)
        self.node.children = self  # Trigger the setter
    
class Node:
    def __init__(
            self,name : str = None, 
            children: Optional[List["Node"]]=None, 
            attributes : Optional[List[Attribute]]=None,
            text: str = None,
            ):
        """
        Represents an HTML element with attributes, children, and text content.

        Attributes:
            name (str): The tag name of the element.
            children (list of Node): The child elements of this node.
            attributes (list of Attribute): The attributes of this node.
            text (str, optional): The text content of this node.
            nodeId (str): A unique identifier for this node.
            is_leaf (bool): Whether this node has no children.
            is_text_node (bool): Whether this node represents text content.
            level (int): The depth of this node in the tree.
            key (int): A unique identifier for this node within its level.
            path (str): The path from the root to this node.
        """
        self._parent = None

        # calculated properties
        self._level = 0
        self._key = 0 
        self._is_leaf = True
        self._path = ""

        self.name = name
        self._children = children if children else []
        self.attributes = [] if attributes is None else attributes
        self.nodeId = uuid.uuid4().hex
        self.text = text        
        # calculated proerty depends on children, text
        self._is_text_node = isinstance(self.text, str)
        update_root_properties(self)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level

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
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path

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
        self._children = new_children
        update_root_properties(self)

    def append_child(self, child):
        """
        Adds a child node to this node.

        Args:
            child (Node or str): The child node to add. If a string is provided,
                it will be converted to a text node.
        """
        if isinstance(child, str):
            child = Node(text=child)
            child.is_text_node = True
        self.children.append(child)
        update_root_properties(self)
    
    def to_dict(self) -> dict:
        """
        Converts this node and its children into a nested dictionary representation.

        Returns:
            dict: A dictionary representing the node and its children.
        """
        return {
            "name": self.name,
            "parent": self.parent.name if self.parent else "none",
            "level" : self.level,
            "key": self.key,
            "path": self.path,
            "children": [child.to_dict() if isinstance(child, Node) else child for child in self.children],
        }
    
    def getAttributes(self, node) -> List[Attribute]:
        attrs = []
        for attr in node.attributes:
            attrs.append(f' {attr.key}="{attr.value}"')
        return "".join(attrs)
    
    def to_html(self) -> str:
        """
        Converts this node and its children into an HTML string.

        Returns:
            str: The HTML representation of the node and its children.
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
        Finds a child node with the given name.

        Args:
            name (str): The name of the child node to find.

        Returns:
            Node: The child node with the given name, or None if not found.
        """
        for child in self.children:
            if isinstance(child, Node):
                if child.name == name:
                    return child
        return None 
    
    def findAllByName(self, name) -> List["Node"]:
        """
        Finds all child nodes with the given name.

        Args:
            name (str): The name of the child nodes to find.

        Returns:
            List[Node]: A list of child nodes with the given name.
        """
        found = []
        for child in self.children:
            if isinstance(child, Node):
                if child.name == name:
                    found.append(child)

        return found 
    
    def findByAttribute(self, key : str, value : str) -> "Node":
        """
        Finds a child node with the given attribute key and value.

        Args:
            key (str): The attribute key to search for.
            value (str): The attribute value to search for.

        Returns:
            Node: The child node with the given attribute, or None if not found.
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
        Finds all child nodes with the given attribute key.

        Args:
            key (str): The attribute key to search for.

        Returns:
            List[Node]: A list of child nodes with the given attribute key.
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
        Finds all child nodes with the given attribute value.

        Args:
            value (str): The attribute value to search for.

        Returns:
            List[Node]: A list of child nodes with the given attribute value.
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
        Replaces a child node with a new node.

        Args:
            oldNode (Node): The node to be replaced.
            newNode (Node): The new node to replace it with.
        """
        found = self.getChildIndex(oldNode)
        if found:
            self.children[found] = newNode
    
    def getChildIndex(self,node : "Node") -> int :
        """
        Gets the index of a child node.

        Args:
            node (Node): The child node to find the index of.

        Returns:
            int: The index of the child node, or -1 if not found.
        """
        for idx, child in enumerate(self.children):
              if isinstance(child, Node):
                if child.nodeId == node.nodeId:
                    return idx
                
    def insertAfter(self, node : "Node", newNode : "Node") -> None:
        """
        Inserts a new node after a specific child node.

        Args:
            node (Node): The child node to insert after.
            newNode (Node): The new node to insert.
        """
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            self.children.insert(foundIdx + 1, newNode)
    
    def insertBefore(self, node : "Node", newNode : "Node") -> None:
        """
        Inserts a new node before a specific child node.

        Args:
            node (Node): The child node to insert before.
            newNode (Node): The new node to insert.
        """
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            self.children.insert(foundIdx, newNode)

    def remove(self, node : "Node"):
        """
        Removes a child node.

        Args:
            node (Node): The child node to remove.
        """
        foundIdx = self.getChildIndex(node)
        if foundIdx:
            del self.children[foundIdx]

    def appendAttributeToChild(self, node : "Node", attribute : "Attribute") -> None:
        """
        Appends an attribute to a child node.

        Args:
            node (Node): The child node to add the attribute to.
            attribute (Attribute): The attribute to add.
        """
        for child in self.children:
            if isinstance(child, Node):
                if child.nodeId == node.nodeId:
                    child.attributes.append(attribute)
