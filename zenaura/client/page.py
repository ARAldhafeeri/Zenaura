import uuid 
import itertools
from .component import Component, UUIDManager
from typing import List


class Page:
    """
        a class representing a page in zenaura application
    """
    _page_count = itertools.count(0)

    def __init_subclass__(cls, **kwargs):
        cls.count = next(cls._component_count)
        cls.id = UUIDManager.generate_uuid(cls.__name__, cls.count)

    def __init__(self, children : List[Component]):
        self.children = children
        self.pageId = uuid.uuid4().hex
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")

        for child in self.children:
            if not isinstance(child, Component):
                raise TypeError("page children must be a Component")


    
        