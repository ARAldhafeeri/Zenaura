from dataclasses import dataclass
from typing import List
from zenaura.client.dom import zenaura_dom
from zenaura.client.tags import Node
from zenaura.client.component import Component
from zenaura.client.page import Page
# this is really nothing just to be able to mock 
from pyscript import document, window
from typing import Optional, Tuple, Callable, Dict, Any 

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
        self.routes = {}
        self.paths = []
        # Call handlelocation once to handle the initial route
        window.onpopstate = self.handlelocation
        # global middleware to run on routes

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
            zenaura_dom.mount(self.notFoundComponent)
            document.title = "Page Not Found"
            zenaura_dom.mount([notFound])
            return
        [_, _, middleware] = self.routes[path]
        # run middle ware #TODO test
        middleware()

        [page, title] = self.routes[path]
        zenaura_dom.mount(page)  # Mount the page on root container
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
            # Handle 404
            zenaura_dom.mount(self.notFoundComponent)
            document.title = "Page Not Found"
            zenaura_dom.mount([notFound])
            return
        [page, title] = self.routes[path] #TODO integrate params, props of new feature route wild card
        zenaura_dom.mount(page)
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

    def get_current_route(self) -> Optional[Tuple[Page, str]]:
            """Get the page and title of the current route, or None if not found."""
            path = window.location.pathname
            return self.routes.get(path, None) 
    
    def _match_route(self, path: str) -> Tuple[Optional[Tuple[Page, str, Dict[str, Any]]], Dict[str, str]]:
        """Matches the given path to a registered route and extracts parameters."""
        for route_path, (component, title, props) in self.routes.items():
            if "*" in route_path:  # Wildcard route
                route_parts = route_path.split("*")
                if path.startswith(route_parts[0]) and path.endswith(route_parts[1]):
                    params = {"wildcard": path[len(route_parts[0]):-len(route_parts[1])]}
                    return (component, title, props), params
            elif ":" in route_path:  # Parameterized route
                route_parts = route_path.split("/")
                path_parts = path.split("/")
                if len(route_parts) == len(path_parts):
                    params = {}
                    for i, part in enumerate(route_parts):
                        if part.startswith(":"):
                            param_name = part[1:]
                            params[param_name] = path_parts[i]
                    return (component, title, props), params
            elif route_path == path:  # Exact match
                return (component, title, props), {}
        return None, {}  # No match found
    
    #TODO transition effects 