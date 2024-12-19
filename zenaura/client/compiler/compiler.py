from zenaura.client.tags import Node
from .attribute import AttributeProccessor
from .sanitize import CompilerSanitizer
import io
from zenaura.client.config import (
    ZENAURA_DOM_ATTRIBUTE,
    self_closing_tags
)


class Compiler(
    CompilerSanitizer,
    AttributeProccessor,
):
    """
    Compiles Zenui Nodes into their corresponding HTML representation.

    This class provides methods for:

    - Generating unique keyed UUIDs for each child within a component tree.
    - Compiling Zenui Nodes into HTML strings.
    - Sanitizing HTML content to prevent XSS vulnerabilities.
    - Processing attributes for HTML elements.

    Attributes:
        attrKeyWords (dict): A dictionary mapping attribute keywords to their corresponding HTML attribute names.
    """

    def __init__(self):
        """
        Initializes the Compiler instance with sanitizer and attribute processor

        """
        AttributeProccessor.__init__(self)

    def getKeyedUID(self, id, withAttribut=False, key=None):
        """
        Generates a unique keyed UUID for a child element within a component tree.

        This UUID is used to create a unique `ZENAURA_DOM_ATTRIBUTE` attribute for the element.

        Args:
            id (str): The unique ID of the parent component.
            withAttribut (bool, optional): Whether to include the `ZENAURA_DOM_ATTRIBUTE` attribute. Defaults to False.
            key (str or list, optional): The key or path of the child element. Defaults to None.

        Returns:
            str: The generated keyed UUID.

        Examples:
            ```python
            >>> compiler = Compiler()
            >>> compiler.getKeyedUID("my-component", key="child1")
            'my-componentchild1'
            >>> compiler.getKeyedUID("my-component", withAttribut=True, key=[0, 1])
            ' ZENAURA_DOM_ATTRIBUTE="my-component01"'
            ```
        """
        if isinstance(key, list):
            key = "".join(str(i) for i in key)  # Convert list to string

        if withAttribut:
            return f' {ZENAURA_DOM_ATTRIBUTE}="{id}{key}"'
        return f"{id}{key}"

    def compile(self, elm: Node, id=None, zenaura_dom_mode=False):
        """
        Compiles a Zenui Node into its corresponding HTML representation.

        Args:
            elm (Node): The Zenui Node object to compile.
            id (str, optional): The unique ID of the parent component. Used to generate keyed UUIDs.
            zenaura_dom_mode (bool, optional): Whether to add the `ZENAURA_DOM_ATTRIBUTE` attribute to the compiled HTML. Defaults to False.

        Returns:
            str: The compiled HTML string.

        Examples:
            ```python
            >>> compiler = Compiler()
            >>> node = Node("div", attributes=[Attribute("class", "my-class")], children=[Node("p", text="Hello, world!")])
            >>> compiler.compile(node)
            '<div class="my-class"><p>Hello, world!</p></div>'
            >>> compiler.compile(node, zenaura_dom_mode=True)
            '<div class="my-class" ZENAURA_DOM_ATTRIBUTE="div0"> <p ZENAURA_DOM_ATTRIBUTE="div00">Hello, world!</p></div>'
            ```
        """
        if elm.is_text_node or isinstance(elm, str):
            return self.sanitize(elm.text)

        tag = elm.name

        zenui_id = ""

        # Assign unique ID for Zenui DOM
        if isinstance(elm, Node) and zenaura_dom_mode:
            zenui_id = self.getKeyedUID(id, withAttribut=True, key=elm.path)

        # Get node attributes
        attributes = self.process_attributes(elm.attributes)

        if tag in self_closing_tags:
            return f"<{tag}{zenui_id}{attributes} />"

        # Start tag
        html = io.StringIO()
        html.write(f"<{tag}{zenui_id}{attributes}>")

        # Get children
        for child in elm.children:
            html.write(self.compile(child, id, zenaura_dom_mode))

        # Finish tag
        html.write(f"</{tag}>")

        return html.getvalue()