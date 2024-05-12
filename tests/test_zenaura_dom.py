import sys
import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockWindow
from zenaura.client.tags import Node
from zenaura.client.component import Component

sys.modules["pyscript"] = MagicMock()

class TestDom(unittest.TestCase):

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
        # advaced dom node mock 
        self.dom_node = MagicMock()
        self.dom_node.getNodeById = MagicMock(return_value=self.dom_node)
        self.dom_node.innerHTML = ""
        
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
        # print end of line 
        print("\n")
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

    # Graceful degradation: testing componentDidCatchError lifecycle method 
        
    def test_componentDidCatchError_with_custom_error_component(self):
        # Arrange
        class CustomErrorComponent(Component):
            def __init__(self, error_message):
                super().__init__()
                self.error_message = error_message
            def node(self):
                return Node("div", children=[Node("p", children=[str(self.error_message)])])

        class TestComponent(Component):
            def componentDidCatchError(self, error):
                return CustomErrorComponent(error_message=error).node()

        test_component = TestComponent()

        self.zenaura_dom.componentDidCatchError(test_component, "Custom error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test_component.componentId].children[0].children[0], "Custom error message")

    def test_componentDidCatchError_with_default_error_component(self):

        class TestComponent(Component):
            pass
        
        test = TestComponent()
        self.zenaura_dom.componentDidCatchError(test, "Default error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test.componentId].children[0].children[0], "Default error message")

    # Mount - testing component lifecycle methods 
    def test_unmount_no_componentWillUnmount_method(self):
        class TestComponent(Component):
            pass

        component = TestComponent()
        
        self.zenaura_dom.mount(component)
        self.zenaura_dom.unmount(component)

        self.assertNotIn(component.componentId, self.zenaura_dom.zen_dom_table)

    def test_unmount_with_componentWillUnmount_method(self):
        class TestComponent(Component):
            x = 0

            def componentWillUnmount(self, *args, **kwargs):
                self.x = 10
    
        component = TestComponent()

        self.zenaura_dom.mount(component)
        self.zenaura_dom.unmount(component)

        self.assertNotIn(component.componentId, self.zenaura_dom.zen_dom_table)
        self.assertEqual(component.x, 10)


    def test_component_did_mount_without_componentDidMount_method(self):
        class TestComponent(Component):
            def node(self):
                return Node("p")

        component = TestComponent()

        self.zenaura_dom.mount(component)

        self.assertEqual(self.zenaura_dom.zen_dom_table[component.componentId].name, "p")

    
    def test_component_did_mount_with_componentDidMount_method(self):
        class TestComponent(Component):
            x = 0
    
            def componentDidMount(self, *args, **kwargs):
                self.x = 10

            def node(self):
                return Node("p")
            
        component = TestComponent()

        self.assertEqual(component.x, 0)
        self.zenaura_dom.mount(component)

        self.assertEqual(component.componentId, self.zenaura_dom.mounted_component_id)
      
        self.assertEqual(component.x, 10)


    def test_component_did_update_without_componentDidUpdate_method(self):
        class TestComponent(Component):
            def node(self):
                return Node("p")
            
        component = TestComponent()
        self.zenaura_dom.mount(component)
        self.assertEqual(self.zenaura_dom.zen_dom_table[component.componentId].name, "p")
        

    def test_component_did_update_with_componentDidUpdate_method(self):
        class TestComponent(Component):
            
            x  = 0
            
            def node(self):
                return Node("p")
            
            def componentDidUpdate(self, *args, **kwargs):
                self.x = 10
            

        component = TestComponent()
        self.assertEqual(component.x, 0)
        self.zenaura_dom.render(component)
        self.assertEqual(component.x, 10)


    def test_mount_with_lifecycle_methods(self):
        class TestComponent(Component):
            x = 0

            def componentWillMount(self, *args, **kwargs):
                self.x = 5


            def componentWillUnmount(self, *args, **kwargs):
                self.x = 15

        component = TestComponent()


        self.zenaura_dom.mount(component)

        self.assertEqual(component.x, 5)

        self.zenaura_dom.unmount(component)

        self.assertEqual(component.x, 15)
