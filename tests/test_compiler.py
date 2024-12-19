import unittest
import time 
import sys
import random
import string
from zenaura.client.tags import Node, Attribute
from zenaura.client.compiler import Compiler


compiler = Compiler() 

class CompilerTests(unittest.TestCase):
    def test_compile_simple_render(self):
        elm = Node("div")
        result = compiler.compile(elm)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.append_child(Attribute("styles", "my-paragraph"))
        elm.append_child(Attribute("id", "main-content"))
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
            Node(text="Hello")
        ]
        div.append_child(span)
        result = compiler.compile(div, zenaura_dom_mode=False)
        self.assertEqual(result, "<div><span>Hello</span></div>")
    
    def test_sanitize_html(self):
        input_html = '<script>alert("XSS attack")</script>'
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '&lt;script&gt;alert("XSS attack")&lt;/script&gt;')


    def test_process_attributes_with_keywords(self):
        attrs = [Attribute("styles", "my-button"), Attribute("id", "btn-1")]
        result = compiler.process_attributes(attrs)
        self.assertEqual(result, ' class="my-button" id="btn-1"')

    def test_compile_with_nested_elements(self):
        div = Node("div")
        span = Node("span")
        span.children = [Node(text="Hello")]
        div.append_child(span)
        result = compiler.compile(div, zenaura_dom_mode=False)
        self.assertEqual(result, "<div><span>Hello</span></div>")


    def test_sanitize_empty_input(self):
        input_html = ''
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '')

    def test_sanitize_input_with_special_characters(self):
        input_html = '<>&"'
        result = compiler.sanitize(input_html)
        self.assertEqual(result, '&lt;&gt;&amp;"')

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
        grandchild2.children = [Node(text="Link")]
        grandchild3 = Node("img")
        grandchild3.attributes.append(Attribute("src", "image.jpg"))
        grandchild3.attributes.append(Attribute("alt", "Image"))
        grandchild1.children = [Node(text="Hello")]
        child1.children.extend([grandchild1, grandchild2, grandchild3])
        root.children.extend([child1, child2])
        result = compiler.compile(root, zenaura_dom_mode=False)
        expected_output = '<div><div><span>Hello</span><a href="https://example.com">Link</a><img src="image.jpg" alt="Image" /></div><div></div></div>'
        self.assertEqual(result, expected_output)


    def test_compile_with_even_more_nested_structure(self):
        root = Node("div")
        child1 = Node("div")
        child2 = Node("div")
        grandchild1 = Node("span")
        grandchild2 = Node("a")
        grandchild2.attributes.append(Attribute("href", "https://example.com"))
        grandchild2.children = [Node(text="Link")]
        grandchild3 = Node("img")
        grandchild3.attributes.append(Attribute("src", "image.jpg"))
        grandchild3.attributes.append(Attribute("alt", "Image"))
        grandchild1.children = [Node(text="Hello")]
        child1.children.extend([grandchild1, grandchild2, grandchild3])
        root.children.extend([child1, child2])

        greatGrandchild1 = Node("div")
        greatGrandchild2 = Node("div")
        greatGrandchild3 = Node("div")
        greatGrandchild1.children.extend([greatGrandchild2, greatGrandchild3])
        grandchild2.children.extend([greatGrandchild1])

        result = compiler.compile(root, zenaura_dom_mode=False)
        
        expected_output = '<div><div><span>Hello</span><a href="https://example.com">Link<div><div></div><div></div></div></a><img src="image.jpg" alt="Image" /></div><div></div></div>'
        self.assertEqual(result, expected_output)

    def test_compile_with_very_large_structure(self):
        root = Node("div", attributes=[Attribute("id", "root")])
        parent = root

    # Function to generate random attributes
        def generate_attributes(num_attributes):
            attributes = []
            for _ in range(num_attributes):
                key = ''.join(random.choices(string.ascii_lowercase, k=5))  # Random 5-letter key
                value = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Random 10-char value
                attributes.append(Attribute(key, value))
            return attributes

        # Create 10 levels of nested divs, each with 10 children, and attributes
        for level in range(10):
            for i in range(10):
                child = Node("div", attributes=generate_attributes(3))  # 3 attributes per child
                parent.append_child(child)
            parent = child
    
        # Add some content to the leaf nodes
        for child in parent.children:
            child.append_child("Some content")

        # Benchmark compilation time
        start_time = time.time()  # Start timer
        result = compiler.compile(root, zenaura_dom_mode=True)
        end_time = time.time()  # End timer
        compilation_time = end_time - start_time

        # Assert the size of the generated HTML
        self.assertGreater(0.1, compilation_time)
        self.assertLess(sys.getsizeof(result), 30000)  # Adjust the threshold as needed

