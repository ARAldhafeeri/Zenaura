from dataclasses import dataclass, field
from typing import List, Optional

from enum import Enum

@dataclass
class Child:
    name: str
    children : any
    attributes: any
    def __repr__(self) -> str:
        return 'Child'
    
@dataclass
class Attribute:
    key : any
    value: any

    def __repr__(self) -> str:
        return 'Attribute'

@dataclass
class Element:
    name: str = field(default="div")
    children : List[Child] = field(default_factory= lambda : [])
    attributes : List[Attribute] = field(default_factory= lambda : [])

    def __repr__(self) -> str:
        return 'Element'

class Tags(Enum):
    BODY = "body"