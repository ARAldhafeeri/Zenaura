import sys
import unittest
import gc
import time
from unittest.mock import MagicMock
from zenaura.client.tags import Node, Attribute
from zenaura.client.compiler import compiler

class TestSearchAlgorithm(unittest.TestCase):

    def setUp(self):  # Run before each test
        from zenaura.client.dom import zenaura_dom
        self.zenaura_dom = zenaura_dom
        gc.collect()  # Ensure a clean state before each test
        self.initial_garbage_count = len(gc.garbage)  # Record initial garbage
        
    def test_no_diff(self):
        prev_tree = Node(name="div", children=["child1"])
        new_tree = Node(name="div", children=["child1"])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 0)  # No differences

    def test_identical_trees(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 0)

    def test_search_child_appended(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=["test"])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(diffedNode.text, "test")

    def test_update_child(self):
        prev_tree = Node(name="div", children=["child1"])
        new_tree = Node(name="div", children=["updated_child"])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(diffedNode.children[0].text, "updated_child")

    def test_add_attribute(self):
        prev_tree = Node(name="div", children=[], attributes=[])
        new_tree = Node(name="div", children=[], attributes=[Attribute("test", "test")])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(diffedNode.attributes[0].value, "test")

    def test_remove_attribute(self):
        prev_tree = Node(name="div", children=[], attributes=[Attribute("test", "test")])
        new_tree = Node(name="div", children=[], attributes=[])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(len(diffedNode.attributes), 0)  # Attribute removed

    def test_remove_attribute(self):
        prev_tree = Node(name="div", children=[], attributes=[Attribute("test", "test")])
        new_tree = Node(name="div", children=[], attributes=[Attribute("test", "test2")])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(diffedNode.attributes[0].value, "test2")  # Attribute removed
    
    def test_attribute_added(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[], attributes=[Attribute("class", "new-class")])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[0].value, "new-class")

    def test_attribute_removed(self):
        prev_tree = Node(name="div", children=[], attributes=[Attribute("class", "old-class")])
        new_tree = Node(name="div", children=[])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(len(diffed_node.attributes), 0)

    def test_attribute_value_changed(self):
        prev_tree = Node(name="div", children=[], attributes=[Attribute("class", "old-class")])
        new_tree = Node(name="div", children=[], attributes=[Attribute("class", "new-class")])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[0].value, "new-class")

    def test_attribute_moved(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"], attributes=[Attribute("class", "old-class")])
        ])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"], attributes=[Attribute("class", "new-class")])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[0].value, "new-class")

    def test_deeply_nested_add_child(self):
        prev_tree = Node("div", children=[
            Node("section", children=[
                Node("p", children=["existing text"])
            ])
        ])
        new_tree = Node("div", children=[
            Node("section", children=[
                Node("p", children=["existing text"]),
                Node("span", children=["new text"])  # Added a new nested child
            ])
        ])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()

        self.assertEqual(diffedNode.name, "span")  
        self.assertEqual(diffedNode.children[0].text, "new text")
        self.assertEqual(path, "")  # path to the parent where the addition occurred

    def test_deeply_nested_remove_child(self):
        prev_tree = Node("div", children=[
            Node("ul", children=[
                Node("li", children=["item1"]),
                Node("li", children=["item2"])  
            ])
        ])
        new_tree = Node("div", children=[
            Node("ul", children=[
                Node("li", children=["item1"]) 
            ])
        ])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        # self.assertEqual(diffedNode.name, "li")  
        self.assertEqual(path, "0011")  # Removed node's parent path
        self.assertEqual(diffedNode.children[0].text,"item2")


    def test_deeply_nested_attribute_change(self):
        prev_tree = Node("div", children=[
            Node("article", children=[
                Node("h2", attributes=[Attribute("id", "old-title")])
            ])
        ])
        new_tree = Node("div", children=[
            Node("article", children=[
                Node("h2", attributes=[Attribute("id", "new-title")])  # Changed attribute
            ])
        ])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prevNodeId, diffedNode, path, op = diff.pop()
        self.assertEqual(diffedNode.attributes[0].value, "new-title")
        self.assertEqual(path,"0010")  # path to the node with the attribute change

    def test_mixed_deep_changes(self):
        prev_tree = Node("div", children=[
            Node("section", attributes=[Attribute("class", "old-style")], children=[
                Node("p", children=["some text"])
            ])
        ])
        new_tree = Node("div", children=[
            Node("section", attributes=[Attribute("class", "new-style")], children=[
                Node("p", children=[]),  # Removed child text
                Node("span", children=["added text"])  # Added a new child
            ])
        ])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 3)


    def test_very_deeply_nested_with_multiple_changes(self):
        # Create a deeply nested structure with several levels
        prev_tree = Node("div", children=[
            Node("main", children=[
                Node("section", children=[
                    Node("article", children=[
                        Node("h1", children=["Old Title"]),
                        Node("p", children=["Old paragraph text."]),
                        Node("ul", children=[
                            Node("li", children=["Item 1"]),
                            Node("li", children=["Item 2"])
                        ])
                    ])
                ])
            ])
        ])

        new_tree = Node("div", children=[
            Node("main", children=[
                Node("section", children=[
                    Node("article", children=[
                        Node("h1", children=["New Title"]),  # Changed text
                        Node("p", attributes=[Attribute("style", "font-weight: bold;")]), # Added attribute
                        Node("ul", children=[
                            Node("li", children=["Item 1"]),
                            Node("li", children=["Modified Item 2"])  # Changed text
                        ]),
                        Node("div", children=["A newly added element"])  # Added element
                    ])
                ])
            ])
        ])
        # The expected number of differences should be 4
        # Change h1 text, add style to p, update li text and add div element
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 5)

        # Iterate over the differences to check details (add more assertions as needed)
        for prev_node_id, diffed_node, path, op in diff:
            # Example assertion for the added div element
            if diffed_node.name == "div":
                self.assertEqual(diffed_node.children[0].text, "A newly added element")
                self.assertEqual(path, "")  # root


    def test_extreme_deeply_nested_with_various_changes(self):
        # Create an extremely deeply nested structure
        prev_tree = Node("html", children=[
            Node("body", children=[
                Node("div", children=[
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("header", children=[
                                    Node("h1", children=["Old Title"])
                                ]),
                                Node("div", children=[
                                    Node("p", children=["Paragraph 1"]),
                                    Node("p", children=["Paragraph 2"]),
                                    Node("ul", children=[
                                        Node("li", children=["Item A"]),
                                        Node("li", children=["Item B"]),
                                        Node("li", children=["Item C"]),
                                    ])
                                ]),
                                Node("footer", children=[
                                    Node("p", children=["Old footer"])
                                ])
                            ])
                        ])
                    ])
                ])
            ])
        ])

        new_tree = Node("html", children=[
            Node("body", children=[
                Node("div", children=[
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("header", children=[
                                    Node("h1", children=["New Title"])  # Changed text
                                ]),
                                Node("div", children=[
                                    Node("p", children=["Paragraph 1"]),
                                    Node("p", children=["Modified Paragraph 2"])  # Changed text
                                ]),
                                Node("footer", children=[
                                    Node("p", children=["New footer"]),
                                    Node("a", children=["Link to external website"]) # Added
                                ])
                            ]),
                            Node("aside", children=[  # Added node
                                Node("p", children=["Sidebar content"])
                            ])
                        ])
                    ])
                ])
            ])
        ])
        
        # 6 changes have been made
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 6)

        # Iterate over the differences to check details (add more assertions as needed)
        for prev_node_id, diffed_node, path, op in diff:
            # Example assertion for the added aside element
            if diffed_node.name == "aside":
                self.assertEqual(diffed_node.children[0].children[0].text, "Sidebar content")
                self.assertEqual(path, "") 


    def test_extremely_nested_with_comprehensive_changes(self):
        # Create an extremely deeply nested structure
        prev_tree = Node("html", children=[
            Node("body", children=[
                Node("div", attributes=[Attribute("id", "container")], children=[
                    Node("header", children=[
                        Node("h1", children=["Old Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["About"])]),
                                Node("li", children=[Node("a", children=["Contact"])])
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["Old Article Title"]),
                                Node("p", children=["Paragraph 1"]),
                                Node("p", children=["Paragraph 2"]),
                                Node("img", attributes=[Attribute("src", "old-image.jpg")])
                            ]),
                            Node("aside", children=[
                                Node("p", children=["Old sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[
                        Node("p", children=["Old footer text"])
                    ])
                ])
            ])
        ])

        new_tree = Node("html", children=[
            Node("body", children=[
                Node("div", attributes=[Attribute("id", "updated-container")], children=[
                    Node("header", children=[
                        Node("h1", children=["New Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["Products"])]),  # Changed
                                Node("li", children=[Node("a", children=["Blog"])]),   # Changed
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["New Article Title"]),
                                Node("p", children=["Modified Paragraph 1"]),
                                Node("img", attributes=[Attribute("src", "new-image.jpg"), Attribute("alt", "New Image Description")])  # Changed + added
                            ]),
                            Node("aside", children=[
                                Node("p", children=["New sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[  # Changed order
                        Node("p", children=["Copyright 2024"]),
                        Node("p", children=["New footer text"])
                    ])
                ])
            ])
        ])
        # 11 Changes have been made
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 12)



    def test_extremely_nested_with_comprehensive_changes_gc(self):
        prev_tree = Node("html", children=[
            Node("body", children=[
                Node("div", attributes=[Attribute("id", "container")], children=[
                    Node("header", children=[
                        Node("h1", children=["Old Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["About"])]),
                                Node("li", children=[Node("a", children=["Contact"])])
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["Old Article Title"]),
                                Node("p", children=["Paragraph 1"]),
                                Node("p", children=["Paragraph 2"]),
                                Node("img", attributes=[Attribute("src", "old-image.jpg")])
                            ]),
                            Node("aside", children=[
                                Node("p", children=["Old sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[
                        Node("p", children=["Old footer text"])
                    ])
                ])
            ])
        ])

        new_tree = Node("html", children=[
            Node("body", children=[
                Node("div", attributes=[Attribute("id", "updated-container")], children=[
                    Node("header", children=[
                        Node("h1", children=["New Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["Products"])]),  # Changed
                                Node("li", children=[Node("a", children=["Blog"])]),   # Changed
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["New Article Title"]),
                                Node("p", children=["Modified Paragraph 1"]),
                                Node("img", attributes=[Attribute("src", "new-image.jpg"), Attribute("alt", "New Image Description")])  # Changed + added
                            ]),
                            Node("aside", children=[
                                Node("p", children=["New sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[  # Changed order
                        Node("p", children=["Copyright 2024"]),
                        Node("p", children=["New footer text"])
                    ])
                ])
            ])
        ])

        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 12)

        # Garbage collection assessment
        gc.collect()  # Force garbage collection after the diff
        final_garbage_count = len(gc.garbage)  # Record garbage after collection

        # Assert that garbage did not increase significantly
        garbage_increase = final_garbage_count - self.initial_garbage_count
        self.assertLessEqual(garbage_increase, 10,  # Allow for some minor fluctuations
                             "Unexpected increase in garbage objects after diff")
        

    def test_child_added(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Hello, world!")

    def test_child_removed(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        new_tree = Node(name="div", children=[])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op= diff.pop()
        self.assertEqual(len(diffed_node.children), 1)

    def test_child_moved(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        new_tree = Node(name="div", children=[
            Node(name="span", children=["Hello, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 2)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Hello, world!")

    def test_child_order_changed(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"]),
            Node(name="span", children=["Goodbye, world!"])
        ])
        new_tree = Node(name="div", children=[
            Node(name="span", children=["Goodbye, world!"]),
            Node(name="p", children=["Hello, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 4)
        prev_node_id, diffed_node, path, op = diff.pop()
        # removed - added pair 1 :
        self.assertEqual(diffed_node.children[0].text, "Hello, world!")
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Goodbye, world!")
        # remove added pair 2: 
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Goodbye, world!")
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Hello, world!")




    def test_text_node_added(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Hello, world!")

    def test_text_node_removed(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        new_tree = Node(name="div", children=[])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)

    def test_text_node_content_changed(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Goodbye, world!"])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 1)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Goodbye, world!")

    def test_multiple_changes(self):
        prev_tree = Node(name="div", children=[
            Node(name="p", children=["Hello, world!"])
        ], attributes=[Attribute("class", "old-class")])
        new_tree = Node(name="div", children=[
            Node(name="p", children=["Goodbye, world!"])
        ], attributes=[Attribute("class", "new-class")])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 2)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Goodbye, world!")
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[0].value, "new-class")

    def test_deeply_nested_changes(self):
        prev_tree = Node(name="div", children=[
            Node(name="section", children=[
                Node(name="article", children=[
                    Node(name="h2", children=["Old Title"]),
                    Node(name="p", children=["Old paragraph text."])
                ])
            ])
        ])
        new_tree = Node(name="div", children=[
            Node(name="section", children=[
                Node(name="article", children=[
                    Node(name="h2", children=["New Title"]),
                    Node(name="p", children=["Modified paragraph text."])
                ])
            ])
        ])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 2)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "Modified paragraph text.")
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.children[0].text, "New Title")

    def test_changes_with_complex_attributes(self):
        prev_tree = Node(name="div", children=[], attributes=[Attribute("data-id", "123"), Attribute("data-options", '{"path": "value"}')])
        new_tree = Node(name="div", children=[], attributes=[Attribute("data-id", "456"), Attribute("data-options", '{"path": "new-value"}')])
        diff = self.zenaura_dom.search(prev_tree, new_tree, "comp-id")
        self.assertEqual(len(diff), 2)
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[0].value, "456")
        prev_node_id, diffed_node, path, op = diff.pop()
        self.assertEqual(diffed_node.attributes[1].value, '{"path": "new-value"}')


    def test_performance_large_tree(self):
        # Create a large tree with many nodes and attributes
        large_tree = Node("html", children=[
            Node("body", children=[
                Node("div", attributes=[Attribute("id", "updated-container")], children=[
                    Node("header", children=[
                        Node("h1", children=["New Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["Products"])]),  # Changed
                                Node("li", children=[Node("a", children=["Blog"])]),   # Changed
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["New Article Title"]),
                                Node("p", children=["Modified Paragraph 1"]),
                                Node("img", attributes=[Attribute("src", "new-image.jpg"), Attribute("alt", "New Image Description")])  # Changed + added
                            ]),
                            Node("aside", children=[
                                Node("p", children=["New sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[  # Changed order
                        Node("p", children=["Copyright 2024"]),
                        Node("p", children=["New footer text"])
                    ])
                ])
            ]),
             Node("body", children=[
                Node("div", attributes=[Attribute("id", "updated-container")], children=[
                    Node("header", children=[
                        Node("h1", children=["New Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["Products"])]),  # Changed
                                Node("li", children=[Node("a", children=["Blog"])]),   # Changed
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["New Article Title"]),
                                Node("p", children=["Modified Paragraph 1"]),
                                Node("img", attributes=[Attribute("src", "new-image.jpg"), Attribute("alt", "New Image Description")])  # Changed + added
                            ]),
                            Node("aside", children=[
                                Node("p", children=["New sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[  # Changed order
                        Node("p", children=["Copyright 2024"]),
                        Node("p", children=["New footer text"])
                    ])
                ])
            ]),
             Node("body", children=[
                Node("div", attributes=[Attribute("id", "updated-container")], children=[
                    Node("header", children=[
                        Node("h1", children=["New Title"]),
                        Node("nav", children=[
                            Node("ul", children=[
                                Node("li", children=[Node("a", children=["Home"])]),
                                Node("li", children=[Node("a", children=["Products"])]),  # Changed
                                Node("li", children=[Node("a", children=["Blog"])]),   # Changed
                            ])
                        ])
                    ]),
                    Node("main", children=[
                        Node("section", children=[
                            Node("article", children=[
                                Node("h2", children=["New Article Title"]),
                                Node("p", children=["Modified Paragraph 1"]),
                                Node("img", attributes=[Attribute("src", "new-image.jpg"), Attribute("alt", "New Image Description")])  # Changed + added
                            ]),
                            Node("aside", children=[
                                Node("p", children=["New sidebar content"])
                            ])
                        ])
                    ]),
                    Node("footer", children=[  # Changed order
                        Node("p", children=["Copyright 2024"]),
                        Node("p", children=["New footer text"])
                    ])
                ])
            ])
        ])
        # Measure the time it takes to search the tree
        start_time = time.time()
        diff = self.zenaura_dom.search(large_tree, large_tree, "comp-id")
        end_time = time.time()
        # Assert that the search time is within an acceptable range
        self.assertLess(end_time - start_time, 1)
        self.assertEqual(len(diff), 0)

if __name__ == "__main__":
    unittest.main()