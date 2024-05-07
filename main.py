from zenui.component import ZenUIComponent
from dataclasses import dataclass
from typing import Optional
from zenui.tags import Element, Child

@dataclass
class CounterStyles:
	btn: str
	container: Optional[str] = None
	h1:  Optional[str] = None
	controls:  Optional[str] = None


a = CounterStyles(
	btn="test", 
    )
x = Element("test")
print(str(x))