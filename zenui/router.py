from dataclasses import dataclass
from typing import List
from zenui.zenui_dom import zenui_dom
from zenui.tags import Element
from pyscript import document, window
from zenui.component import ZenUIComponent

class NotFound(ZenUIComponent):

    def element(self):
        em = Element("div")
        em.children.append(Element(name="text", children=["page not found"]))
        return em
    
notFound = NotFound()


class Route:
    def __init__(self, title, path, comp):
        self.title = title
        self.path = path
        self.comp = comp
        handler: Optional[Callable] = None  # For optional route-specific logic


# router 

class Router:
    def __init__(self):
        # key -> path , value -> [comp, document.title]
        self.routes = {}
        self.paths = []
        # Call handlelocation once to handle the initial route
        window.onpopstate = self.handlelocation

    def navigate(self, path) -> None:
        if path in self.paths:
            [comp, title] = self.routes[path]
            zenui_dom.mount(comp)  # Mount the component
            document.title = title  # Update the title
            window.history.pushState(path, title, path) # Update browser history 
        else:
            print("Invalid Path")  # Handle invalid path (optional)

    def handlelocation(self) -> None:
        path = window.location.pathname
        print(path, self.paths)
        if path in self.paths:
            [comp, title] = self.routes[path]
            zenui_dom.mount(comp)
            document.title = title
        else:
            zenui_dom.mount(notFound)

    def addRoute(self, route : Route) -> None:
        self.routes[route.path] = [route.comp, route.title]
        self.paths.append(route.path)