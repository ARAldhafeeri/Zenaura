import sys
import unittest
from unittest.mock import patch, MagicMock
from zenaura.client.tags import Attribute, Node
from tests.mocks.browser_mocks import MockDocument, MockWindow

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

	@patch('pyscript.document')
	@patch('pyscript.window')
	def setUp(self, document, window):  # Run before each test
		from tests.mocks.counter_mocks import Counter, BTN_STYLES, CounterState
		from zenaura.client.dom import zenaura_dom
		self.dependencies = {}  # Mock dependencies if needed
		self.btnstyles = BTN_STYLES
		self.counter = Counter(self.dependencies)
		document = MockDocument()
		window = MockWindow()
		self.zenaura_dom = zenaura_dom
		self.counterState = CounterState

	def test_initial_state(self):
		state = self.counter.get_state()
		self.assertEqual(state.count, 0)  # Ensure initial count is 0
	

	def test_increment(self):
		self.counter.increment()
		state = self.counter.get_state()
		self.assertEqual(state.count, 1)
	

	def test_create_button(self):
		button = self.counter.create_button("test", self.counter.increment)


		self.assertEqual(len(button.attributes), 2)
		self.assertEqual(len(button.children), 1)

		self.assertEqual(self.btnstyles.btn, button.attributes[1].value)
		self.assertEqual(self.counter.increment, button.attributes[0].value)
		self.assertEqual(button.children[0].name , "label")

	def test_decrease(self):
		self.counter.decrease()
		state = self.counter.get_state()
		self.assertEqual(state.count, -1)
	


	def test_node_structure(self):
		rendered_node = self.counter.node()
		# Check for top-level container and attributes 
		self.assertEqual(rendered_node.name, 'div')
		# Ensure h1 header is present
		header = rendered_node.children[0]
		self.assertEqual(header.name, 'h1')

		# Check controls div
		controls = rendered_node.children[1]
		self.assertEqual(controls.name, 'div')
		self.assertEqual(self.btnstyles.controls, rendered_node.children[1].attributes[0].value)

		# check parent node and nodes have unique node Id
		curr = [rendered_node]
		ids = []
		while curr:
			node = curr.pop()
			self.assertTrue(node.nodeId)
			self.assertNotIn(node.nodeId, ids)
			ids.append(node.nodeId)
			for i in node.children:
				if isinstance(i, Node):
					curr.append(i)


	def test_component_rerender_on_state_update(self):
		self.zenaura_dom.mount(self.counter)
		# trigger mutator function
		self.counter.increment()
		re_rendered = self.zenaura_dom.zen_dom_table[self.counter.componentId]
		self.assertEqual(re_rendered.children[0].children[0].children[0].children[0], f'Counter: {self.counterState(count=1)}')
		self.counter.decrease()
		re_rendered = self.zenaura_dom.zen_dom_table[self.counter.componentId]
		self.assertEqual(re_rendered.children[0].children[0].children[0].children[0], f'Counter: {self.counterState(count=0)}')




if __name__ == "__main__":
    unittest.main()