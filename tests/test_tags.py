from zenui.tags import Element, Attribute
import unittest

class DataclassTests(unittest.TestCase):


    def test_attribute_creation(self):
        attribute = Attribute(key="test", value="test")
        self.assertEqual(attribute.key, "test")
        self.assertEqual(str(attribute), "Attribute")

    def test_element_creation(self):
        child = Element(name="test", children=[])
        attribute = Attribute(key="test", value="test")
        element = Element(name="test_element", children=[child, attribute])
        self.assertEqual(element.name, "test_element")
        self.assertEqual(len(element.children), 2)
        self.assertEqual(str(element.children[0]), "Element")
        self.assertEqual(str(element.children[1]), "Attribute")