import sys
import unittest
from unittest.mock import patch, MagicMock
from zenui.tags import Attribute, Element
from tests.mocks.browser_mocks import MockDocument, MockWindow

sys.modules["pyscript"] = MagicMock()

class TestComponent(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from tests.mocks.counter_mocks import Counter, BTN_STYLES
        from zenui.zenui_dom import zenui_dom
        self.dependencies = {}  # Mock dependencies if needed
        self.btnstyles = BTN_STYLES
        self.counter = Counter(self.dependencies)
        self.document = MockDocument()
        self.window = MockWindow()
        self.zenui_dom = zenui_dom
        
    def test_mount(self):
        self.zenui_dom.mount(self.counter)
        self.assertIn(self.counter.componentId, self.zenui_dom.zen_dom_table.keys())
        prev = self.zenui_dom.zen_dom_table[self.counter.componentId]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getElementById("root")
        self.assertTrue(exists)
	
    def test_search(self):
        prevTree = self.counter.element()
        # simulate search table mount manually for testing
        self.zenui_dom.zen_dom_table[self.counter.componentId] = prevTree
        self.counter.set_state("test")
        newTree = self.counter.element()
        prevParentNode, newParentNode = self.zenui_dom.search(prevTree, newTree)
        self.assertEqual(prevParentNode.name, newParentNode.name)
        self.assertNotEqual(prevParentNode.children, newParentNode.children)

    
    def test_render_with_new_element(self):
        self.zenui_dom.mount(self.counter)  # For initial rendering

        # update state and re-render component
        self.counter.set_state("test")

        self.zenui_dom.render(self.counter)

        # get component in zenui dom
        rerendered = self.zenui_dom.zen_dom_table[self.counter.componentId]
        
        self.assertEqual(rerendered.children[0].children[0].children[0], "yoo")

        # print(self.document.getElementById("root").innerHTML)
        # print(self.zenui_dom.zen_dom_table[self.counter.componentId])