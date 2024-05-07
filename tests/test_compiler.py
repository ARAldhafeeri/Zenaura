from zenui.tags import Element, Child, Attribute
from zenui.compiler import ZenuiCompiler
import unittest

class ZenuiCompilerTests(unittest.TestCase):
    def test_compile_simple_element(self):
        elm = Element("div", children=[])
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Element("p", children=[])
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    
    def test_compile_with_attributes(self):
        elm = Element("p", children=[])
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_attributes(self):
        elm = Element("p", children=[])
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        compiler = ZenuiCompiler()
        result = compiler.compile(elm)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_children(self):
        div = Element("div", children=[])
        span = Element("span", [])
        span.children.append(Element(name="text",children=["Hello"]))
        div.children.append(span)
        compiler = ZenuiCompiler()
        result = compiler.compile(div)
        self.assertEqual(result, "<div><span>Hello</span></div>")

    def test_split_children_attributes(self):
        elm = Element("div", children=[])
        elm.children.append(Element(name="text", children=["Text content"]))
        elm.children.append(Attribute("styles", "container"))
        compiler = ZenuiCompiler()
        children, attributes = compiler.split_children_attributes(elm)
        self.assertEqual(children, [Element(name="text", children=["Text content"])])
        self.assertEqual(attributes, [Attribute("styles", "container")])

    def test_process_attributes(self):
        attrs = [Attribute("id", "my-element"), Attribute("styles", "important")]
        compiler = ZenuiCompiler()
        result = compiler.process_attributes(attrs)
        #  note here space is important <div id=....
        self.assertEqual(result, ' id="my-element" class="important"')

    def test_process_attributes_with_styles(self):
        attrs = [Attribute("styles", "color")]
        compiler = ZenuiCompiler()
        result = compiler.process_attributes(attrs)
        #  same <div|space| attrs... only for indexed-0 attr
        self.assertEqual(result, ' class="color"')

    