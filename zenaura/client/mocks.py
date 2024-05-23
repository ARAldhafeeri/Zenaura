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
    

    def __repr__(self):  # Helpful for debugging
        return f"<MockElement '{self.tagName}'>"

class MockDocument:  # Use MagicMock for flexibility
    def __init__(self):
        self.body = MockElement("body")  # Create a body element
        self.elementsById = {"root": self.body}  # Store elements by ID
        self.title = ""

    def getElementById(self, element_id):
        return self.elementsById.get(element_id)

    def createElement(self, tag_name):
        return MockElement(tag_name)
    
    def setElementById(self, element_id, element):
        # for mocking purposes
        self.elementsById[element_id] = element

    def createTextNode(self,txt):
        textNode = MockTextNode(txt)
        return textNode

    def querySelector(self, query:str):
        query = query.replace("[", "").replace("]", "").replace('"', "").split("=")
        id = query[-1]
        return self.elementsById[id]

class MockLocation:
    def __init__(self):
        self.href = "http://localhost:8000"  # Example
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
