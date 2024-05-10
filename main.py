from zenui.component import ZenUIComponent
from dataclasses import dataclass
from typing import Optional
from zenui.tags import Node, Attribute
from zenui.router import Router, Route

class SimpleUi(ZenUIComponent):
    def node(self):
        div = Node(name="div")
        div.attributes = [Attribute(key="test", value="test")]
        div.children.append(Node(name="text", children=["test"]))
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

print(simpleUi.componentId)
simpleUi.set_state("koko")
print(simpleUi.get_state())
print(zenui_dom.zen_dom_table)
print(simpleUi.set_state("koko2"))
print(zenui_dom.zen_dom_table)

app = ZenUIApp(router)

