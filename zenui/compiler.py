from zenui.tags import Element, Attribute
from typing import List 
class ZenuiCompiler:
    def __init__(self):
        # A dictionary to map ZenUI-specific attribute names to standard HTML
        # attribute names (e.g., convert "styles" attribute to "class"). 
        self.attrKeyWords = {
            "styles": "class"
        }

    def compile(self, elm: Element, parent=True, componentName=None, componentId=None):
        """Compiles a Zenui Element into its corresponding HTML representation.

        Args:
            elm: The Zenui Element object to compile.
            parent: true by default, zenui set data-zenui-id to every parent component
            the data-zenui-id will be used in zenui-dom functionality
            in tests, if not testing zenui-dom, set this to false.
            componentName: for event handling attributes like onclick,
            transcript needs the following format : 
            "index.componentName.eventHandler"
            this must be the output for every event handler
            otherwise the component event handler will not work.
            passed optionally as None for testing purposes.

        Returns:
            A string containing the compiled HTML.
        """

        tag = elm.name 

        if elm.name == "text":
            # Special handling for text elements - directly return the text content
            return str(elm.children[0]) 

        attributes = self.process_attributes(elm.attributes, componentName) 
        children = self.compile_children(elm.children)
        
        zen_ui_id = ""
        if parent:
           zen_ui_id = f' data-zenui-id="{componentId}"'
        # Construct the HTML tag including attributes and children
        return f"<{tag}{attributes}{zen_ui_id}>{children if children else ''}</{tag}>" 

    def process_attributes(self, attrs: List[Attribute], componentName=None) -> str:
        """Processes a list of Attributes, converting them to HTML-formatted attributes.

        Args:
            attrs: A list of Zenui Attribute objects.

        Returns:
            A string containing the HTML-formatted attributes, ready to be included in a tag.
        """

        attr_parts = []  # Create a string buffer for building the output

        for i, attr in enumerate(attrs):
            attrKey = attr.key
            attrValue = attr.value
            if attrKey in self.attrKeyWords.keys():
                attrKey = self.attrKeyWords[attrKey]  # Apply keyword mapping

            #format event handlers
            if componentName and ("on" in attrKey):
                # transcrypt expect the following main.className.eventHandlerName()
                # lower first letter of component name
                # add the rest
                componentName = componentName[0].lower() + componentName[1:]
                attrValue = f"main.{componentName}.{attrValue.__name__}()"

            # Add space only if it's not the first or last attribute
            if i == 0 or i == len(attrs) - 1:
                attr_parts.append(f' {attrKey}="{attrValue}"')
            else:
                attr_parts.append(f'{attrKey}="{attrValue}" ')

        return "".join(attr_parts)

    def compile_children(self, children):
        """Recursively compiles a list of children elements.

        Args:
            children: A list of Zenui Element objects.

        Returns:
            A combined string of the compiled HTML for all the children.
        """

        if not children:
            return

        parts = []
        for child in children:
            parts.append(self.compile(child, parent=False))  # Recursively compile each child

        return "".join(parts)