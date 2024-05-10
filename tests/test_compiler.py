from zenui.tags import Node, Child, Attribute
from zenui.compiler import ZenuiCompiler
import unittest

class ZenuiCompilerTests(unittest.TestCase):
    def test_compile_simple_node(self):
        elm = Node("div")
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm, zenui_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    
    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm, zenui_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_attributes(self):
        elm = Node("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm, zenui_dom_mode=False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_process_attributes(self):
        attrs = [Attribute("id", "my-node"), Attribute("styles", "important")]
        compiler = ZenuiCompiler()
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
        compiler = ZenuiCompiler()
        result = compiler.compile(div, zenui_dom_mode=False)
        self.assertEqual(result, "<div><span>Hello</span></div>")
    