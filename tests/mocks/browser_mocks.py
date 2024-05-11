import unittest.mock
from collections import defaultdict


class MockNode:
    def __init__(self, tagName=None, innerHTML=None):
        self.tagName = tagName
        self.innerHTML = None

root = MockNode()

class MockDocument:
    def __init__(self):
        self.nodes = defaultdict(lambda: MockNode)
        self.nodes["root"] = root
    def getNodeById(self, node_id):
        return self.nodes.get(node_id)

    def createNode(self, tag_name):
        node = MockNode()
        return node
    
    def querySelector(self, query:str):
        query = query.replace("[", "").replace("]", "").replace('"', "").split("=")
        id = query[-1]
        return self.nodes[id]

class MockWindow:
    def __init__(self):
        self.innerWidth = 1024 
        self.innerHeight = 768
        self.location = MockLocation()

class MockLocation:
    def __init__(self):
        self.href = "http://localhost:8000"  # Example
