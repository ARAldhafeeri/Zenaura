# ZenUI 

ZenUI is mini, light weight, super fast python framework that brings python zen into the UI world. Build scalable, stateful component-based, interactive SPA with nothing but TailwindCSS and pure Python, no HTML, no CSS, no JS, but you could use js, css, html if you want !

## Quick Example : 

```Python
from zenui.tags import Attribute, Element
from zenui.component import ZenUIComponent

class CounterState:
	def __init__(self,count):
		self.count = count

class CounterStyles:
	def __init__(self, btn, container, h1, controls):
	self.btn= str
	self.container = container
	self.h1 = h1
	self.controls = controls


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

	def increment(self):
		self.set_state(CounterState(count=self.get_state().count + 1))

	def decrease(self):
		self.set_state(CounterState(count=self.get_state().count - 1))

	def create_button(self, label_text, onclick_handler):
		btn = Element(name="button")
		btn.attributes.append(Attribute(key="onclick", value=onclick_handler))
		btn.attributes.append(Attribute(key="styles", value=BTN_STYLES.btn))	
		btn.children.append(Element(name="label", children=[label_text]))
		return btn
			 

	def element(self):
		# header
		header =  Element(name="h1")
		header.attributes.append(Attribute(key="styles", value=BTN_STYLES.h1))
		header.children.append(Element(name="text", children=[f"Counter: {self.get_state()}"]))

		#  btn controls

		incBtn = self.create_button(
			"Increase", 
			self.increment, 
		)

		decBtn = self.create_button(
			"Decrease", 
			self.decrease, 
		)

		# controls div
		controls = 	Element(name="div")
		controls.attributes.append(
			Attribute(key="styles", value=BTN_STYLES.controls)
		)
		controls.children.append(decBtn)
		controls.children.append(incBtn)

		# component
		comp = Element(name="div")

		comp.attributes.append(Attribute(key="styles", value=BTN_STYLES.container))
		comp.children.append(header)
		comp.children.append(controls)

		return comp	    
```
