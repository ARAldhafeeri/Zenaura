import itertools
from .component import Component, UUIDManager
from typing import List, Dict


class Page:
    """
    Represents a page in a Zenaura application.

    A Page is a container for components that are displayed together. It manages the
    lifecycle of its child components and handles rendering them to the DOM.

    Attributes:
        count (int): A unique identifier for the page.
        id (str): A unique UUID for the page.
        children (List[Component]): The list of components that belong to this page.

    Raises:
        TypeError: If `children` is not a list or if any child is not a `Component`.
    """

    _page_count = itertools.count(0)

    def __init__(self, children: List[Component], attributes: Dict = None):
        """
        Initializes a new Page instance.

        Args:
            children (List[Component]): The list of components to be added to the page.
            attributes Dict : list of attributes for the page wrapper div
        """

        self.count = next(self._page_count)
        self.id = UUIDManager.generate_uuid(self.__class__.__name__, self.count)
        self.children = children
        self.attributes ={} if not attributes else attributes

        if not isinstance(self.children, list):
            raise TypeError("children must be a list")

        for child in self.children:
            if not isinstance(child, Component):
                raise TypeError("page children must be a Component")
