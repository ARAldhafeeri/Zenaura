from zenaura.client.tags import Node 
from .tags import tag 

def Grid(*children: Node, columns: int = 12, gap: int = 4, class_: str = "", **attrs) -> Node:
    """
    A grid container for arranging child elements.

    Args:
        columns (int): Number of grid columns (default: 12).
        gap (int): Spacing between grid items.
        class_ (str): Additional classes for the grid container.
        **attrs: Additional attributes for the container.

    Returns:
        Node: The grid container.

    example usage: 
      Grid(
        p(text="Col 1", class_="bg-green-100 p-4"),
        p(text="Col 2", class_="bg-green-200 p-4"),
        p(text="Col 3", class_="bg-green-300 p-4"),
        columns=3,
        gap=6
      )
    """
    grid_classes = f"grid grid-cols-{columns} gap-{gap} {class_}"
    return tag("div", *children, class_=grid_classes, **attrs)