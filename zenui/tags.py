import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Child:
    def __init__(self,name, children=None, attributes=None):
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes

    
class Attribute:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Element:
    def __init__(self,name, children=None, attributes=None):
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes
        self.elementId = uuid.uuid4().hex
       

class Tags(Enum):
    BODY = "body"