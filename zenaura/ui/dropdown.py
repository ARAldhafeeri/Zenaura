from .tags import tag 
from zenaura.client.tags import Node


def Dropdown(
    label: str,
    options: list,
    class_: str = "",
    **attrs
) -> Node:
    """
    A dropdown menu component.

    Args:
        label (str): The dropdown button label.
        options (list): List of option labels.
        class_ (str): Tailwind classes for styling.
        **attrs: Additional attributes.

    Returns:
        Node: The dropdown container.

    Example Usage: 
      Dropdown(
          label="Options",
          options=["Option 1", "Option 2", "Option 3"],
          class_="hover:bg-blue-600"
      )
    """
    dropdown_items = [
        tag(
            "li",
            tag("a", option, class_="block px-4 py-2 hover:bg-gray-100"),
            class_="cursor-pointer"
        )
        for option in options
    ]
    return tag(
        "div",
        tag(
            "button",
            label,
            class_=f"dropdown-btn px-4 py-2 bg-blue-500 text-white rounded {class_}",
            **attrs
        ),
        tag(
            "ul",
            *dropdown_items,
            class_="dropdown-menu mt-2 hidden bg-white border border-gray-200 rounded shadow-lg"
        ),
        class_="relative dropdown"
    )
