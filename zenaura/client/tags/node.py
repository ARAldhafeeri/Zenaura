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
        Initializes a Node object with the given name, children, and attributes.

        Args:
        name (str): The name of the node.
        children (list, optional): List of children nodes. Defaults to None.
        attributes (list, optional): List of attributes. Defaults to None.
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
        if isinstance(child, str):
            child = Node(text=child)
            child.is_text_node = True
        child.level = self.level + 1
        child.key = len(self.children)
        child.parent = self 
        child.is_leaf = len(child.children) == 0 
        child.path = f'{self.path}{child.level}{child.key}'
        self.children.append(child)
    
    def to_dict(self) -> dict:
        """
            convert a node object into nested dictionary.
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
