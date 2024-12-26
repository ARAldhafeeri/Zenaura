
from .tags import tag 

def Badge(label: str, color: str = "blue", class_: str = "px-2 py-1 rounded text-sm font-semibold") -> Node:
    """
    A reusable badge component.

    Args:
        label (str): The badge text.
        color (str): The color of the badge (e.g., blue, green, red).
        class_ (str): Tailwind classes for styling.

    Returns:
        Node: The badge element.
    """
    color_classes = f"bg-{color}-100 text-{color}-800"
    return tag("span", text=label, class_=f"{class_} {color_classes}")