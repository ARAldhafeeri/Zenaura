from dataclasses import dataclass
from typing import List
from zenaura.client.dom import zenaura_dom
from zenaura.client.tags import Node
from zenaura.client.component import Component
from zenaura.client.page import Page
# this is really nothing just to be able to mock 
from pyscript import document, window

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
        em.children.append(Node(name="text", children=["page not found"]))
        return em
    
notFound = NotFound()


class Route:
    """
        Represents a route configuration for the Router.
    """
    def __init__(self, title, path, page):
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
        handler: Optional[Callable] = None  # For optional route-specific logic


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

    def navigate(self, path) -> None:
        """
            Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.

            Parameters
            ----------
            path : str
                The path to navigate to.
        """
        if path in self.paths:
            [page, title] = self.routes[path]
            zenaura_dom.mount(page)  # Mount the page on root container
            document.title = title  # Update the title
            window.history.pushState(path, title, path) # Update browser history 
        else:
            print("Invalid Path")  # Handle invalid path (optional)

    def handlelocation(self) -> None:
        """
        Handles the current location by mounting the associated page and update title of document
        """
        path = window.location.pathname
        if path in self.paths:
            [page, title] = self.routes[path]
            zenaura_dom.mount(page)
            document.title = title
        else:
            zenaura_dom.mount([notFound])

    def addRoute(self, route : Route) -> None:
        """
        Adds a route to the router's configuration.

        Parameters
        ----------
        route : Route
            The route to be added to the router's configuration.
        """
        self.routes[route.path] = [route.page, route.title]
        self.paths.append(route.path)