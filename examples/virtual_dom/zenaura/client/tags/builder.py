from .attribute import Attribute
from .node import Node

class TagBuilder:
    def __init__(self, name : str) -> None:
        """
        Initializes a TagBuilder object with the given name.

        Args:
        name (str): The name of the tag.
        """
        self.node = Node(name)
    
    def with_attribute(self, key : str, value : any) -> "TagBuilder":
        """
        Adds an attribute to the tag.

        Args:
        key (str): The key of the attribute.
        value: The value of the attribute.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        self.node.attributes.append(Attribute(key,value))
        return self
    
    def with_child(self, child : Node) -> "TagBuilder":
        """
        Adds a child node to the tag.

        Args:
        child (Node): The child node to be added.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        self.node.children.append(child)
        return self 
    
    def with_styles(self, styles: dict) -> "TagBuilder":
        """
        Adds styles to the tag.

        Args:
        styles (dict): Dictionary of styles.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
        self.node.attributes.append(Attribute("style", style_str))
        return self
    
    def with_classes(self, *class_names: str) -> "TagBuilder":

        """
        Adds multiple class names to the element.

        Args:
        *class_names (str): Variable number of class names.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        for class_name in class_names:
            self.with_class(class_name)
        return self
    
    def with_class(self, class_name: str) -> "TagBuilder":
        """
        Adds a single class name to the element.

        Args:
        class_name (str): The class name to be added.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        for i in self.node.attributes:
            if i.key =="class":
                if class_name not in i.value:
                    i.value = i.value + " " +  class_name
                    return self
        self.node.attributes.append(Attribute("class", class_name))
       
        return self

    def with_class_if(self, class_name: str, condition: bool) -> "TagBuilder":
        """
        Adds a class name to the element if the condition is True.
        If the condition is False, the class is not added.

        args : 
            class_name (str): The class name to be added.
            condition (bool): The condition for adding the class.
        """
        self.with_class(class_name) if condition else None
        return self 

    def with_attribute_if(self, key : str, value : any, condition: bool) -> "TagBuilder":
        """
            adds attribute if condition is true 
            args :
            key (str): The key of the attribute.
            value: The value of the attribute.
            condition (bool): The condition for adding the attribute.
        """
        self.with_attribute(key, value) if condition else None
        return self
    
    def with_child_if(self, child : Node, condition: bool) -> "TagBuilder":
        """
            adds child if condition is true
            args :
            child (Node): The child node to be added.
            condition (bool): The condition for adding the child.
        """
        self.with_child(child) if condition else None
        return self

    
    def build(self):
        """
        Builds and returns the node.

        Returns:
        Node: The built node.
        """
        return self.node