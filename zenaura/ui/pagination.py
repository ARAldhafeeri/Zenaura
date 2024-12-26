from .tags import tag 
from zenaura.client.tags import Node

def Pagination(
    total_pages: int,
    current_page: int = 1,
    class_: str = "",
    id: str = "",
    **attrs
) -> Node:
    """
    A pagination component.

    Args:
        total_pages (int): Total number of pages.
        current_page (int): The currently active page.
        class_ (str): Tailwind classes for styling.
        id (str): element id to bind method to.
        **attrs: Additional attributes.

    Returns:
        Node: The pagination container.
    
    Usage:
    Pagination(
        total_pages=10,
        current_page=3,
        on_click="handlePageChange",
        class_="mt-4"
    )
    """
    page_items = []
    for i in range(1, total_pages + 1):
        page_class = (
            "px-4 py-2 border rounded cursor-pointer"
            + (" bg-blue-500 text-white" if i == current_page else " hover:bg-gray-100")
        )
        page_items.append(
            tag(
                "button",
                str(i),
                class_=page_class,
                **attrs,
                id=id
            )
        )
    return tag("div", *page_items, class_=f"pagination flex gap-2 {class_}", **attrs)
