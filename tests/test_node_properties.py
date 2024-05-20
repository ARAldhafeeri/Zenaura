from zenaura.client.tags.node import Node
import unittest

class TestNodeCalculatedProperties(unittest.TestCase):
    
    
    def test_level_initialization(self):
        node = Node()
        self.assertEqual(node.level, 0)  # Default level should be 0

    def test_level_propagation(self):
        root = Node()
        child1 = Node()
        child2 = Node()
        root.children = [child1, child2]
        self.assertEqual(child1.level, 1)
        self.assertEqual(child2.level, 1)

    def test_is_leaf_initialization(self):
        node = Node()
        self.assertTrue(node.is_leaf)  # A node with no children is a leaf

        node_with_child = Node(children=[Node()])
        self.assertFalse(node_with_child.is_leaf)


    def test_key_initialization_and_assignment(self):
        root = Node()
        self.assertEqual(root.key, 0)  # Root node has key 0

        child1 = Node()
        root.children = [child1]
        self.assertEqual(child1.key, 0)  # First child under root has key 0

        child2 = Node()
        root.children.append(child2)
        self.assertEqual(child2.key, 1)  # Second child under root has key 1

    def test_key_remains_after_deletion(self):
        root = Node(children=[Node(), Node(), Node()])
        del root.children[1]  # Remove the middle child
        self.assertEqual(root.children[0].key, 0)  # Keys of remaining children are unchanged
        self.assertEqual(root.children[1].key, 2)

    def test_key_uniqueness_after_insertion(self):
        root = Node(children=[Node(), Node()])
        new_child = Node()
        root.children.insert(1, new_child)
        self.assertEqual(new_child.key, 2)  # New child gets a unique key
        self.assertEqual(root.children[2].key, 1)  # Existing child's key remains the same

    def test_level_initialization(self):
        node = Node()
        self.assertEqual(node.level, 0)  

    def test_level_propagation(self):
        root = Node()
        child1 = Node()
        child2 = Node()
        root.children = [child1, child2]
        self.assertEqual(child1.level, 1)
        self.assertEqual(child2.level, 1)
    
    def test_is_leaf_initialization(self):
        node = Node()
        self.assertTrue(node.is_leaf)  

        node_with_child = Node(children=[Node()])
        self.assertFalse(node_with_child.is_leaf)

    def test_is_text_node(self):
        node_with_text = Node(text="Hello")
        self.assertTrue(node_with_text.is_text_node)

        node_without_text = Node()
        self.assertFalse(node_without_text.is_text_node)


    def test_parent_assignment(self):
        parent = Node()
        child = Node()
        child.parent = parent
        parent.children.append(child)
        self.assertEqual(child.parent, parent)
        self.assertEqual(child.level, 1)

   

    def test_child_list_conversion(self):
        node = Node(children=['child1', 'child2'])
        self.assertIsInstance(node.children[0], Node)  
        self.assertEqual(node.children[0].text, 'child1')
        self.assertEqual(node.children[0].key, 0)
        self.assertEqual(node.children[1].key, 1)
        self.assertEqual(node.children[1].path, [0, 0, 1, 1] )
        self.assertEqual(node.children[0].path, [0, 0, 1, 0] )

    def test_is_leaf_update_on_child_change(self):
        node = Node()
        self.assertTrue(node.is_leaf)
        node.children = [Node()]
        self.assertFalse(node.is_leaf)
        node.children = []  
        self.assertTrue(node.is_leaf)


    def test_child_list_conversion(self):
        # Base Node
        root = Node(children=['child1', 'child2'])

        # Level 1 children
        child1 = root.children[0]
        child2 = root.children[1]

        # Level 2 children (added)
        child11 = Node(children=['grandchild11'])
        child12 = Node(children=['grandchild12'])
        child21 = Node(children=['grandchild21'])

        # Level 3 child (added for deeper nesting)
        great_grandchild111 = Node()

        # Attach children (to maintain the hierarchy)
        child1.children.append(child11)  # Using append
        child1.children.append(child12)
        child2.children = [child21]        # Direct assignment
        child11.children.append(great_grandchild111)

        # Assertions for base nodes (level 1)
        self.assertIsInstance(child1, Node)
        self.assertEqual(child1.text, 'child1')
        self.assertEqual(child1.key, 0)
        self.assertEqual(child1.path, [0, 0, 1, 0])
        self.assertEqual(child2.path, [0, 0, 1, 1])

        # Assertions for nested children (levels 2 and 3)
        self.assertEqual(child11.path, [0, 0, 1, 0, 2, 0])
        self.assertEqual(child12.path, [0, 0, 1, 0, 2, 1])
        self.assertEqual(child21.path, [0, 0, 1, 1, 2, 0])
        self.assertEqual(great_grandchild111.path, [0, 0, 1, 0, 2, 0, 3, 1])
