from zenaura.client.component import Component
from zenaura.client.tags import Node, Attribute, Data
from zenaura.client.router import Route, Router
from zenaura.routes import ClientRoutes
from dataclasses import dataclass
from pyscript import window, when
from functools import cache
from zenaura.client.mutator import mutator
from zenaura.client.tags import Builder
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

def Button( label_text : str, onclick_handler : str, id=None) -> Node:
    btn = Node(name="button")
    btn.attributes.append(Attribute(key="styles", value=STYLES.btn))
    if id:
        btn.attributes.append(Attribute(key="id", value=id))
    else:
        btn.attributes.append(Attribute(key="py-click", value=onclick_handler))

    btn.children.append(Node(name="label", children=[label_text]))
    return btn

def DomContainer() -> Node:
    virtualDom = Node(name="div")
    virtualDom.attributes = [
        Attribute(key="id", value="virtualDom"),
    ]

    virtualDom.children = [
        Node(name="svg")
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



def CounterPresntaional(increaseBtn, decreaseBtn, headertext) -> Node:
    
    header = Builder('h1') \
    .with_child(
        headertext
    ).build()
    
    ctrl = Builder("div") \
        .with_attribute("styles", STYLES.controls) \
        .with_child(
            increaseBtn
        ).with_child(
            decreaseBtn
        ).build()

    return Builder("div") \
        .with_attribute("styles", STYLES.container) \
        .with_attribute("id", "large-header") \
        .with_child(
            header 
        ).with_child(
            ctrl
    ).build()

class Counter(Component):
    def __init__(self, dependencies):			
        
        # set init state	 
        super().set_state({
             "count1": 0,
             "count2": 0
        })
        
        self.count1 = self.get_state()['count1']

        # dependencies
        self.dependencies = dependencies
        self.state_chnages = []

    # def treeGraph(self):
    #     import js
    #     s = json.dumps(self.node().to_dict())
    #     js.window.VirtualDomGraph(s)

        
    # def componentDidMount(self, *args , **kwargs):
    #     self.treeGraph()

    # def componentDidUpdate(self, *args, **kwargs):
    #     self.state_chnages.append(self.get_state())
    #     self.treeGraph()

    @mutator        
    def increment(self, event) -> None:
        state = self.get_state()
        print("increment", state)
        state["count1"] = state["count1"] + 1
        self.set_state(state)

    @mutator        
    def decrease(self, event) -> None:
        state = self.get_state()
        state["count1"] = state["count1"] - 1
        self.set_state(state)

    @mutator        
    def increment2(self, event) -> None:
        state = self.get_state()
        print("increment", state)
        state["count2"] = state["count2"] + 1
        self.set_state(state)

    @mutator        
    def decrease2(self, event) -> None:
        state = self.get_state()
        state["count2"] = state["count2"] - 1
        self.set_state(state)


    def node(self) -> Node:
    
        # table = Node(name="div")
        # # table for state_change 
        
        # for state in self.state_chnages:
        #     table.children.append(f"count: {state['count1']} {state['count2']}")
        
        # table_and_graph = Node(name="div")
        # table_and_graph.attributes = [
        #     Attribute(key="id", value="table_and_graph")
        # ]
        
        # table_and_graph.children = [
        #     DomContainer(),
        #     table,
        # ]
       

        return Builder("div") \
            .with_attribute("styles", f"{STYLES.main_container} large-header") \
                .with_child(
                    Builder("div")
                    .with_child(Image("./zenaura/assets/logo.png"))
                    .with_attribute("styles", STYLES.container2)
                    .build()
                ) \
                .with_child(
                    CounterPresntaional(
                        Button("-", "counter.decrease"),
                        Button("+", "counter.increment"),
                        f"count: {self.get_state()['count1']}"
                    )
                ) \
                .with_child(
                    CounterPresntaional(
                        Button("-", "counter.decrease2"),
                        Button("+", "counter.increment2"),
                        f"count: {self.get_state()['count2']}"
                    )
                ) \
                .build()




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



