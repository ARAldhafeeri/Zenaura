# ZenUI 

ZenUI is python framework that brings python zen into the UI world. Build scalable, stateful component-based, interactive SPA with nothing but TailwindCSS and pure Python, no HTML, no CSS, no JS. 

## Quick Example : 

```Python

from ZenUI import ZenUIComponent
from ZenUI.tags import, Attribute, div, h1, button
# from typing import List, Dict, ClassVar

@dataclass
class CounterState:
	count: str
@dataclass
class CounterStyles:
	btn: str
	container: str
	h1: str
	controls: str

from ZenUI import Component

class Counter(ZenUIComponent):
	def __init__(self, dependencies):
		super().__init__(self):
			
			# state	 
			self.state = Counter(
			count=1
			)

			# styles
			self.styles = CounterStyles(
				btn="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded", 
				h1="self-center text-xl font-semibold whitespace-nowrap dark:text-white",
				container: "flex flex-col",
				btnText = "text-xl",
				controls = "flex flex-row",
			)

			# dependencies
			self.dependencies = dependencies

			#  events 
			emitter.on("inc_count", increment)
			emitter.on("dec_count", decrement)

	def increment(self):
		self.state.count += 1

		
	def decrease(self):
		self.state.count -= 1

	def create_button(label_text, onclick_handler, styles):
		btn = Element(name="button")
		btn.attributes.append(Attribute(key=onclick, value=onclick_handler))
		btn.attributes.append(Attribute(key="styles", value=styles))	
		btn..children.append(Element(name="label", children=[label_text]))
			 

	def element(self):
		# header
		header =  Element(name="h1")
		header.attributes.append(Attribute(key=styles, value=self.styles.h1))
		header.children.append(Element(text("Counter: " + self.state.count)))

		#  btn controls
  
		incBtn = create_button(
			"Increase", 
			emitter.emit("inc_count"), 
			self.styles
		)

    	decBtn = create_button(
			"Decrease", 
			emitter.emit("dec_count"), 
			self.styles
		)

		# controls div
		controls = 	Element(name="div")
		controls.attributes.append(
			Attribute(key="styles", value=self.styles.controls)
		)
		controls.children.append(decBtn)
		controls.children.append(incBtn)

		# component
		comp = Element(name="div")

		comp.attr.append(Attribute(key="styles", value="container"))
		comp.children.append(header)
		comp.children.append(controls)
		
		return self.render(comp, [self.dependencies])
	    
```
