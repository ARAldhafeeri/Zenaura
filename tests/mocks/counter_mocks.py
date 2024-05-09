from zenui.tags import Attribute, Element
from zenui.component import ZenUIComponent
from dataclasses import dataclass

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

class Counter(ZenUIComponent):
	def __init__(self, dependencies):			
		
		# set init state	 
		super().set_state(CounterState(
			count=0
		))

		# dependencies
		self.dependencies = dependencies

	def increment(self) -> None:
		self.set_state(CounterState(count=self.get_state().count + 1))

	def decrease(self) -> None:
		self.set_state(CounterState(count=self.get_state().count - 1))

	def create_button(self, label_text : str, onclick_handler : str) -> Element:
		btn = Element(name="button")
		btn.attributes.append(Attribute(key="onclick", value=onclick_handler))
		btn.attributes.append(Attribute(key="styles", value=BTN_STYLES.btn))	
		btn.children.append(Element(name="label", children=[label_text]))
		return btn
			 

	def element(self) -> Element:
		# header
		header =  Element(name="h1")
		header.attributes = [
			Attribute(key="styles", value=BTN_STYLES.h1)
		]
		header.children = [
			Element(name="text", children=[f"Counter: {self.get_state()}"])
		]

		#  btn controls

		incBtn = self.create_button( "Increase",  self.increment )

		decBtn = self.create_button( "Decrease", self.decrease )

		# controls div
		controls = 	Element(name="div")
		controls.attributes = [
			Attribute(key="styles", value=BTN_STYLES.controls)
		]
		controls.children = [
			decBtn,
			incBtn
		]

		# component
		comp = Element(name="div")

		comp.attributes = [
			Attribute(key="styles", value=BTN_STYLES.container)
		]
		comp.children = [
			header, 
			controls
		]

		return comp