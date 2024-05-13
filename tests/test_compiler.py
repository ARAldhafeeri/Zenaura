from zenaura.client.tags import Node, Attribute
from zenaura.client.compiler import Compiler
import unittest

compiler = Compiler() 

class CompilerTests(unittest.TestCase):
    def test_compile_simple_node(self):
        elm = Node("div")
        result = compiler.compile(elm)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        result = compiler.compile(elm, zenaura_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    
    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        result = compiler.compile(elm, zenaura_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        result = compiler.compile(elm, zenaura_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_process_attributes(self):
        attrs = [Attribute("id", "my-node"), Attribute("styles", "important")]
        result = compiler.process_attributes(attrs)
        #  note here space is important <div id=....
        self.assertEqual(result, ' id="my-node" class="important"')

    def test_compile_with_children(self):
        div = Node("div")
        span = Node("span")
        span.children = [
            "Hello"
        ]
        div.children.append(span)
        result = compiler.compile(div, zenaura_dom_mode=False)
        self.assertEqual(result, "<div><span>Hello</span></div>")
    
    def test_sanitize_html(self):
        input_html = '<script>alert("XSS attack")</script>'
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '&lt;script&gt;alert(&quot;XSS attack&quot;)&lt;/script&gt;')

    def test_compile_with_component_name(self):
        elm = Node("button")
        elm.attributes.append(Attribute("onclick", "counter.handleClick"))
        result = compiler.compile(elm, componentName="myButton", zenaura_dom_mode=False)
        expected_output = '<button onclick="counter.handleClick"></button>'
        self.assertEqual(result, expected_output)

    def test_process_attributes_with_keywords(self):
        attrs = [Attribute("styles", "my-button"), Attribute("id", "btn-1")]
        result = compiler.process_attributes(attrs)
        self.assertEqual(result, ' class="my-button" id="btn-1"')

    def test_compile_with_nested_elements(self):
        div = Node("div")
        span = Node("span")
        span.children = ["Hello"]
        div.children.append(span)
        result = compiler.compile(div, zenaura_dom_mode=False)
        self.assertEqual(result, "<div><span>Hello</span></div>")


    def test_sanitize_empty_input(self):
        input_html = ''
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '')

    def test_sanitize_input_with_special_characters(self):
        input_html = '<>&"'
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '&lt;&gt;&amp;&quot;')

    def test_compile_node_with_no_attributes_or_children(self):
        elm = Node("div")
        result = compiler.compile(elm, zenaura_dom_mode=False)
        self.assertEqual(result, "<div></div>")

    def test_process_attributes_with_no_attrs(self):
        attrs = []
        result = compiler.process_attributes(attrs)
        self.assertEqual(result, '')

    def test_compile_with_no_children(self):
        elm = Node("div")
        result = compiler.compile(elm, zenaura_dom_mode=False)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_very_nested_complex_structure_and_attributes(self):
        root = Node("div")
        child1 = Node("div")
        child2 = Node("div")
        grandchild1 = Node("span")
        grandchild2 = Node("a")
        grandchild2.attributes.append(Attribute("href", "https://example.com"))
        grandchild2.children = ["Link"]
        grandchild3 = Node("img")
        grandchild3.attributes.append(Attribute("src", "image.jpg"))
        grandchild3.attributes.append(Attribute("alt", "Image"))
        grandchild1.children = ["Hello"]
        child1.children.extend([grandchild1, grandchild2, grandchild3])
        root.children.extend([child1, child2])
        result = compiler.compile(root, zenaura_dom_mode=False)
        expected_output = '<div><div><span>Hello</span><a href="https://example.com">Link</a><img src="image.jpg" alt="Image"></div><div></div></div>'
        self.assertEqual(result, expected_output)


    def test_compile_with_even_more_nested_structure(self):
        root = Node("div")
        child1 = Node("div")
        child2 = Node("div")
        grandchild1 = Node("span")
        grandchild2 = Node("a")
        grandchild2.attributes.append(Attribute("href", "https://example.com"))
        grandchild2.children = ["Link"]
        grandchild3 = Node("img")
        grandchild3.attributes.append(Attribute("src", "image.jpg"))
        grandchild3.attributes.append(Attribute("alt", "Image"))
        grandchild1.children = ["Hello"]
        child1.children.extend([grandchild1, grandchild2, grandchild3])
        root.children.extend([child1, child2])

        greatGrandchild1 = Node("div")
        greatGrandchild2 = Node("div")
        greatGrandchild3 = Node("div")
        greatGrandchild1.children.extend([greatGrandchild2, greatGrandchild3])
        grandchild2.children.extend([greatGrandchild1])

        result = compiler.compile(root, zenaura_dom_mode=False)
        
        expected_output = '<div><div><span>Hello</span><a href="https://example.com">Link<div><div></div><div></div></div></a><img src="image.jpg" alt="Image"></div><div></div></div>'
        self.assertEqual(result, expected_output)