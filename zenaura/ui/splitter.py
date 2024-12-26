from zenaura.client.tags import Node 
from .tags import tag 

def SpaceSplitter(*children: Node, direction: str = "horizontal", size: int = 4, align: str = "center", class_: str = "", **attrs) -> Node:
    """
    A splitter container for spacing elements.

    Args:
        direction (str): Direction ('horizontal' or 'vertical').
        size (int): Spacing between items.
        align (str): Alignment ('start', 'center', 'end').
        class_ (str): Additional classes for the container.
        **attrs: Additional attributes for the container.

    Returns:
        Node: The space splitter container.

    example usage:
    SpaceSplitter(
        tag("div", text="Item 1", class_="bg-red-100 p-2"),
        tag("div", text="Item 2", class_="bg-red-200 p-2"),
        tag("div", text="Item 3", class_="bg-red-300 p-2"),
        direction="horizontal",
        size=6,
        align="center"
    )
    """
    direction_class = "flex-row" if direction == "horizontal" else "flex-col"
    splitter_classes = f"flex {direction_class} items-{align} gap-{size} {class_}"
    return tag("div", *children, class_=splitter_classes, **attrs)