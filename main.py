from zenui.component import ZenUIComponent
from dataclasses import dataclass
from typing import Optional
from zenui.tags import Element, Attribute
from zenui.router import Router, Route


class SimpleUi(ZenUIComponent):
    def element():
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

print("routes", f"{router.routes[0]}")

app = ZenUIApp(router)
