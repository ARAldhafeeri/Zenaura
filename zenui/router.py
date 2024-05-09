from dataclasses import dataclass
from typing import List
from zenui.zenui_dom import zenui_dom
from zenui.tags import Element
from pyscript import document, window

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

# router 

class Router:
    def __init__(self):
        # key -> path , value -> [comp, document.title]
        self.routes = {}
        self.paths = []
        window.onpopstate = self.handlelocation()

    def addRoute(self, route : Route) -> None:
        self.routes[route.path] = [route.comp, route.title]
        self.paths.append(route.path)

    def handlelocation(self) -> None:
        path = window.location.pathname
        if path in self.paths:
            [comp, title] = self.routes[path]
            zenui_dom.render(comp)
            return
        zenui_dom.render(notFound)


