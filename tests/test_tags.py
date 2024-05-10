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

    def test_init(self):
        tb = Blueprint.div
        self.assertEqual(tb.node.name, "div")
        self.assertEqual(tb.node.attributes, [])  
        self.assertEqual(tb.node.children, []) 

    def test_with_attribute(self):
        tb = Blueprint.p
        tb.with_attribute("id", "main-paragraph")
        self.assertEqual(tb.node.attributes, [Attribute("id", "main-paragraph")])

    def test_with_child(self):
        tb = Blueprint.li
        child_node = Node("li")
        tb.with_child(child_node)
        self.assertEqual(tb.node.children, [child_node])

    def test_with_styles(self):
        tb = Blueprint.p
        tb.with_styles({"color": "blue", "font-size": "16px"})
        self.assertEqual(tb.node.attributes, [Attribute("style", "color:blue;font-size:16px")])

    def test_with_class(self):
        tb = Blueprint.p
        tb.with_class("my-class") 
        self.assertEqual(tb.node.attributes, [Attribute("class", "my-class")])

    def test_with_classes(self):
        tb = Blueprint.span
        tb.with_classes("highlighted", "bold")
        self.assertEqual(tb.node.attributes, [Attribute("class", "highlighted bold")])

    def test_with_class_avoid_duplicates(self):
        tb = Blueprint.div
        tb.with_class("container").with_class("container")  # Adding the same class twice
        self.assertEqual(tb.node.attributes, [Attribute("class", "container")])
