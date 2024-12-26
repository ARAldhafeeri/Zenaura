from zenaura.client.tags import Node 
from .tags import tag 

def Flex(*children: Node, direction: str = "row", justify: str = "start", align: str = "stretch", gap: int = 2, wrap: bool = False, class_: str = "", **attrs) -> Node:
    """
    A flexible container for arranging child elements.

    Args:
        direction (str): Flex direction ('row', 'col').
        justify (str): Justify content ('start', 'center', 'end', 'between', 'around').
        align (str): Align items ('stretch', 'start', 'center', 'end').
        gap (int): Spacing between items.
        wrap (bool): Whether the flex items should wrap.
        class_ (str): Additional classes for the container.
        **attrs: Additional attributes for the container.

    Returns:
        Node: The flex container.

    Example Usage:
    Flex(
        h1(text="Item 1", class_="bg-blue-100 p-4"),
        p(text="Item 2", class_="bg-blue-200 p-4"),
        direction="row",
        justify="center",
        gap=4
    )
    """
    flex_classes = f"flex flex-{direction} justify-{justify} items-{align} gap-{gap} {'flex-wrap' if wrap else ''} {class_}"
    return tag("div", *children, class_=flex_classes, **attrs)
