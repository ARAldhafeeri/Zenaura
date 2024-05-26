from dataclasses import dataclass
from typing import List
from zenaura.client.dom import zenaura_dom
from zenaura.client.tags import Node
from zenaura.client.component import Component, Reuseable
from zenaura.client.page import Page
from zenaura.client.mocks import MockWindow, MockDocument
import asyncio
event_loop = asyncio.get_event_loop()

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
    Represents a page for displaying a "page not found" message.

    Methods
    -------
    render()
        Returns a Node representing the "page not found" message.
    """
    def render(self):
        em = Node("div")
        em.append_child(Node(name="text", children=["page not found"]))
        return em
    
notFound = NotFound()


class Route:
    """
        Represents a route configuration for the App.
    """
    def __init__(self, title, path, page, middleware=None, ssr=False):
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
        self.ssr=ssr

        if not isinstance(page, Page):
            raise TypeError("Only a Page can be mounted on a route")
        self.middleware: Optional[Callable] = middleware  # For optional route-specific logic


# router 

class App:
    """
        Represents a router for managing routes and navigation.

        Methods
        -------
        __init__()
            Initializes the App with empty routes and paths, and sets up the initial route handling.
        navigate(path)
            Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.
        handle_location()
            Handles the current location by mounting the associated pageonent and updating the document title.
        add_route(route)
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
            Initializes the App with empty routes and paths, and sets up the initial route handling.
        """
        # key -> path , value -> [page, document.title]
        self.routes = defaultdict(str)
        self.paths = []
        self.history = PageHistory()
        # Call handle_location once to handle the initial route
        window.onpopstate = event_loop.run_until_complete(self.handle_location())
        # global middleware to run on routes

    async def not_found(self):
        document.title = "Page Not Found"
        page = Page([notFound])
        await zenaura_dom.mount(page)
        self.history.visit(page)

    async def navigate(self, path) -> None:
        """
            Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.

            Parameters
            ----------
            path : str
                The path to navigate to.
        """
        if not path in self.paths:
            await self.not_found()
            return
        [_, _, middleware, _] = self.routes[path]
        # run middle ware #TODO test
        if callable(middleware):
            await middleware()
        

        [page, title, middleware, ssr] = self.routes[path]
        window.history.pushState(path, title, path) # Update browser history
        if not ssr: # ignore mount step for ssr
            await zenaura_dom.mount(page)  # Mount the page on root container
        self.history.visit(page)
        document.title = title  # Update the title

    async def handle_location(self) -> None:
        """
        Handles the current location by mounting the associated page and update title of document
        """
        path = window.location.pathname
        matched_route, params = self._match_route(path)
        print(f"Updated browser history with path: {path}")
        if not matched_route:
            await self.not_found()
            return
        [page, title, middleware, ssr] = self.routes[path]
        window.history.pushState(path, title, path) # Update browser history
        if callable(middleware):
            await middleware()
        if not ssr: # ignore mount for ssr 
            await zenaura_dom.mount(page)
        self.history.visit(page)
        document.title = title




    def add_route(self, route : Route) -> None:
        """
        Adds a route to the router's configuration.

        Parameters
        ----------
        route : Route
            The route to be added to the router's configuration.
        """
        self.routes[route.path] = [route.page, route.title, route.middleware, route.ssr]
        self.paths.append(route.path)
    
    async def back(self) -> None:
        page = self.history.back()
        if self.history.current.page == page:
            return # do not mount new page
        await zenaura_dom.mount(page) # else mount new page
    
    async def forward(self) -> None:
        page = self.history.forward()
        if self.history.current.page == page:
            return # do not mount new page
        await zenaura_dom.mount(page) # else mount new page

    def get_current_route(self) -> Optional[Tuple[Page, str]]:
            """Get the page and title of the current route, or None if not found."""
            path = window.location.pathname
            matched_route, info = self._match_route(path)
            return matched_route, info
    
    # TODO still needs a lot of work
    def _match_route(self, path: str) -> Tuple[Optional[Tuple[Page, str, Dict[str, Any]]], Dict[str, str]]:
        """Matches the given path to a registered route and extracts parameters."""
        for route_path, (page, title, middleware, ssr) in self.routes.items():
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

                    return (page, title, middleware, ssr), params
            elif ":" in route_path:  # Parameterized route
                route_parts = route_path.split("/")
                path_parts = path.split("/")
                if len(route_parts) == len(path_parts):
                    params = {}
                    for i, part in enumerate(route_parts):
                        if part.startswith(":"):
                            param_name = part[1:]
                            params[param_name] = path_parts[i]
                    return (page, title, middleware, ssr), params
            elif route_path == path:  # Exact match
                return (page, title, middleware, ssr), {}
        return None, {}  # No match found
        
    #TODO transition effects 