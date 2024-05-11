from zenaura.component import Component
from dataclasses import dataclass
from typing import Optional
from zenaura.tags import Node, Attribute
from zenaura.router import Router, Route

class SimpleUi(Component):
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
print(zenaura_dom.zen_dom_table)
print(simpleUi.set_state("koko2"))
print(zenaura_dom.zen_dom_table)

app = ZenUIApp(router)

