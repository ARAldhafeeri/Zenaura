from .tags import tag 
from zenaura.client.tags import Node

def FloatButton(*children: Node, class_: str = "", size: int = 12, position: str = "bottom-right", **attrs) -> Node:
    """
    A floating action button.

    Args:
        children (Node): Child elements (e.g., icon or text).
        class_ (str): Tailwind classes for styling.
        size (int): The size of the button.
        position (str): Position of the button ('bottom-right', 'bottom-left', etc.).
        **attrs: Additional attributes for the button.

    Returns:
        Node: The floating action button element.

    Example Usage:
    FloatButton(
        Icon("plus", size=6, class_="fill-current"),
        class_="hover:bg-blue-600",
        size=14,
        position="bottom-right"
    )
    """
    position_classes = {
        "bottom-right": "fixed bottom-4 right-4",
        "bottom-left": "fixed bottom-4 left-4",
        "top-right": "fixed top-4 right-4",
        "top-left": "fixed top-4 left-4",
    }
    float_class = position_classes.get(position, "fixed bottom-4 right-4")
    size_class = f"w-{size} h-{size}"
    button_classes = f"rounded-full flex items-center justify-center bg-blue-500 text-white shadow-lg {float_class} {size_class} {class_}"

    return tag("button", *children, class_=button_classes, **attrs)