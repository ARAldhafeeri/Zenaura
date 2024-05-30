from .attribute import Attribute
from .node import Node

class Builder:
    """
    A builder class for constructing HTML tags.

    This class provides a fluent interface for creating HTML tags with attributes,
    children, and styles. It simplifies the process of building complex HTML structures.

    Attributes:
        node (Node): The root node of the tag being built.
    """

    def __init__(self, name: str = "div") -> None:
        """
        Initializes a Builder object with the given tag name.

        Args:
            name (str, optional): The name of the tag. Defaults to "div".
        """
        self.node = Node(name)

    def with_attributes(self, **kwargs) -> "Builder":
        """
        Adds attributes to the tag.

        Args:
            **kwargs: Key-value pairs of attributes.

        Returns:
            Builder: The Builder object.
        """
        for key, value in kwargs.items():
            self.with_attribute(key, value)
        return self

    def with_children(self, *children) -> "Builder":
        """
        Adds child nodes to the tag.

        Args:
            *children: List of child nodes.

        Returns:
            Builder: The Builder object.
        """
        for child in children:
            self.with_child(child)
        return self

    def with_attribute(self, key: str, value: any) -> "Builder":
        """
        Adds an attribute to the tag.

        Args:
            key (str): The key of the attribute.
            value: The value of the attribute.

        Returns:
            Builder: The Builder object.
        """
        self.node.attributes.append(Attribute(key, value))
        return self

    def with_child(self, child: Node) -> "Builder":
        """
        Adds a child node to the tag.

        Args:
            child (Node): The child node to be added.

        Returns:
            Builder: The Builder object.
        """
        self.node.append_child(child)
        return self

    def with_styles(self, styles: dict) -> "Builder":
        """
        Adds styles to the tag.

        Args:
            styles (dict): Dictionary of styles.

        Returns:
            Builder: The Builder object.
        """
        style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
        self.node.attributes.append(Attribute("style", style_str))
        return self

    def with_classes(self, *class_names: str) -> "Builder":
        """
        Adds multiple class names to the element.

        Args:
            *class_names (str): Variable number of class names.

        Returns:
            Builder: The Builder object.
        """
        for class_name in class_names:
            self.with_class(class_name)
        return self

    def with_class(self, class_name: str) -> "Builder":
        """
        Adds a single class name to the element.

        Args:
            class_name (str): The class name to be added.

        Returns:
            Builder: The Builder object.
        """
        for i in self.node.attributes:
            if i.key == "class":
                if class_name not in i.value:
                    i.value = i.value + " " + class_name
                    return self
        self.node.attributes.append(Attribute("class", class_name))

        return self

    def with_class_if(self, class_name: str, condition: bool) -> "Builder":
        """
        Adds a class name to the element if the condition is True.
        If the condition is False, the class is not added.

        args:
            class_name (str): The class name to be added.
            condition (bool): The condition for adding the class.
        """
        self.with_class(class_name) if condition else None
        return self

    def with_attribute_if(self, key: str, value: any, condition: bool) -> "Builder":
        """
            adds attribute if condition is true
            args:
            key (str): The key of the attribute.
            value: The value of the attribute.
            condition (bool): The condition for adding the attribute.
        """
        self.with_attribute(key, value) if condition else None
        return self

    def with_child_if(self, child: Node, condition: bool) -> "Builder":
        """
            adds child if condition is true
            args:
            child (Node): The child node to be added.
            condition (bool): The condition for adding the child.
        """
        self.with_child(child) if condition else None
        return self

    def with_text(self, text: str):
        """
            add text node
        """
        self.with_child(Node(text=text))
        return self

    def build(self) -> Node:
        """
        Builds and returns the node.

        Returns:
            Node: The built node.
        """
        return self.node
