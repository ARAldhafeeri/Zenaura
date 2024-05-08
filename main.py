from zenui.component import ZenUIComponent
from dataclasses import dataclass
from typing import Optional
from zenui.tags import Element, Attribute
from zenui.router import Router, Route

from pyscript import document, display
from js import console

class SimpleUi(ZenUIComponent):
    def element(self):
        div = Element(name="div")
        div.attributes = [Attribute(key="test", value="test")]
        div.children.append(Element(name="text", children=["test"]))
        return div

simpleUi = SimpleUi()

router = Router()

router.addRoute(
    Route(
        title="test",
        path="/",
        comp=simpleUi
    )
)

router.handlelocation()

console.log("routes", f"{router.paths}", )

app = ZenUIApp(router)
