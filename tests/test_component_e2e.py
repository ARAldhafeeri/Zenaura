import sys
import unittest
from unittest.mock import patch, MagicMock
from zenaura.client.tags import Attribute, Node
from zenaura.client.dispatcher import dispatcher
sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.IsolatedAsyncioTestCase):

	def setUp(self):  # Run before each test
		from tests.mocks.counter_mocks import Counter, BTN_STYLES, CounterState
		from zenaura.client.dom import zenaura_dom
		self.dependencies = {}  # Mock dependencies if needed
		self.btnstyles = BTN_STYLES
		self.counter = Counter(self.dependencies)
		self.zenaura_dom = zenaura_dom
		self.counterState = CounterState

	def test_initial_state(self):
		state = self.counter.get_state()
		self.assertEqual(state.count, 0)  # Ensure initial count is 0
	

	async def test_increment(self):
		await self.counter.increment("update")
		print("self counter state", self.counter.state, self.counter.get_state())
		await self.zenaura_dom.render(self.counter)
		self.assertEqual(self.counter.state.count, 1)
	

	def test_create_button(self):
		button = self.counter.create_button("test", self.counter.increment)


		self.assertEqual(len(button.attributes), 2)
		self.assertEqual(len(button.children), 1)

		self.assertEqual(self.btnstyles.btn, button.attributes[1].value)
		self.assertEqual(self.counter.increment, button.attributes[0].value)
		self.assertEqual(button.children[0].name , "label")

	async def test_decrease(self):
		await self.counter.decrease("event")
		state = self.counter.get_state()
		self.assertEqual(state.count, -1)
	


	def test_node_structure(self):
		rendered_node = self.counter.render()
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


	def test_node_method_constructs_component_with_header_and_buttons(self):

		result = self.counter.render()

		# Assert
		self.assertEqual(result.name, "div")
		self.assertEqual(len(result.children), 2)
		self.assertEqual(result.children[0].name, "h1")
		self.assertEqual(len(result.children[0].children), 1)
		self.assertEqual(result.children[0].children[0].name, "text")
		self.assertEqual(len(result.children[0].children[0].children), 1)
		self.assertEqual(result.children[0].children[0].children[0].name, "data")
		self.assertEqual(len(result.children[1].children), 2)
		self.assertEqual(result.children[1].children[0].name, "button")
		self.assertEqual(result.children[1].children[0].children[0].name, "label")
		self.assertEqual(result.children[1].children[1].name, "button")
		self.assertEqual(result.children[1].children[1].children[0].name, "label")

	def test_create_button_with_empty_label(self):
		button = self.counter.create_button("", self.counter.increment)
		self.assertEqual(len(button.attributes), 2)
		self.assertEqual(len(button.children), 1)
		self.assertEqual(self.btnstyles.btn, button.attributes[1].value)
		self.assertEqual(self.counter.increment, button.attributes[0].value)
		self.assertEqual(button.children[0].name, "label")

	async def test_increment_multiple_times(self):
		# Increment the count multiple times
		for _ in range(5):
			await self.counter.increment("event")
		state = self.counter.get_state()
		self.assertEqual(state.count, 5)

	async def test_decrease_multiple_times(self):
		# Decrease the count multiple times
		for _ in range(3):
			await self.counter.decrease("event")
		state = self.counter.get_state()
		self.assertEqual(state.count, -3)


if __name__ == "__main__":
    unittest.main()