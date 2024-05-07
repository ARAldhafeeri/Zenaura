from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Child:
    name: str
    children : any
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
    name: str
    children : Optional[List[Child |Attribute]] = None

    def __repr__(self) -> str:
        return 'Element'
