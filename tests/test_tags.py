from zenaura.client.tags import Node, Attribute, HTMLTags
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

    def test_node_to_html_with_nested_nodes(self):
        # Create a nested node structure
        node1 = Node("div")
        node1.attributes.append(Attribute("class", "container"))

        node2 = Node("h1")
        node2.children.append("Welcome to our website")

        node3 = Node("p")
        node3.children.append("This is a paragraph")

        node1.children.append(node2)
        node1.children.append(node3)

        # Convert the node to HTML
        expected_html = (
            "<div class=\"container\">"
            "<h1>Welcome to our website</h1>"
            "<p>This is a paragraph</p>"
            "</div>"
        )
        self.assertEqual(node1.to_html(), expected_html)

    def test_node_to_html_with_nested_nodes_and_attributes(self):
        # Create a nested node structure with attributes
        node1 = Node("div")
        node1.attributes.append(Attribute("class", "container"))

        node2 = Node("h1")
        node2.attributes.append(Attribute("id", "title"))
        node2.children.append("Welcome to our website")

        node3 = Node("p")
        node3.attributes.append(Attribute("class", "description"))
        node3.children.append("This is a paragraph")

        node1.children.append(node2)
        node1.children.append(node3)

        # Convert the node to HTML
        expected_html = (
            "<div class=\"container\">"
            "<h1 id=\"title\">Welcome to our website</h1>"
            "<p class=\"description\">This is a paragraph</p>"
            "</div>"
        )
        self.assertEqual(node1.to_html(), expected_html)

    def test_node_to_html_with_nested_nodes_and_mixed_content(self):
        # Create a nested node structure with mixed content
        node1 = Node("div")
        node1.attributes.append(Attribute("class", "container"))

        node2 = Node("h1")
        node2.children.append("Welcome to our website")

        node3 = Node("p")
        node3.children.append("This is a paragraph")

        node4 = Node("img")
        node4.attributes.append(Attribute("src", "image.jpg"))
        node4.attributes.append(Attribute("alt", "Image"))

        node1.children.append(node2)
        node1.children.append(node3)
        node1.children.append(node4)

        # Convert the node to HTML
        expected_html = (
            "<div class=\"container\">"
            "<h1>Welcome to our website</h1>"
            "<p>This is a paragraph</p>"
            "<img src=\"image.jpg\" alt=\"Image\">"
            "</div>"
        )
        self.assertEqual(node1.to_html(), expected_html)

    def test_node_to_html_with_nested_nodes_and_empty_children(self):
        # Create a nested node structure with empty children
        node1 = Node("div")
        node1.attributes.append(Attribute("class", "container"))

        node2 = Node("h1")
        node2.children.append("Welcome to our website")

        node3 = Node("p")
        node3.children.append("")

        node1.children.append(node2)
        node1.children.append(node3)

        # Convert the node to HTML
        expected_html = (
            "<div class=\"container\">"
            "<h1>Welcome to our website</h1>"
            "<p></p>"
            "</div>"
        )
        self.assertEqual(node1.to_html(), expected_html)



    def test_to_dict_with_children(self):
        
        child1 = Node("child1")
        child2 = Node("child2")
        node = Node("parent", children=[child1, child2])

        
        result = node.to_dict()
        self.assertDictEqual(
            result , 
            {
            "name": "parent",
            "children": [
                {
                "name": "child1",
                "children": []
                },
                {
                "name": "child2",
                "children": []
                }
            ]
            }
        )
       
        
    def test_to_dict_without_children(self):
        
        node = Node("parent")

        
        result = node.to_dict()


        self.assertDictEqual(
            result, {"name": "parent", "children": []}
        )
    def test_to_dict_with_children(self):
        
        child1 = Node("child1")
        node = Node("parent", children=[child1])

        
        result = node.to_dict()


        self.assertDictEqual(
            result,
            {
            "name": "parent",
            "children": [
                {
                "name": "child1",
                "children": []
                }
            ]
            }
        )
        
    def test_to_dict_with_nested_children(self):
        
        child1 = Node("child1", children=[Node("grandchild1"), Node("grandchild2")])
        child2 = Node("child2")
        node = Node("parent", children=[child1, child2])

        
        result = node.to_dict()


        self.assertDictEqual(
            result,
            {
                "name": "parent",
                "children": [
                    {
                    "name": "child1",
                    "children": [
                        {
                        "name": "grandchild1",
                        "children": [],
                        },
                        {
                        "name": "grandchild2",
                        "children": [],
                        }
                    ]
                    },
                    {
                    "name": "child2",
                    "children": [],
                    }
                ]
            }
        )

    def test_getAttributes(self):

        node = Node("div")
        node.attributes.append(Attribute("class", "container"))
        node.attributes.append(Attribute("id", "title"))
        node.attributes.append(Attribute("style", "color:blue;font-size:16px"))

        attributes = node.getAttributes(node)

        expected = " class=\"container\" id=\"title\" style=\"color:blue;font-size:16px\""
        self.assertEqual(attributes, expected)


    def test_findChildByName_found(self):
        node = Node("div")
        node.children.append(Node("h1"))

        child = node.findChildByName("h1")
        self.assertEqual(child.name, "h1")

    def test_findChildByName_not_found(self):
        node = Node("div")

        child = node.findChildByName("h1")
        self.assertFalse(child)

    def test_findAllByName_found(self):
        node = Node("div")
        node.children.append(Node("h1"))
        node.children.append(Node("h1"))
        node.children.append(Node("p"))

        children = node.findAllByName("h1")
        self.assertEqual(len(children), 2)

    def test_findAllByName_not_found(self):
        node = Node("div")
        node.children.append(Node("h1"))
        node.children.append(Node("p"))

        children = node.findAllByName("h2")
        self.assertEqual(len(children), 0)

    def test_findByAttribute_found(self):
        node = Node("div")
        child = Node("h1")
        child.attributes.append(Attribute("class", "container"))
        node.children.append(child)

        child = node.findByAttribute("class", "container")
        self.assertEqual(child.name, "h1")

    def test_findByAttribute_not_found(self):
        node = Node("div")

        child = node.findByAttribute("class", "container")
        self.assertFalse(child)

    def test_findAllChildrenByAttributeKey_found(self):
        node = Node("div")
        node.children.append(Node("h1", attributes=[Attribute("class", "container")]))
        node.children.append(Node("h1", attributes=[Attribute("class", "container")]))
        node.children.append(Node("p"))

        children = node.findAllChildrenByAttributeKey("class")
        self.assertEqual(len(children), 2)

    def test_findAllChildrenByAttributeKey_not_found(self):
        node = Node("div")
        node.children.append(Node("p"))

        children = node.findAllChildrenByAttributeKey("class")
        self.assertFalse(children)

    def test_findAllChildrenByAttributeValue_found(self):
        node = Node("div")
        node.children.append(Node("h1", attributes=[Attribute("class", "container")]))
        node.children.append(Node("h1", attributes=[Attribute("class", "container")]))
        node.children.append(Node("p"))

        children = node.findAllChildrenByAttributeValue("container")
        self.assertEqual(len(children), 2)


    def test_findAllChildrenByAttributeValue_not_found(self):
        node = Node("div")

        children = node.findAllChildrenByAttributeValue("container")
        self.assertFalse(children)

    def test_replace_children_found(self):
        node = Node("div")
        spe = Node("h1")
        node.children.append(Node("h2"))
        node.children.append(spe)
        node.children.append(Node("p"))

        node.replace(spe, Node("h2"))
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].name, "h2")
        self.assertEqual(node.children[1].name, "h2")
        self.assertEqual(node.children[2].name, "p")

    def test_replace_children_not_found(self):
        node = Node("div")
        spe = Node("h1")
        node.children.append(Node("h2"))
        node.children.append(Node("h1"))
        node.children.append(Node("p"))

        node.replace(spe, spe)
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].name, "h2")
        self.assertEqual(node.children[1].name, "h1")
        self.assertEqual(node.children[2].name, "p")

    def test_getChildIndex_found(self):
        node = Node("div")
        k = Node("h1")
        node.children.append(k)
        node.children.append(Node("h2"))
        node.children.append(Node("p"))

        index = node.getChildIndex(k)
        self.assertEqual(index, 0)

    def test_insertAfter(self):
        node = Node("div")
        h2 = Node("h2")
        node.children.append(Node("h1"))
        node.children.append(h2)
        node.children.append(Node("p"))

        node.insertAfter(h2, Node("h3"))
        self.assertEqual(len(node.children), 4)
        self.assertEqual(node.children[0].name, "h1")
        self.assertEqual(node.children[1].name, "h2")
        self.assertEqual(node.children[2].name, "h3")
        self.assertEqual(node.children[3].name, "p")

    def test_insertBefore(self):
        node = Node("div")
        h2 = Node("h2")
        node.children.append(Node("h1"))
        node.children.append(h2)
        node.children.append(Node("p"))

        node.insertBefore(h2, Node("h3"))
        self.assertEqual(len(node.children), 4)
        self.assertEqual(node.children[0].name, "h1")
        self.assertEqual(node.children[1].name, "h3")
        self.assertEqual(node.children[2].name, "h2")
        self.assertEqual(node.children[3].name, "p")


    def test_remove(self):
        node = Node("div")
        h2 = Node("h2")
        node.children.append(Node("h1"))
        node.children.append(h2)
        node.children.append(Node("p"))

        node.remove(h2)
        self.assertEqual(len(node.children), 2)
        self.assertEqual(node.children[0].name, "h1")
        self.assertEqual(node.children[1].name, "p")

    def test_appendAttributeToChild(self):

        node = Node("div")
        h2 = Node("h2")
        node.children.append(Node("h1"))
        node.children.append(h2)
        node.children.append(Node("p"))

        h2.attributes.append(Attribute("class", "container"))
        h2.attributes.append(Attribute("id", "title"))
        h2.attributes.append(Attribute("style", "color:blue;font-size:16px"))

        node.appendAttributeToChild(h2, Attribute("class", "container2"))

        self.assertEqual(len(h2.attributes), 4)
        self.assertEqual(h2.attributes[0].key, "class")
        self.assertEqual(h2.attributes[0].value, "container")
        self.assertEqual(h2.attributes[1].key, "id")
        self.assertEqual(h2.attributes[1].value, "title")
        self.assertEqual(h2.attributes[2].key, "style")
        self.assertEqual(h2.attributes[2].value, "color:blue;font-size:16px")
        self.assertEqual(h2.attributes[3].key, "class")
        self.assertEqual(h2.attributes[3].value, "container2")
        