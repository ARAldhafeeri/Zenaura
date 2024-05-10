from zenui.tags import Node, Attribute, HTMLTags
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
        node = HTMLTags().div \
            .with_attribute("test", "test") \
            .with_child(
                Node(name="test")
            ).build()
        
        self.assertEqual(len(node.children), 1)
        self.assertEqual(len(node.attributes), 1)
        self.assertTrue(isinstance(node.children[0], Node ))
        self.assertTrue(isinstance(node.attributes[0], Attribute))

    def test_init(self):
        tb = HTMLTags().div.build()
        self.assertEqual(tb.name, "div")
        self.assertEqual(tb.attributes, [])  
        self.assertEqual(tb.children, []) 

    def test_with_attribute(self):
        tb = HTMLTags().p
        tb.with_attribute("id", "main-paragraph").build()
        self.assertEqual(tb.node.attributes[0].key, "id")
        self.assertEqual(tb.node.attributes[0].value, "main-paragraph")


    def test_with_styles(self):
        tb = HTMLTags().p
        tb.with_styles({"color": "blue", "font-size": "16px"}).build()
        self.assertEqual(tb.node.attributes[0].key, "style")
        self.assertEqual(tb.node.attributes[0].value, "color:blue;font-size:16px")

    def test_with_class(self):
        tb = HTMLTags().p
        tb.with_class("my-class").build() 
        self.assertEqual(tb.node.attributes[0].key, "class")
        self.assertEqual(tb.node.attributes[0].value, "my-class")

    def test_with_classes(self):
        tb = HTMLTags().span
        tb.with_classes("highlighted", "bold").build()
        self.assertEqual(tb.node.attributes[0].key, "class")
        self.assertEqual(tb.node.attributes[0].value, "highlighted bold")


    def test_with_class_avoid_duplicates(self):
        tb = HTMLTags().div
        tb.with_class("container").with_class("container").build()
        self.assertEqual(tb.node.attributes[0].key, "class")
        self.assertEqual(tb.node.attributes[0].value, "container")

