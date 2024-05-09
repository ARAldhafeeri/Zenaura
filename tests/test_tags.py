from zenui.tags import Element, Attribute
import unittest

class DataclassTests(unittest.TestCase):


    def test_attribute_creation(self):
        attribute = Attribute(key="test", value="test")
        self.assertEqual(attribute.key, "test")
        self.assertTrue(isinstance(attribute, Attribute))

    def test_element_creation(self):
        child = Element(name="test")
        element = Element(name="div")
        element.children.append(child)
        print(element)
        element.attributes.append(Attribute(key="test", value="test"))
        self.assertEqual(child.name, "test")
        self.assertEqual(len(element.children), 1)
        self.assertEqual(len(element.attributes), 1)
        self.assertTrue(isinstance(element.children[0], Element ))
        self.assertTrue(isinstance(element.attributes[0], Attribute))

    def test_element_has_elementId(self):
        child = Element(name="test")
        parent = Element(name="div")
        parent.children.append(child)
        self.assertTrue(child.elementId)
        self.assertTrue(parent.elementId)