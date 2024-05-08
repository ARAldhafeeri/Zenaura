from zenui.tags import Element, Attribute
from zenui.compiler import ZenuiCompiler
import unittest

class ZenuiCompilerTests(unittest.TestCase):
    def setUp(self):
        self.compiler = ZenuiCompiler()
        
    def test_compile_simple_element(self):
        elm = Element("div")
        result = self.compiler.compile(elm, False)
        self.assertEqual(result, "<div></div>")

    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.children.append(Attribute("styles", "my-paragraph"))
        elm.children.append(Attribute("id", "main-content"))
        result = self.compiler.compile(elm, False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    
    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        result = self.compiler.compile(elm, False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_attributes(self):
        elm = Element("p")
        elm.attributes.append(Attribute("styles", "my-paragraph"))
        elm.attributes.append(Attribute("id", "main-content"))
        result = self.compiler.compile(elm, False)
        self.assertEqual(result, '<p class="my-paragraph" id="main-content"></p>')

    def test_compile_with_children(self):
        div = Element("div")
        span = Element("span", [])
        span.children.append(Element(name="text",children=["Hello"]))
        div.children.append(span)
        result = self.compiler.compile(div, False)
        self.assertEqual(result, "<div><span>Hello</span></div>")

    def test_process_attributes(self):
        attrs = [Attribute("id", "my-element"), Attribute("styles", "important")]
        result = self.compiler.process_attributes(attrs)
        #  note here space is important <div id=....
        self.assertEqual(result, ' id="my-element" class="important"')

    def test_on_event_handlers(self):
        def eventhandler():
            pass
        attrs = [Attribute("id", "my-element"), Attribute("onclick", eventhandler)]
        result = self.compiler.process_attributes(attrs, "MyComp")
        self.assertEqual(result, ' id="my-element" onclick="main.myComp.eventhandler()"')



    