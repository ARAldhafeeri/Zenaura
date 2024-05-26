import sys
import unittest
from unittest.mock import patch  # For patching the global document object
from zenaura.client.tags import Node, Attribute  # Assuming these exist in your project
from zenaura.client.hydrator import HydratorRealDomAdapter
from zenaura.client.config import ZENAURA_DOM_ATTRIBUTE
from unittest.mock import patch, MagicMock
from tests.mocks.browser_mocks import MockDocument, MockElement, MockTextNode
from zenaura.client.tags import Node


sys.modules["pyscript"] = MagicMock()

class TestHydratorRealDomAdapter(unittest.TestCase):
    def setUp(self):
        self.mock_document = MockDocument()
        
        # Patch the global document object to use our mock
        self.patcher = patch("zenaura.client.hydrator.real_dom_adapter.document", self.mock_document)
        self.patcher.start()

        self.hydrator = HydratorRealDomAdapter()


    def tearDown(self):
        self.patcher.stop()  # Restore the original document after each test

    def test_hyd_rdom_create_element(self):
        virtual_node = Node("div")
        element = self.hydrator.hyd_rdom_create_element(virtual_node)
        self.assertTrue(element)
        self.assertEqual(element.tagName, "div")

    def test_hyd_rdom_attach_to_root(self):
        html = "<p>Test content</p>"
        self.hydrator.hyd_rdom_attach_to_root(html)
        root_element = self.mock_document.getElementById("root")
        self.assertEqual(root_element.innerHTML, html)

    def test_hyd_rdom_attach_to_mounted_comp(self):
        parent_div = self.mock_document.createElement("div")

        parent_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "parent-comp")
        self.mock_document.setElementById("parent_comp", parent_div)

        child_html = "<span>Child content</span>"
        self.hydrator.hyd_rdom_attach_to_mounted_comp("parent_comp", child_html)

        self.assertEqual(parent_div.outerHTML, child_html)
    
    def test_hyd_rdom_set_attribute(self):
        element = self.mock_document.createElement("div")
        element.setAttribute(ZENAURA_DOM_ATTRIBUTE, "my-comp")
        self.mock_document.setElementById("my-comp", element)

        attribute = Attribute(key="class", value="test-class")
        self.hydrator.hyd_rdom_set_attribute("my-comp", attribute)
        self.assertEqual(element.getAttribute("class"), "test-class")

    def test_hyd_rdom_remove_attribute(self):
        element = self.mock_document.createElement("div")
        element.setAttribute(ZENAURA_DOM_ATTRIBUTE, "my-comp")
        element.setAttribute("data-test", "some-value")
        self.mock_document.setElementById("my-comp", element)
        
        self.hydrator.hyd_rdom_remove_attribute("my-comp", "data-test")
        self.assertIsNone(element.getAttribute("data-test"))  # Ensure attribute is removed

    def test_hyd_rdom_remove_element(self):
        parent_div = self.mock_document.createElement("div")
        child_div = self.mock_document.createElement("div")
        child_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "child-comp")
        parent_div.appendChild(child_div)
        self.mock_document.setElementById("parent-comp", parent_div)
        self.mock_document.setElementById("child-comp", child_div)

        self.hydrator.hyd_rdom_remove_element("child-comp")
        self.assertEqual(len(parent_div.childNodes), 0)  # Child should be removed

    def test_hyd_rdom_append_child(self):
        parent_div = self.mock_document.createElement("div")
        parent_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "parent-comp")
        self.mock_document.setElementById("parent-comp", parent_div)

        child_html = "<span>Child content</span>"
        self.hydrator.hyd_rdom_append_child("parent-comp", child_html)
        self.assertEqual(len(parent_div.childNodes), 1)  # Should have one child

    def test_hyd_rdom_remove_child(self):
        parent_div = self.mock_document.createElement("div")
        parent_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "parent-comp")

        child_div = self.mock_document.createElement("div")
        child_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "child-comp")
        parent_div.appendChild(child_div)

        self.mock_document.setElementById("parent-comp", parent_div)
        self.mock_document.setElementById("child-comp", child_div)

        self.hydrator.hyd_rdom_remove_child("child-comp")
        self.assertEqual(child_div.outerHTML, "")  # Child should be removed
    
    #  New test for hyd_rdom_add_text_node
    def test_hyd_rdom_add_text_render(self):
        parent_div = self.mock_document.createElement("div")
        parent_div.setAttribute(ZENAURA_DOM_ATTRIBUTE, "parent-comp")
        self.mock_document.setElementById("parent-comp", parent_div)
        text_content = "Some text"
        self.hydrator.hyd_rdom_add_text_render("parent-comp", text_content)
        self.assertEqual(len(parent_div.childNodes), 1)
        self.assertEqual(parent_div.childNodes[0].nodeValue, text_content)


    def test_hyd_rdom_replace_inner_text(self):
        element = self.mock_document.createElement("div")
        element.setAttribute(ZENAURA_DOM_ATTRIBUTE, "my-comp")
        existing_text = "Existing text"
        self.mock_document.setElementById("my-comp", element)
        self.hydrator.hyd_rdom_replace_inner_text("my-comp", existing_text)  # Add initial text node

        new_text = "New text"
        self.hydrator.hyd_rdom_replace_inner_text("my-comp", new_text)

        # Assertions:
        self.assertEqual(element.textContent, new_text)  # Text should be replaced

if __name__ == "__main__":
    unittest.main()
