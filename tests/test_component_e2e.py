import unittest
from .mocks.counter_mocks import Counter, BTN_STYLES
from zenui.tags import Attribute, Element

class TestComponent(unittest.TestCase):


	def setUp(self):  # Run before each test
		self.dependencies = {}  # Mock dependencies if needed
		self.counter = Counter(self.dependencies)

	def test_initial_state(self):
		state = self.counter.get_state()
		self.assertEqual(state.count, 0)  # Ensure initial count is 0

	def test_increment(self):
		self.counter.increment()
		state = self.counter.get_state()
		self.assertEqual(state.count, 1)

	def test_create_button(self):
		button = self.counter.create_button("test", self.counter.increment())


		self.assertEqual(len(button.attributes), 2)
		self.assertEqual(len(button.children), 1)

		self.assertIn(Attribute(key="styles", value=BTN_STYLES.btn), button.attributes)
		self.assertIn(Attribute(key="onclick", value=self.counter.increment()), button.attributes)
		self.assertIn(
			Element(name="label", children=["test"])
			,
			button.children
		)

	def test_decrease(self):
		self.counter.decrease()
		state = self.counter.get_state()
		self.assertEqual(state.count, -1)

	def test_element_structure(self):
		rendered_element = self.counter.element(self.counter.get_state())
		# Check for top-level container and attributes 
		self.assertEqual(rendered_element.name, 'div')
		self.assertIn(Attribute(key="styles", value=BTN_STYLES.container), rendered_element.attributes)

		# Ensure h1 header is present
		header = rendered_element.children[0]
		self.assertEqual(header.name, 'h1')

		# Check controls div
		controls = rendered_element.children[1]
		self.assertEqual(controls.name, 'div')
		self.assertIn(Attribute(key="styles", value=BTN_STYLES.controls), controls.attributes)


