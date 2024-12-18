from dataclasses import dataclass
from typing import List
from zenaura.client.dom import zenaura_dom
from zenaura.client.tags import Node
from zenaura.client.component import Component, Reuseable
from zenaura.client.page import Page
from zenaura.client.hydrator import HydratorRealDomAdapter
from zenaura.client.layout import Layout
from zenaura.web.utils import document, window
from zenaura.client.dispatcher import dispatcher
rdom_hyd = HydratorRealDomAdapter() 

    
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
        middleware : Optional[Callable]
            Optional route-specific logic handler.
        ssr : bool
            Whether the route is server-side rendered.
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

    This class provides methods for adding routes, navigating between pages, and handling the current location.

    Attributes:
        routes (dict): A dictionary mapping paths to their associated pages and titles.
        paths (list): A list of paths registered in the router.
        history (PageHistory): An object that manages the history of visited pages.

    Methods:
        __init__()
            Initializes the App with empty routes and paths, and sets up the initial route handling.
        navigate(path)
            Navigates to the specified path by mounting the associated page and updating the document title and browser history.
        handle_location()
            Handles the current location by mounting the associated page and updating the document title.
        add_route(route)
            Adds a route to the router's configuration.
        back()
            Navigates back to the previous Page in the history stack.
        forward()
            Navigates forward to the next Page in the history stack.
        get_current_route()
            Get the page and title of the current route, or None if not found.
    """
    def __init__(self, layout=None):
        """
            Initializes the App with empty routes and paths, and sets up the initial route handling.
        """
        # key -> path , value -> [page, document.title]
        self.routes = defaultdict(str)
        self.paths = []
        self.history = PageHistory()
        self._layout = layout

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, new_layout):
        self._layout = new_layout 

    async def not_found(self):
        document.title = "Page Not Found"
        page = Page([notFound])
        await zenaura_dom.mount(page)
        self.history.visit(page)

    async def mount_layout(self) -> None:
        """
            Trigger mount method for layout components if layout is defined
        """
        if self._layout:
            # mount  global components 
            comps = self._layout.top + self._layout.bottom
            for comp in comps:
                if hasattr(comp, "attached"):
                    await comp.attached()
            

    async def navigate(self, path) -> None:
        """
        Navigates to the specified path by mounting the associated pageonent and updating the document title and browser history.

        Parameters
        ----------
        path : str
            The path to navigate to.
        """
        # handle route
        matched_route, params = self._match_route(path)
        if not matched_route:
            await self.not_found()
            return
        
        [page, title, middleware, ssr] = matched_route

        if callable(middleware):
            middleware()

        if ssr:  # Ignore mount step for server side rendering pages.
            await zenaura_dom.mount(page)
            self.history.visit(page)
            document.title = title
            return

        if not self.history.current.page:  # self.history.current is initially None
            pass
        else:
            self.hyd_rdom_toggle_pages_visibilty(self.history.current.page, page)
        
        window.history.pushState(path, title, path)  # Update browser history

        # trigger layout components mount if layout is defined, after 
        # the reason after pushState, middleware
        # global components may be be coupled to a state of route path or middleware
        await self.mount_layout()
        # mount page
        await zenaura_dom.mount(page)
        self.history.visit(page)
        document.title = title

    def run(self):
        """
            facade interface mounts the app on "/" location
            e.g. 
            app = App()
            app.add_route(
                Route(
                    "Home", 
                    "/",
                    Page(
                        [counter1, counter2, counter3, counter4]
                ) 
                )
            )
            app.run()

        """
        dispatcher.dispatch(self.handle_location)

    def hyd_rdom_toggle_pages_visibilty(self, previous_page: Page, current_page: Page):
        p_page = document.querySelector(f'[data-zenaura="{previous_page.id}"]')
        if p_page:
            p_page.hidden = True  # Hide the previous page
        curr_page = document.querySelector(f'[data-zenaura="{current_page.id}"]')
        if curr_page:
            curr_page.hidden = False  # Show the current page

    async def handle_location(self) -> None:
        """
        Handles the current location by mounting the associated page and updating the document title.
        """
        # handle home route
        path = window.location.pathname
        matched_route, params = self._match_route(path)
        if not matched_route:
            await self.not_found()
            return
        [page, title, middleware, ssr] = self.routes[path]
        window.history.pushState(path, title, path)  # Update browser history

        if callable(middleware):
            middleware()

        # trigger layout components mount if layout is defined, after 
        # the reason after pushState, middleware
        # global components may be be coupled to a state of route path or middleware
        await self.mount_layout()
        if ssr:  # Ignore mount step for server side rendering pages.
            await zenaura_dom.mount(page)
            self.history.visit(page)
            document.title = title
            return
        if not self.history.current.page:  # self.history.current is initially None
           pass
        else:
            self.hyd_rdom_toggle_pages_visibilty(self.history.current.page, page)
        
        # visit page
        self.history.visit(page)
        await zenaura_dom.mount(page)  # Trigger attached lifecycle for each component within the page.


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
        """
        Navigates back to the previous Page in the history stack.
        """
        previous_page = self.history.current.page
        curr_page = self.history.back()
        rdom_hyd.hyd_rdom_toggle_pages_visibilty(previous_page, curr_page)
        await zenaura_dom.mount(curr_page)  # trigger attached lifecycle for each component within the page.

    
    async def forward(self) -> None:
        """
        Navigates forward to the next Page in the history stack.
        """
        previous_page = self.history.current.page
        curr_page = self.history.forward()
        rdom_hyd.hyd_rdom_toggle_pages_visibilty(previous_page, curr_page)
        await zenaura_dom.mount(curr_page)  # trigger attached lifecycle for each component within the page.
     

    def get_current_route(self) -> Optional[Tuple[Page, str]]:
        """
        Get the page and title of the current route, or None if not found.
        """
        path = window.location.pathname
        matched_route, info = self._match_route(path)
        return matched_route, info
    
    # TODO still needs a lot of work
    def _match_route(self, path: str) -> Tuple[Optional[Tuple[Page, str, Dict[str, Any]]], Dict[str, str]]:
        """
        Matches the given path to a registered route and extracts parameters.

        Args:
            path (str): The path to match.

        Returns:
            Tuple[Optional[Tuple[Page, str, Dict[str, Any]]], Dict[str, str]]:
                A tuple containing the matched route information (if any) and extracted parameters.
        """
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