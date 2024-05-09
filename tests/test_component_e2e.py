import sys
import unittest
from unittest.mock import patch, MagicMock
from zenui.tags import Attribute, Element
from tests.mocks.browser_mocks import MockDocument, MockWindow

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

	@patch('pyscript.document')
	@patch('pyscript.window')
	def setUp(self, document, window):  # Run before each test
		from tests.mocks.counter_mocks import Counter, BTN_STYLES
		self.dependencies = {}  # Mock dependencies if needed
		self.btnstyles = BTN_STYLES
		self.counter = Counter(self.dependencies)
		document = MockDocument()
		window = MockWindow()

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
	

	def test_element_structure(self):
		rendered_element = self.counter.element()
		# Check for top-level container and attributes 
		self.assertEqual(rendered_element.name, 'div')
		# Ensure h1 header is present
		header = rendered_element.children[0]
		self.assertEqual(header.name, 'h1')

		# Check controls div
		controls = rendered_element.children[1]
		self.assertEqual(controls.name, 'div')
		self.assertEqual(self.btnstyles.controls, rendered_element.children[1].attributes[0].value)

		# check parent element and elements have unique element Id
		curr = [rendered_element]
		ids = []
		while curr:
			node = curr.pop()
			self.assertTrue(node.elementId)
			self.assertNotIn(node.elementId, ids)
			ids.append(node.elementId)
			for i in node.children:
				if isinstance(i, Element):
					curr.append(i)




if __name__ == "__main__":
    unittest.main()