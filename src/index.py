
# tags
from typing import List, Optional
import random
import time

def generate_simple_uuid():
    random_part = hex(random.getrandbits(128))[2:]  # 128-bit random number
    timestamp_part = hex(int(time.time()))[2:]
    return f'{timestamp_part}-{random_part}' 

class Child:
    def __init__(self, name, children=[], attributes=[]):
        self.name = name
        self.children = children
        self.attributes = attributes

    def __repr__(self) -> str:
        return f"Child(name={self.name})" 

class Attribute:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self) -> str:
        return f"Attribute({self.key}={self.value})"

class Element:
    def __init__(self, name="div", children=[], attributes=[]):
        self.name = name
        self.children = children
        self.attributes = attributes

    def __repr__(self) -> str:
        return 'Element'


# compiler 

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

# dom 
    

compiler = ZenuiCompiler()

class ZenUIDom:

    def __init__(self):
        self.curr_mounted_element = None


    def render(self, comp ) -> None:
        """
            recieve instance of ZenUIComponent child, rerender it.
        """
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
            componentId=comp.componentId
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById(comp.id).innerHTML = compiled_comp
        self.dom_comp_update(comp)

    
    def mount(self, comp) -> None:
        comp_element_handler = comp.element 
        comp_tree = comp.element()
        compiled_comp = compiler.compile(
            comp_tree, 
            componentName=comp.__class__.__name__, 
            componentId=comp.componentId
        )
        # this line might be confusing
        # but transcrypt allows using js & python code
        # then the library compiles to js.
        document.getElementById("root").innerHTML = compiled_comp
        # update zenui dom lookup for re-rendering
        self.curr_mounted_element = comp

zenui_dom = ZenUIDom()


# component 


class ZenUIComponent:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.componentId = generate_simple_uuid()
    global_state = {}

    
    # Initialize an internal (private) dictionary to store component state
    _state = {}  
        
    @property
    def state(self): 
        return self.get_state()

    @state.setter
    def value(self, value):
        self.set_state(value)
        #  re-render call Comp.element(self, self.get_state)
        zenui_dom.render(zenui_dom.curr_mounted_element)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state  # Update the internal state
    
    def element():
        pass

notFound = Element("div", children=["page not found"])


class Route:
    def __init__(self, title, path, comp):
        self.title = title
        self.path = path
        self.comp = comp

# router 

class Router:
    def __init__(self):
        # key -> path , value -> [comp, document.title]
        self.routes : List[Route] =  []
        self.paths = []
        window.onpopstate = self.handlelocation()

    def addRoute(self, route : Route) -> None:
        self.routes.append(route)
        self.paths.append(route.path)

    def handlelocation(self) -> None:
        path = window.location.pathname
        if path in self.paths:
            comp = self.routes[path]
            zenui_dom.mount(comp)
            return
        zenui_dom.mount(notFound)
# app 
class ZenUIApp(ZenUIComponent):
    def __init__(self, router: Router):
        super().__init__()
        self.router = router
