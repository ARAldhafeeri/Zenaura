import uuid 
import itertools
from .component import Component, UUIDManager
from typing import List


class Page:
    """
        a class representing a page in zenaura application
    """
    _page_count = itertools.count(0)

    def __init__(self, children : List[Component]):
        self.count = next(self._page_count)
        self.id = UUIDManager.generate_uuid(self.__class__.__name__, self.count)
        self.children = children
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")

        for child in self.children:
            if not isinstance(child, Component):
                raise TypeError("page children must be a Component")


    
        