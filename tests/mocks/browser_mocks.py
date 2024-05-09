import unittest.mock
from collections import defaultdict
from zenui.tags import Element


class MockElement:
    def __init__(self, tagName=None, innerHTML=None):
        self.tagName = tagName
        self.innerHTML = None

root = MockElement()

class MockDocument:
    def __init__(self):
        self.elements = defaultdict(lambda: MockElement)
        self.elements["root"] = root
    def getElementById(self, element_id):
        return self.elements.get(element_id)

    def createElement(self, tag_name):
        element = MockElement()
        return element
    
    def querySelector(self, query:str):
        query = query.replace("[", "").replace("]", "").replace('"', "").split("=")
        id = query[-1]
        return self.elements[id]

class MockWindow:
    def __init__(self):
        self.innerWidth = 1024 
        self.innerHeight = 768
        self.location = MockLocation()

class MockLocation:
    def __init__(self):
        self.href = "http://localhost:8000"  # Example
