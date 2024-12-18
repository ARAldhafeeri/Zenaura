import asyncio
from unittest.mock import MagicMock
from collections import defaultdict

class Content:
    def __init__(self):
        self.firstChild = ""


class MockTextNode:
    def __init__(self, text):
        self.nodeValue = text
        self.parentNode = None


class MockElement:
    def __init__(self, tag_name=None, innerHTML=""):
        self.tagName = tag_name
        self.innerHTML = innerHTML
        self.outerHTML = ""
        self.attributes = {}
        self.childNodes = []
        self.parentNode = None
        self.content = Content()
        self.eventListeners = defaultdict(list)  
    
    def setAttribute(self, name, value):
        self.attributes[name] = value

    def getAttribute(self, name):
        return self.attributes.get(name)

    def removeAttribute(self, name):
        self.attributes.pop(name, None)

    def appendChild(self, child):
        if child not in self.childNodes:
            self.childNodes.append(child)
            if isinstance(child, MockElement):
                child.parentNode = self

    def removeChild(self, child):
        if child in self.childNodes:
            self.childNodes.remove(child)
            child.parentNode = None

    def createElement(self, tag_name):
        return MockElement(tag_name)

    def addEventListener(self, event, callback):
        self.eventListeners[event].append(callback)

    def dispatchEvent(self, event):
        for callback in self.eventListeners.get(event, []):
            callback(event)

    def __repr__(self):  
        return f"<MockElement '{self.tagName}'>"

class MockDocument:
    def __init__(self):
        self.body = MockElement("body")
        self.elementsById = {"root": self.body}
        self.title = ""
        self.readyState = "loading"  
        self.eventListeners = defaultdict(list)

    def getElementById(self, element_id):
        return self.elementsById.get(element_id)

    def createElement(self, tag_name):
        return MockElement(tag_name)

    def createTextNode(self, txt):
        return MockTextNode(txt)

    def setElementById(self, element_id, element):
        self.elementsById[element_id] = element

    def addEventListener(self, event, callback):
        self.eventListeners[event].append(callback)

    def querySelector(self, query: str):
        query = query.replace("[", "").replace("]", "").replace('"', "").split("=")
        id = query[-1]
        return self.elementsById.get(id)

    def dispatchEvent(self, event):
        for callback in self.eventListeners.get(event, []):
            callback(event)

class MockLocation:
    def __init__(self):
        self.href = "http://localhost:8000"
        self.pathname = ""

class MockWindowHistory:
    def __init__(self):
        self.history = []

    def pushState(self, *args, **kwargs):
        self.history.append([args, kwargs])

class MockWindow:
    def __init__(self):
        self.innerWidth = 1024
        self.innerHeight = 768
        self.location = MockLocation()
        self.history = MockWindowHistory()
        self.eventListeners = defaultdict(list)

    def addEventListener(self, event, callback):
        self.eventListeners[event].append(callback)

    def dispatchEvent(self, event):
        for callback in self.eventListeners.get(event, []):
            callback(event)

def create_proxy(callback):
    def wrapper(event):
        callback(event)
    return wrapper