import sys
import unittest
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockWindow
from zenaura.client.tags import Node
from zenaura.client.page import Page
from zenaura.client.component import Component, Reuseable
from zenaura.client.compiler import compiler

sys.modules["pyscript"] = MagicMock()

class TestDom(unittest.IsolatedAsyncioTestCase):

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
        
    async def test_mount(self):
        await self.zenaura_dom.mount(Page([self.counter]))
        self.assertIn(self.counter.id, self.zenaura_dom.zen_dom_table.keys())
        prev = self.zenaura_dom.zen_dom_table[self.counter.id]
        self.assertTrue(prev)
        # mount is called on root div
        exists = self.document.getElementById("root")
        self.assertTrue(exists)
	

    async def test_render(self):
        await self.zenaura_dom.mount(Page([self.counter]))
        self.counter.set_state(self.counterState(count=1))
        await self.zenaura_dom.render(self.counter)
        re_rendered = self.zenaura_dom.zen_dom_table[self.counter.id]
        # print end of line 
        # new data structure Data for data binding
        self.assertEqual(re_rendered.children[0].children[0].children[0].children[0].text, f'Counter: {self.counterState(count=1)}')

        
    async def test_mount_existing_component(self):
        
        await self.zenaura_dom.mount(Page([self.counter]))
        exists = self.zenaura_dom.zen_dom_table[self.counter.id]

        
        self.assertTrue(exists)

    async def test_render_unmounted_component(self):
        
        class K(Component):
            def render(self):
                return Node(name="div", children=[Node(name="span", children=Node(text="test"))])
        
        unmounted_counter = K()

        
        await self.zenaura_dom.render(unmounted_counter)
        key = self.zenaura_dom.zen_dom_table[self.counter.id]
        self.assertFalse(key)


        
    def test_on_error_with_custom_error_component(self):
        # Arrange
        class CustomErrorComponent(Component):
            def __init__(self, error_message):
                super().__init__()
                self.error_message = error_message
            def render(self):
                return Node("div", children=[Node("p", children=[Node(text=self.error_message)])])

        @Reuseable
        class TestComponent(Component):
            def on_error(self, error):
                return CustomErrorComponent(error_message=error)

        test_component = TestComponent()

        self.zenaura_dom.on_error(test_component, "Custom error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test_component.id].children[0].children[0].text, "Custom error message")

    def test_on_error_with_default_error_component(self):

        class TestComponent2(Component):
            pass
        
        test = TestComponent2()
        self.zenaura_dom.on_error(test, "Default error message")

        self.assertEqual(self.zenaura_dom.zen_dom_table[test.id].children[0].text, "Default error message")

    # Mount - testing component lifecycle methods 

    async def test_component_did_mount_without_attached_method(self):
        
        class TestComponent1(Component):
            def render(self):
                return Node("p")

        c = TestComponent1()

        await self.zenaura_dom.mount(Page([c]))

        self.assertEqual(self.zenaura_dom.zen_dom_table[c.id].name, "p")

    
    async def test_component_did_mount_with_on_seatled_method(self):

        @Reuseable
        class TestComponent3(Component):
            x = 0
    
            def attached(self, *args, **kwargs):
                self.x = 10

            def render(self):
                return Node("p")
            
        component = TestComponent3()

        self.assertEqual(component.x, 0)
        await self.zenaura_dom.mount(Page([component]))
      
        self.assertEqual(component.x, 10)


    async def test_component_did_update_with_on_settled_method(self):
        @Reuseable
        class TestComponent(Component):
            
            x  = 0
            
            def render(self):
                return Node("p")
            
            def on_settled(self, *args, **kwargs):
                self.x = 10

        component = TestComponent()
        self.assertEqual(component.x, 0)
        await self.zenaura_dom.render(component)
        self.assertEqual(component.x, 10)
