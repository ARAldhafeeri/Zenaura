from zenaura.client.tags import Node 
from .tags import tag 

def Layout(*children: Node, header: Node = None, footer: Node = None, sider: Node = None, class_: str = "", **attrs) -> Node:
    """
    A layout component supporting header, sider, content, and footer.

    Args:
        header (Node): The header element.
        footer (Node): The footer element.
        sider (Node): The sidebar element.
        class_ (str): Additional classes for the layout.
        **attrs: Additional attributes for the container.

    Returns:
        Node: The layout container.

    example usage:
    Layout(
        tag("main", text="Main Content", class_="p-4 flex-1"),
        header=tag("div", text="Header"),
        sider=tag("div", text="Sidebar"),
        footer=tag("div", text="Footer"),
        class_="min-h-screen"
    )
    """
    layout_children = []
    if header:
        layout_children.append(tag("header", header, class_="bg-gray-800 text-white p-4"))
    if sider:
        layout_children.append(tag("aside", sider, class_="bg-gray-100 p-4 w-1/4"))
    layout_children.extend(children)
    if footer:
        layout_children.append(tag("footer", footer, class_="bg-gray-800 text-white p-4"))

    layout_classes = "flex flex-row" if sider else "flex flex-col"
    return tag("div", *layout_children, class_=f"{layout_classes} {class_}", **attrs)