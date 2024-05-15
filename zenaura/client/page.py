from .component import Component
from typing import List
import uuid 

class Page:
    """
        a class representing a page in zenaura application
    """
    def __init__(self, children : List[Component]):
        self.children = children
        self.pageId = uuid.uuid4().hex
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")

        for child in self.children:
            if not isinstance(child, Component):
                raise TypeError("page children must be a Component")


    
        