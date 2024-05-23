from dataclasses import dataclass
from typing import List
from zenaura.client.dom import zenaura_dom
from zenaura.client.tags import Node
from zenaura.client.component import Component, Reuseable
from zenaura.client.page import Page
from zenaura.client.mocks import MockWindow, MockDocument
# this is really nothing just to be able to mock 
try :
    from pyscript import document, window
except ImportError:
    document = MockDocument() 
    window = MockWindow() 
    
from typing import Optional, Tuple, Callable, Dict, Any 
from collections import defaultdict

class HistoryNode:
    def __init__(self, page=None):
        self.page = page
        self.prev = None
        self.next = None 

class PageHistory:
    def __init__(self):
        self.current = HistoryNode()

    def visit(self, page : Page) -> None:
        new_page  =HistoryNode(page)
        new_page.prev = self.current
        self.current.next = new_page
        self.current = new_page

    def back(self) -> None:
        if self.current.prev:
            self.current = self.current.prev
        return self.current.page
    
    def forward(self) -> None:
        if self.current.next:
            self.current = self.current.next
        return self.current.page

@Reuseable
class NotFound(Component):
    """
    Represents a pageonent for displaying a "page not found" message.

    Methods
    -------
    node()
        Returns a Node representing the "page not found" message.
    """
    def node(self):
        em = Node("div")
        em.append_child(Node(name="text", children=["page not found"]))
        return em
    
notFound = NotFound()


class Route:
    """
        Represents a route configuration for the Router.
    """
    def __init__(self, title, path, page, middleware):
        """
        Initializes a Route with the specified title, path, and pageonent.
        Attributes
        ----------
        title : str
            The title of the route.
        path : str
            The path of the route.
        page : Page
            A page of pageonents.
        handler : Optional[Callable]
            Optional route-specific logic handler.
        """
        self.title = title
        self.path = path
        self.page = page

        if not isinstance(page, Page):
            raise TypeError("Only a Page can be mounted on a route")
        self.middleware: Optional[Callable] = middleware  # For optional route-specific logic


# router 

class Router:
    """
        Represents a router for managing routes and navigation.

        Methods
        -------
        __init__()
            Initializes the Router with empty routes and paths, and sets up the initial route handling.
        navigate(path)
            Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.
        handlelocation()
            Handles the current location by mounting the associated pageonent and updating the document title.
        addRoute(route)
            Adds a route to the router's configuration.

        Attributes
        ----------
        routes : dict
            A dictionary mapping paths to their associated pageonents and titles.
        paths : list
            A list of paths registered in the router.
    """
    def __init__(self):
        """
            Initializes the Router with empty routes and paths, and sets up the initial route handling.
        """
        # key -> path , value -> [page, document.title]
        self.routes = defaultdict(str)
        self.paths = []
        self.history = PageHistory()
        # Call handlelocation once to handle the initial route
        window.onpopstate = self.handlelocation
        # global middleware to run on routes

    def not_found(self):
        document.title = "Page Not Found"
        page = Page([notFound])
        zenaura_dom.mount(page)
        self.history.visit(page)

    def navigate(self, path) -> None:
        """
            Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.

            Parameters
            ----------
            path : str
                The path to navigate to.
        """
        matched_route, params = self._match_route(path) #TODO

        if not path in self.paths:
            self.not_found()
            return
        [_, _, middleware] = self.routes[path]
        # run middle ware #TODO test
        if callable(middleware):
            middleware()

        [page, title, middleware] = self.routes[path]
        zenaura_dom.mount(page)  # Mount the page on root container
        self.history.visit(page)
        document.title = title  # Update the title
        window.history.pushState(path, title, path) # Update browser history 

    def handlelocation(self) -> None:
        """
        Handles the current location by mounting the associated page and update title of document
        #TODO Handles wild card routes with params and queries.
        """
        path = window.location.pathname
        matched_route, params = self._match_route(path)
        if not matched_route:
            self.not_found()
            return
        [page, title, middleware] = self.routes[path] #TODO integrate params, props of new feature route wild card
        zenaura_dom.mount(page)
        self.history.visit(page)
        document.title = title

    def addRoute(self, route : Route) -> None:
        """
        Adds a route to the router's configuration.

        Parameters
        ----------
        route : Route
            The route to be added to the router's configuration.
        """
        self.routes[route.path] = [route.page, route.title, route.middleware]
        self.paths.append(route.path)
    
    def back(self) -> None:
        page = self.history.back()
        if self.history.current.page == page:
            return # do not mount new page
        zenaura_dom.mount(page) # else mount new page
    
    def forward(self) -> None:
        page = self.history.forward()
        if self.history.current.page == page:
            return # do not mount new page
        zenaura_dom.mount(page) # else mount new page

    def get_current_route(self) -> Optional[Tuple[Page, str]]:
            """Get the page and title of the current route, or None if not found."""
            path = window.location.pathname
            matched_route, info = self._match_route(path)
            return matched_route, info
    
    # TODO still needs a lot of work
    def _match_route(self, path: str) -> Tuple[Optional[Tuple[Page, str, Dict[str, Any]]], Dict[str, str]]:
        """Matches the given path to a registered route and extracts parameters."""
        for route_path, (page, title, props) in self.routes.items():
            if "*" in route_path:  # Wildcard route
                route_parts = route_path.split("*")
                if path.startswith(route_parts[0]):
                    params = path[len(route_parts[0]):]
                    query = defaultdict(str)
                    if "?" in params: # get all queries
                        newq = "".join(params).split("?")
                        params = newq[0]
                        newq = newq[1]
                        for q in newq.split("&"):
                            k,v = q.split("=")
                            query[k] = v
                    if "/" in params: # get all params
                        params = params.split("/")
                   
                    params = {"wildcard": {"params" : params, "query" : query} }

                    return (page, title, props), params
            elif ":" in route_path:  # Parameterized route
                route_parts = route_path.split("/")
                path_parts = path.split("/")
                if len(route_parts) == len(path_parts):
                    params = {}
                    for i, part in enumerate(route_parts):
                        if part.startswith(":"):
                            param_name = part[1:]
                            params[param_name] = path_parts[i]
                    return (page, title, props), params
            elif route_path == path:  # Exact match
                return (page, title, props), {}
        return None, {}  # No match found
        
    #TODO transition effects 