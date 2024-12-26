from .tags import tag 
from zenaura.client.tags import Node

def Icon(name: str, size: int = 24, class_: str = "", **attrs) -> Node:
    """
    An icon component for displaying SVG or icon fonts.

    Args:
        name (str): The name of the icon (e.g., Material Icons, Font Awesome class, or custom SVG).
        size (int): The size of the icon in pixels.
        class_ (str): Tailwind classes for styling.
        **attrs: Additional attributes for the icon element.

    Returns:
        Node: The icon element.
    
    Usage Example: 
      Icon("check-circle", size=20, class_="text-green-500")  # Font Awesome / Material Icons
      Icon("custom-icon-id", size=32, class_="fill-current", xmlns="http://www.w3.org/2000/svg")  # Custom SVG
    """
    
    # If it's a font-based icon:
    if attrs.get("icon_font", False):
        return tag(
            "i", 
            text=name, 
            class_=f"text-{size} {class_}", 
            **attrs
        )

    # For custom SVG:
    return tag(
        "svg", 
        tag("use", href=f"#{name}"), 
        class_=f"w-{size} h-{size} {class_}", 
        **attrs
    )