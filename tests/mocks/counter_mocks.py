from zenaura.client.tags import Attribute, Node, Data
from zenaura.client.component import Component
from dataclasses import dataclass
from zenaura.client.mutator import mutator
@dataclass
class CounterState:
	count: int
@dataclass
class CounterStyles:
	btn: str
	container: str
	h1: str
	controls: str


BTN_STYLES = CounterStyles(
	btn="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded", 
	h1="self-center text-xl font-semibold whitespace-nowrap dark:text-white",
	container= "flex flex-col",
	controls = "flex flex-row",
)

class Counter(Component):
	def __init__(self, dependencies):			
		
		# set init state	 
		super().set_state(CounterState(
			count=0
		))

		# dependencies
		self.dependencies = dependencies

	@mutator
	async def increment(self) -> None:
		self.set_state(CounterState(count=self.get_state().count + 1))

	@mutator
	async def decrease(self) -> None:
		self.set_state(CounterState(count=self.get_state().count - 1))

	def create_button(self, label_text : str, onclick_handler : str) -> Node:
		btn = Node(name="button")
		btn.attributes.append(Attribute(key="onclick", value=onclick_handler))
		btn.attributes.append(Attribute(key="styles", value=BTN_STYLES.btn))	
		btn.append_child(Node(name="label", children=[Node(text=label_text)]))
		return btn
			 

	def node(self) -> Node:
		# header
		header =  Node(name="h1")
		header.attributes = [
			Attribute(key="styles", value=BTN_STYLES.h1)
		]
		header.children = [
			Node(name="text", children=[
				Node(name="data", children= [
					Node(text=f"Counter: {self.get_state()}")
				])
			])
		]

		#  btn controls

		incBtn = self.create_button( "Increase",  self.increment )

		decBtn = self.create_button( "Decrease", self.decrease )

		# controls div
		controls = 	Node(name="div")
		controls.attributes = [
			Attribute(key="styles", value=BTN_STYLES.controls)
		]
		controls.children = [
			decBtn,
			incBtn
		]

		# component
		comp = Node(name="div")

		comp.attributes = [
			Attribute(key="styles", value=BTN_STYLES.container)
		]
		comp.children = [
			header, 
			controls
		]

		return comp