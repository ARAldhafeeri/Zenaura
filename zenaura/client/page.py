from .component import Component, UUIDManager
from typing import List
import uuid 

class Page:
    """
        a class representing a page in zenaura application
    """
    def __init_subclass__(cls):
        """
        Initialize a new subclass of Page.

        This method generates a unique id for each subclass using uuid.

        Args:
        cls: The subclass being initialized.

        Returns:
        None
        """

        super().__init_subclass__()
        UUIDManager.persist_uuid(cls)

    def __init__(self, children : List[Component]):
        self.children = children
        self.pageId = uuid.uuid4().hex
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")

        for child in self.children:
            if not isinstance(child, Component):
                raise TypeError("page children must be a Component")


    
        