import sys
import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockWindow
from zenaura.client.tags import Node
from zenaura.client.component import Component

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from tests.mocks.counter_mocks import Counter, BTN_STYLES, CounterState
        from zenaura.client.dom import zenaura_dom
        self.dependencies = {}  # Mock dependencies if needed
        self.btnstyles = BTN_STYLES
        self.counter = Counter(self.dependencies)
        self.counterNewInstance = Counter
        self.document = MockDocument()
        self.window = MockWindow()
        self.zenaura_dom = zenaura_dom
        self.counterState = CounterState
        
    def test_mount(self):
        self.zenaura_dom.mount(self.counter)
        self.assertIn(self.counter.componentId, self.zenaura_dom.zen_dom_table.keys())
        prev = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getNodeById("root")
        self.assertTrue(exists)
	
    def test_search(self):
        prevTree = self.counter.node()
        # simulate search table mount manually for testing
        self.zenaura_dom.zen_dom_table[self.counter.componentId] = prevTree
        self.counter.set_state("test")
        newTree = self.counter.node()
        diff = self.zenaura_dom.search(prevTree, newTree)
        # hader location on tree, effected by change
        changedNodeId = prevTree.nodeId
        self.assertEqual(changedNodeId, diff[0][0])


    def test_render(self):
        self.zenaura_dom.mount(self.counter)
        self.counter.set_state(self.counterState(count=1))
        self.zenaura_dom.render(self.counter)
        re_rendered = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertEqual(re_rendered.children[0].children[0].children[0].children[0], f'Counter: {self.counterState(count=1)}')

    def test_update(self):
        prevTree = self.counter.node()
        newChildren = Node(name="div", children=["test"])
        updated = self.zenaura_dom.update(prevTree, prevTree.nodeId, newChildren)
        self.assertEqual(prevTree.children, newChildren.children)

        
    def test_mount_existing_component(self):
        
        self.zenaura_dom.mount(self.counter)
        exists = self.zenaura_dom.zen_dom_table[self.counter.componentId]

        
        self.assertTrue(exists)

    def test_render_unmounted_component(self):
        
        class K(Component):
            def node(self):
                return Node(name="div", children=[Node(name="span", children=["test"])])
        
        unmounted_counter = K()

        
        self.zenaura_dom.render(unmounted_counter)
        key = self.zenaura_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(key)

    def test_update_different_tree_structure(self):
        
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        new_children = Node(name="div", children=["test"])

        
        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_children)

        
        self.assertEqual(updated_tree.children[0], new_children.children[0])

    def test_search_identical_trees(self):
        
        prev_tree = Node(name="div", children=["test"])
        new_tree = Node(name="div", children=["test"])
        
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertEqual(diff, [])


    def test_search_different_trees_with_nested_structure(self):
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        new_tree = Node(name="div", children=[Node(name="span", children=["new test"])])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertNotEqual(diff, [])

    def test_search_identical_trees_with_empty_structure(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertEqual(diff, [])

    def test_search_different_trees_with_empty_structure(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertNotEqual(diff, [])


    def test_search_different_trees_with_nested_structure(self):
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        new_tree = Node(name="div", children=[Node(name="span", children=["new test"])])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertNotEqual(diff, [])

    def test_search_identical_trees_with_empty_structure(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertEqual(diff, [])

    def test_search_different_trees_with_empty_structure(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)

        self.assertNotEqual(diff, [])


    def test_update_with_empty_prev_tree(self):
        prev_tree = Node(name="div", children=[])
        new_children = Node(name="div", children=["test"])

        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_children)

        self.assertEqual(updated_tree.children, new_children.children)

    def test_update_with_empty_new_children(self):
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        new_children = Node(name="div", children=[])

        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_children)

        self.assertEqual(updated_tree.children, new_children.children)

    def test_update_with_same_children(self):
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"]), Node(name="p", children=["old"])])
        new_children = Node(name="div", children=[Node(name="span", children=["test"]), Node(name="p", children=["old"])])
        
        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_children)

        self.assertEqual(updated_tree.children, new_children.children)



    def test_search_and_update_different_trees_with_nested_structure(self):
        prev_tree = Node(name="div", children=[Node(name="span", children=["test"])])
        new_tree = Node(name="div", children=[Node(name="span", children=["new test"])])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)
        self.assertNotEqual(diff, [])

        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_tree)
        # confusing i know this, but this is how it works
        # it should update the changed node with the new node
        # not the entire tree
        self.assertEqual(updated_tree.nodeId, prev_tree.nodeId)
        # also the algorithm update the prev tree  changed nodes with the new nodes
        self.assertEqual(updated_tree.children[0].nodeId, prev_tree.children[0].nodeId)
        self.assertEqual(updated_tree.children[0].children[0], new_tree.children[0].children[0])

    def test_search_and_update_with_empty_trees(self):
        prev_tree = Node(name="div", children=[])
        new_tree = Node(name="div", children=[])
        
        diff = self.zenaura_dom.search(prev_tree, new_tree)
        self.assertEqual(diff, [])

        updated_tree = self.zenaura_dom.update(prev_tree, prev_tree.nodeId, new_tree)
        self.assertEqual(updated_tree.nodeId, prev_tree.nodeId)


    def test_search_method_returns_diff_nodes(self):
        prev_tree = Node("div")
        new_tree = Node("div")
        diff = self.zenaura_dom.search(prev_tree, new_tree)
        # Assert that the search method returns the expected diff nodes
        assert diff == []