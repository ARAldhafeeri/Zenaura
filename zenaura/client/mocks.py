class Content:
    """
    Represents the content of an element.

    Attributes:
        firstChild (str): The text content of the first child element.
    """

    def __init__(self):
        self.firstChild = ""


class MockTextNode:
    """
    Represents a text node in the DOM.

    Attributes:
        nodeValue (str): The text content of the node.
        parentNode (MockElement): The parent element of the node.
    """

    def __init__(self, text):
        self.nodeValue = text
        self.parentNode = None


class MockElement:
    """
    Represents an HTML element in the DOM.

    Attributes:
        tagName (str): The tag name of the element.
        innerHTML (str): The HTML content of the element.
        outerHTML (str): The complete HTML representation of the element, including its children.
        attributes (dict): A dictionary of the element's attributes.
        childNodes (list): A list of the element's child nodes.
        parentNode (MockElement): The parent element of the node.
        content (Content): The content of the element.
    """

    def __init__(self, tag_name=None, innerHTML=""):
        self.tagName = tag_name
        self.innerHTML = innerHTML
        self.outerHTML = ""
        self.attributes = {}
        self.childNodes = []
        self.parentNode = None
        self.content = Content()

    def setAttribute(self, name, value):
        """
        Sets the value of an attribute on the element.

        Args:
            name (str): The name of the attribute.
            value (str): The value of the attribute.
        """

        self.attributes[name] = value

    def getAttribute(self, name):
        """
        Gets the value of an attribute on the element.

        Args:
            name (str): The name of the attribute.

        Returns:
            str: The value of the attribute, or None if the attribute does not exist.
        """

        return self.attributes.get(name)

    def removeAttribute(self, name):
        """
        Removes an attribute from the element.

        Args:
            name (str): The name of the attribute.
        """

        self.attributes.pop(name, None)

    def appendChild(self, child):
        """
        Appends a child node to the element.

        Args:
            child (MockElement or MockTextNode): The child node to append.
        """

        if child not in self.childNodes:
            self.childNodes.append(child)
            if isinstance(child, MockElement):
                child.parentNode = self

    def removeChild(self, child):
        """
        Removes a child node from the element.

        Args:
            child (MockElement or MockTextNode): The child node to remove.
        """

        if child in self.childNodes:
            self.childNodes.remove(child)
            child.parentNode = None

    def createElement(self, tag_name):
        """
        Creates a new MockElement with the given tag name.

        Args:
            tag_name (str): The tag name of the new element.

        Returns:
            MockElement: The newly created element.
        """

        return MockElement(tag_name)

    def __repr__(self):  # Helpful for debugging
        return f"<MockElement '{self.tagName}'>"


class MockDocument:  # Use MagicMock for flexibility
    """
    Represents the HTML document object model (DOM).

    Attributes:
        body (MockElement): The body element of the document.
        elementsById (dict): A dictionary of elements in the document, indexed by their ID.
        title (str): The title of the document.
    """

    def __init__(self):
        self.body = MockElement("body")  # Create a body element
        self.elementsById = {"root": self.body}  # Store elements by ID
        self.title = ""
        self.readyStatus = "interactive"

    def getElementById(self, element_id):
        """
        Gets the element with the given ID.

        Args:
            element_id (str): The ID of the element.

        Returns:
            MockElement: The element with the given ID, or None if the element does not exist.
        """

        return self.elementsById.get(element_id)

    def createElement(self, tag_name):
        """
        Creates a new MockElement with the given tag name.

        Args:
            tag_name (str): The tag name of the new element.

        Returns:
            MockElement: The newly created element.
        """

        return MockElement(tag_name)

    def setElementById(self, element_id, element):
        """
        Sets the element with the given ID.

        Args:
            element_id (str): The ID of the element.
            element (MockElement): The element to set.
        """

        # for mocking purposes
        self.elementsById[element_id] = element

    def createTextNode(self, txt):
        """
        Creates a new MockTextNode with the given text.

        Args:
            txt (str): The text content of the new node.

        Returns:
            MockTextNode: The newly created node.
        """

        textNode = MockTextNode(txt)
        return textNode

    def querySelector(self, query: str):
        """
        Selects the first element that matches the given CSS selector.

        Args:
            query (str): The CSS selector to use.

        Returns:
            MockElement: The first element that matches the selector, or None if no element matches.
        """

        query = query.replace("[", "").replace("]", "").replace('"', "").split("=")
        id = query[-1]
        if id in self.elementsById:
            return self.elementsById[id]
        return False


class MockLocation:
    """
    Represents the location object of the browser window.

    Attributes:
        href (str): The URL of the current page.
        pathname (str): The path portion of the URL.
    """

    def __init__(self):
        self.href = "http://localhost:8000"  # Example
        self.pathname = ""


class MockWindowHistory:
    """
    Represents the history object of the browser window.

    Attributes:
        history (list): A list of the pages that have been visited.
    """

    def __init__(self):
        self.history = []

    def pushState(self, *args, **kwargs):
        """
        Adds a new entry to the history stack.

        Args:
            *args: Arguments to be passed to the history.pushState() method.
            **kwargs: Keyword arguments to be passed to the history.pushState() method.
        """

        self.history.append([args, kwargs])


class MockWindow:
    """
    Represents the browser window object.

    Attributes:
        innerWidth (int): The width of the window in pixels.
        innerHeight (int): The height of the window in pixels.
        location (MockLocation): The location object of the window.
        history (MockWindowHistory): The history object of the window.
    """

    def __init__(self):
        self.innerWidth = 1024
        self.innerHeight = 768
        self.location = MockLocation()
        self.history = MockWindowHistory()
