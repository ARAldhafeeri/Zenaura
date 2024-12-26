from .tags import tag 
from zenaura.client.tags import Node

def Alert(message: str, type_: str = "info", class_: str = "", **attrs) -> Node:
    """
    A reusable alert component.

    Args:
        message (str): The alert message.
        type_ (str): The type of alert (info, success, warning, error).
        class_ (str): Additional Tailwind classes for styling.
        **attrs: Additional attributes for the alert element.

    Returns:
        Node: The alert element.
    """
    type_classes = {
        "info": "bg-blue-100 text-blue-800 border-blue-500",
        "success": "bg-green-100 text-green-800 border-green-500",
        "warning": "bg-yellow-100 text-yellow-800 border-yellow-500",
        "error": "bg-red-100 text-red-800 border-red-500",
    }
    base_class = "p-4 border-l-4"
    final_class = f"{base_class} {type_classes.get(type_, '')} {class_}"

    return tag("div", text=message, class_=final_class, **attrs)