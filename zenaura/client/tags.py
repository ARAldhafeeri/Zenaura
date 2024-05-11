import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Child:
    def __init__(self,name : str, children=None, attributes=None):
        """
        Initializes a Child object with the given name, children, and attributes.

        Args:
        name (str): The name of the child.
        children (list, optional): List of children nodes. Defaults to None.
        attributes (list, optional): List of attributes. Defaults to None.
        """
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes

    
class Attribute:
    def __init__(self, key, value):
        """
        Initializes an Attribute object with the given key and value.

        Args:
        key: The key of the attribute.
        value: The value of the attribute.
        """
        self.key = key
        self.value = value


class Node:
    def __init__(self,name : str, children: Optional[List[Attribute]]=None, attributes : Optional[List[Attribute]]=None):
        """
        Initializes a Node object with the given name, children, and attributes.

        Args:
        name (str): The name of the node.
        children (list, optional): List of children nodes. Defaults to None.
        attributes (list, optional): List of attributes. Defaults to None.
        """
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes
        self.nodeId = uuid.uuid4().hex

class TagBuilder:
    def __init__(self, name : str) -> None:
        """
        Initializes a TagBuilder object with the given name.

        Args:
        name (str): The name of the tag.
        """
        self.node = Node(name)
    
    def with_attribute(self, key : str, value : any) -> "TagBuilder":
        """
        Adds an attribute to the tag.

        Args:
        key (str): The key of the attribute.
        value: The value of the attribute.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        self.node.attributes.append(Attribute(key,value))
        return self
    
    def with_child(self, child : Node) -> "TagBuilder":
        """
        Adds a child node to the tag.

        Args:
        child (Node): The child node to be added.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        self.node.children.append(child)
        return self 
    
    def with_styles(self, styles: dict) -> "TagBuilder":
        """
        Adds styles to the tag.

        Args:
        styles (dict): Dictionary of styles.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
        self.node.attributes.append(Attribute("style", style_str))
        return self
    
    def with_classes(self, *class_names: str) -> "TagBuilder":

        """
        Adds multiple class names to the element.

        Args:
        *class_names (str): Variable number of class names.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        for class_name in class_names:
            self.with_class(class_name)
        return self
    
    def with_class(self, class_name: str) -> "TagBuilder":
        """
        Adds a single class name to the element.

        Args:
        class_name (str): The class name to be added.

        Returns:
        TagBuilder: The TagBuilder object.
        """
        for i in self.node.attributes:
            if i.key =="class":
                if class_name not in i.value:
                    i.value = i.value + " " +  class_name
                    return self
        self.node.attributes.append(Attribute("class", class_name))
       
        return self

    
    def build(self):
        """
        Builds and returns the node.

        Returns:
        Node: The built node.
        """
        return self.node


       

class HTMLTags:
    """
        html tags factory
    """
    def __init__(self):
        """
            Initializes the HTMLTags object with various tag builders for HTML elements.
        """
        self.html =  TagBuilder("html")
        self.head = TagBuilder("head")
        self.body = TagBuilder("body")

        # Core structural tags
        self.a = TagBuilder("a")
        self.div = TagBuilder("div")
        self.p = TagBuilder("p")
        self.img = TagBuilder("img")
        self.span = TagBuilder("span")
        self.h1 = TagBuilder("h1") 
        self.h2 = TagBuilder("h2")
        self.h3 = TagBuilder("h3")
        self.h4 = TagBuilder("h4")
        self.h5 = TagBuilder("h5")
        self.h6 = TagBuilder("h6")

        # Text formatting tags
        self.abbr = TagBuilder("abbr")
        self.acronym = TagBuilder("acronym")  
        self.address = TagBuilder("address")
        self.b = TagBuilder("b")
        self.bdi = TagBuilder("bdi")
        self.bdo = TagBuilder("bdo")
        self.blockquote = TagBuilder("blockquote")
        self.cite = TagBuilder("cite")
        self.code = TagBuilder("code")
        self.del_ = TagBuilder("del")  # Using del_ since 'del' is a Python keyword
        self.dfn = TagBuilder("dfn")
        self.em = TagBuilder("em")
        self.i = TagBuilder("i")
        self.ins = TagBuilder("ins")
        self.kbd = TagBuilder("kbd")
        self.mark = TagBuilder("mark")
        self.pre = TagBuilder("pre")
        self.q = TagBuilder("q")
        self.rp = TagBuilder("rp")
        self.rt = TagBuilder("rt")
        self.ruby = TagBuilder("ruby")
        self.s = TagBuilder("s")
        self.samp = TagBuilder("samp")
        self.small = TagBuilder("small")
        self.strong = TagBuilder("strong")
        self.sub = TagBuilder("sub")
        self.sup = TagBuilder("sup")
        self.time = TagBuilder("time")
        self.u = TagBuilder("u")
        self.var = TagBuilder("var")

        # List tags
        self.ul = TagBuilder("ul")
        self.ol = TagBuilder("ol")
        self.li = TagBuilder("li")
        self.dl = TagBuilder("dl")
        self.dt = TagBuilder("dt")
        self.dd = TagBuilder("dd")

        # Form tags
        self.form = TagBuilder("form")
        self.input = TagBuilder("input")
        self.textarea = TagBuilder("textarea")
        self.button = TagBuilder("button")
        self.label = TagBuilder("label")
        self.select = TagBuilder("select")
        self.optgroup = TagBuilder("optgroup")
        self.option = TagBuilder("option")
        self.fieldset = TagBuilder("fieldset")
        self.legend = TagBuilder("legend")

        # Other common tags
        self.table = TagBuilder("table")
        self.thead = TagBuilder("thead")
        self.tbody = TagBuilder("tbody")
        self.tfoot = TagBuilder("tfoot")
        self.tr = TagBuilder("tr")
        self.th = TagBuilder("th")
        self.td = TagBuilder("td")
        self.caption = TagBuilder("caption")
        self.colgroup = TagBuilder("colgroup")
        self.col = TagBuilder("col")

        # Media tags
        self.audio = TagBuilder("audio")
        self.video = TagBuilder("video")
        self.source = TagBuilder("source")
        self.track = TagBuilder("track")
        self.embed = TagBuilder("embed")
        self.object = TagBuilder("object")
        self.param = TagBuilder("param")
        self.picture = TagBuilder("picture")

        # Semantic/specialized tags
        self.section = TagBuilder("section")
        self.article = TagBuilder("article")
        self.aside = TagBuilder("aside")
        self.header = TagBuilder("header")
        self.footer = TagBuilder("footer")
        self.nav = TagBuilder("nav")
        self.figure = TagBuilder("figure")
        self.figcaption = TagBuilder("figcaption")
        self.main = TagBuilder("main")
        self.details = TagBuilder("details")
        self.summary = TagBuilder("summary")
        self.dialog = TagBuilder("dialog")

        # Deprecated tags (avoid using)
        self.basefont = TagBuilder("basefont") 
        self.big = TagBuilder("big")
        self.center = TagBuilder("center")
        self.font = TagBuilder("font")
        self.strike = TagBuilder("strike")
        self.tt = TagBuilder("tt")