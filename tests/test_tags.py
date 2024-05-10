from zenui.tags import Node, Attribute, Blueprint
import unittest

class DataclassTests(unittest.TestCase):


    def test_attribute_creation(self):
        attribute = Attribute(key="test", value="test")
        self.assertEqual(attribute.key, "test")
        self.assertTrue(isinstance(attribute, Attribute))

    def test_node_creation(self):
        child = Node(name="test")
        node = Node(name="div")
        node.children.append(child)
        print(node)
        node.attributes.append(Attribute(key="test", value="test"))
        self.assertEqual(child.name, "test")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(len(node.attributes), 1)
        self.assertTrue(isinstance(node.children[0], Node ))
        self.assertTrue(isinstance(node.attributes[0], Attribute))

    def test_node_has_nodeId(self):
        child = Node(name="test")
        parent = Node(name="div")
        parent.children.append(child)
        self.assertTrue(child.nodeId)
        self.assertTrue(parent.nodeId)

    def test_node_builder(self):
        node = Blueprint.div \
            .with_attribute("test", "test") \
            .with_child(
                Node(name="test")
            ).build()
        
        self.assertEqual(len(node.children), 1)
        self.assertEqual(len(node.attributes), 1)
        self.assertTrue(isinstance(node.children[0], Node ))
        self.assertTrue(isinstance(node.attributes[0], Attribute))
