from dataclasses import dataclass
from typing import List
from zenui_dom import zenui_dom
from zenui.tags import Element

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
            zenui_dom.render(comp)
            return
        zenui_dom.render(notFound)



