from .component import Component
from .page import Page
from typing import List, Dict, Any

class Layout:
    """
    Represents a layout in a Zenaura application.

    A Layout is a container for components, app routes. It is abstraction
    that handle the need for needing global components on app level such as nav bars, footers
    and others.
    """

    def __init__(self, top: List[Component], routes: List[Any], bottom: List[Component]):
        """
        Initializes a new Page instance.

        Args:
            top : list of component first children of root div
            routes: list of routes
            bottom: list of component bttom children after page rendering.
        """

        self.top = top
        self.routes = routes
        self.bottom = bottom

        if not isinstance(self.top, list):
            raise TypeError("top must be a list of components for root div first children")

        if not isinstance(self.bottom, list):
            raise TypeError("bottom must be a list of components for root div bottom children")

        if not isinstance(self.routes, dict):
            raise TypeError("routes should be a App.routes")

        for comp in self.top:
            if not isinstance(comp, Component):
                raise TypeError("every element in top must be instace of zenaura Component")
        
        for comp in self.bottom:
            if not isinstance(comp, Component):
                raise TypeError("every element in bottom must be instace of zenaura Component")
    
