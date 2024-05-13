from zenaura.client.component import Component
from zenaura.client.tags import Node, Attribute
from zenaura.client.router import Route, Router
from zenaura.client.app import ZenUIApp
from zenaura.client.dom import zenaura_dom
from zenaura.routes import ClientRoutes
from dataclasses import dataclass
from pyscript import window
from functools import cache
import json

@dataclass
class CounterState:
	count: int
@dataclass
class CounterStyles:
    btn: str
    container: str
    container2: str
    h1: str
    controls: str
    main_container: str



                
STYLES = CounterStyles(
	btn="button-13", 
	h1="self-center text-xl font-semibold whitespace-nowrap dark:text-white",
	container= "card",
	controls = "flex flex-row",
    container2="logoContainer",
    main_container="mainContainer"
)

@cache
def Button( label_text : str, onclick_handler : str) -> Node:
    btn = Node(name="button")
    btn.attributes.append(Attribute(key="py-click", value=onclick_handler))
    btn.attributes.append(Attribute(key="styles", value=STYLES.btn))	
    btn.children.append(Node(name="label", children=[label_text]))
    return btn

@cache
def DomContainer() -> Node:
    virtualDom = Node(name="div")
    virtualDom.attributes = [
        Attribute(key="id", value="virtualDom"),
    ]

    realDom = Node(name="div")
    realDom.attributes = [
        Attribute(key="id", value="realDom"),
    ]

    domContainer = Node(name="div")
    domContainer.attributes = [
        Attribute(key="styles", value=f"domContainer"),
    ]

    domContainer.children = [
        virtualDom,
        realDom,
    ]
    return domContainer

@cache
def Image(src : str) -> Node:
     return Node(name="img", attributes=[Attribute(key="src", value=src)])

class SimpleUi(Component):
	
    def nvaigate(self, event):
   
        router.navigate("/counter")
		
    def node(self):
        div = Node(name="div")
        btn = Node(name="button", children=["test"])
        btn.attributes = [
            Attribute("py-click", "simpleUi.nvaigate"),
            Attribute("styles", STYLES.btn),
            Attribute("id", "centered"),
        ]
        div.children.append(btn)
        return div

class Counter(Component):
    def __init__(self, dependencies):			
        
        # set init state	 
        super().set_state({
             "count1": 0,
             "count2": 0
        })

        # dependencies
        self.dependencies = dependencies
        self.state_chnages = []

    def treeGraph(self):
        import js
        s = json.dumps(self.node().to_dict())
        js.window.VirtualDomGraph(s)

        
    def componentDidMount(self, *args , **kwargs):
        self.treeGraph()

    def componentDidUpdate(self, *args, **kwargs):
        self.state_chnages.append(self.get_state())
        self.treeGraph()
        
    def increment(self, event) -> None:
        state = self.get_state()
        state["count1"] = state["count1"] + 1
        self.set_state(state)
        zenaura_dom.render(self)

    def decrease(self, event) -> None:
        state = self.get_state()
        state["count1"] = state["count1"] - 1
        self.set_state(state)
        zenaura_dom.render(self)

    def increment2(self, event) -> None:
        state = self.get_state()
        state["count2"] = state["count2"] + 1
        self.set_state(state)
        zenaura_dom.render(self)

    def decrease2(self, event) -> None:
        state = self.get_state()
        state["count2"] = state["count2"] - 1
        self.set_state(state)
        zenaura_dom.render(self)


    def node(self) -> Node:
        # header
        header =  Node(name="h1")
        header2 =  Node(name="h2")

        header.attributes = [
            Attribute(key="styles", value=STYLES.h1)
        ]
        header.children = [
            Node(name="data", children=[f"Counter: {self.get_state()['count1']}"])
        ]

        header2.attributes = [
            Attribute(key="styles", value=STYLES.h1)
        ]
        header2.children = [
            Node(name="data", children=[f"Counter: {self.get_state()['count2']}"])
        ]



        # controls div
        controls1 = 	Node(name="div")
        controls1.attributes = [
            Attribute(key="styles", value=STYLES.controls)
        ]
        controls1.children = [
            Button( "-",  "counter.decrease" ),
            Button( "+",  "counter.increment" ),
        ]

        # controls div
        controls2 = 	Node(name="div")
        controls2.attributes = [
            Attribute(key="styles", value=STYLES.controls)
        ]
        controls2.children = [
            Button( "-",  "counter.decrease2" ),
            Button( "+",  "counter.increment2" ),
        ]

        # logo 
        logoContainer = Node(name="div")
        logoContainer.attributes = [
            Attribute(key="styles", value=STYLES.container2)
        ]

        logoContainer.children = [
             Image("./zenaura/assets/logo.png"),
        ]

        container = Node(name="div")
        container.attributes = [
            Attribute(key="styles", value=f"${STYLES.main_container} large-header"),
        ]
        # component
        comp = Node(name="div")

        comp.attributes = [
            Attribute(key="styles", value=STYLES.container),
            Attribute(key="id", value="large-header")
        ]

        table = Node(name="div")
        # table for state_change 
        
        for state in self.state_chnages:
            table.children.append(Node(name="p", children=[f"count: {state['count1']} {state['count2']}"]))
        
        table_and_graph = Node(name="div")
        table_and_graph.attributes = [
            Attribute(key="id", value="table_and_graph")
        ]
        table_and_graph.children = [
            DomContainer(),
            table,
        ]
       

        comp.children = [
            header, 
            controls1,
            header2,
            controls2,
        ]

        container.children = [
            logoContainer,
            comp,
            table_and_graph,

        ]

        return container


simpleUi = SimpleUi()

counter = Counter([])
# print(counter.node().to_dict())
router = Router()

router.addRoute(Route(
        title="test",
        path=ClientRoutes.home.value,
        comp=simpleUi
    ))

router.addRoute(Route(
		title="counter",
		path=ClientRoutes.counter.value,
		comp=counter
    ))
 
router.handlelocation()



app = ZenUIApp(router)


