from zenaura.client.tags import Node 
from .tags import tag 

def Typography(*children: Node, variant: str = "p", class_: str = "", **attrs) -> Node:
    """
    A typography component for text elements.

    Args:
        variant (str): The type of text element ('h1', 'h2', 'h3', 'h4', 'p', 'small', etc.).
        class_ (str): Tailwind classes for styling.
        **attrs: Additional attributes for the text element.

    Returns:
        Node: The typography element.
    """
    return tag(variant, *children, class_=class_, **attrs)
