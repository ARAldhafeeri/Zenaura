import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class Child:
    def __init__(self,name : str, children=None, attributes=None):
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes

    
class Attribute:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class Node:
    def __init__(self,name : str, children: Optional[List[Attribute]]=None, attributes : Optional[List[Attribute]]=None):
        self.name = name
        self.children = [] if children is None else children
        self.attributes = [] if attributes is None else attributes
        self.nodeId = uuid.uuid4().hex

class TagBuilder:
    def __init__(self, name : str) -> None:
        self.node = Node(name)
    
    def with_attribute(self, key : str, value : any) -> "TagBuilder":
        self.node.attributes.append(Attribute(key,value))
        return self
    
    def with_child(self, child : Node) -> "TagBuilder":
        self.node.children.append(child)
        return self 
    
    def with_styles(self, styles: dict) -> "TagBuilder":
        style_str = ";".join([f"{k}:{v}" for k, v in styles.items()])
        self.element.attributes.append(Attribute("style", style_str))
        return self
    
    def with_classes(self, *class_names: str) -> "TagBuilder":
        """Adds multiple class names to the element"""
        for class_name in class_names:
            self.with_class(class_name)
        return self
    
    def with_class(self, class_name: str) -> "TagBuilder":
        """Adds a single class name to the element"""
        existing_classes = ""
        for i in self.element.attributes:
            if i =="class":
                existing_classes = i
                break
        class_list = existing_classes.split(" ")

        if class_name not in class_list:
            class_list.append(class_name)

        self.element.attributes["class"] = " ".join(class_list)
        return self

    
    def build(self):
        return self.node


       

class HTMLTags:
    """
        html tags exported as TagBuilder
        for faster coding
        exported as Blueprint
    """
    html = TagBuilder("html")
    head = TagBuilder("head")
    body = TagBuilder("body")

    # Core structural tags
    a = TagBuilder("a")
    div = TagBuilder("div")
    p = TagBuilder("p")
    img = TagBuilder("img")
    span = TagBuilder("span")
    h1 = TagBuilder("h1") 
    h2 = TagBuilder("h2")
    h3 = TagBuilder("h3")
    h4 = TagBuilder("h4")
    h5 = TagBuilder("h5")
    h6 = TagBuilder("h6")

    # Text formatting tags
    abbr = TagBuilder("abbr")
    acronym = TagBuilder("acronym")  
    address = TagBuilder("address")
    b = TagBuilder("b")
    bdi = TagBuilder("bdi")
    bdo = TagBuilder("bdo")
    blockquote = TagBuilder("blockquote")
    cite = TagBuilder("cite")
    code = TagBuilder("code")
    del_ = TagBuilder("del")  # Using del_ since 'del' is a Python keyword
    dfn = TagBuilder("dfn")
    em = TagBuilder("em")
    i = TagBuilder("i")
    ins = TagBuilder("ins")
    kbd = TagBuilder("kbd")
    mark = TagBuilder("mark")
    pre = TagBuilder("pre")
    q = TagBuilder("q")
    rp = TagBuilder("rp")
    rt = TagBuilder("rt")
    ruby = TagBuilder("ruby")
    s = TagBuilder("s")
    samp = TagBuilder("samp")
    small = TagBuilder("small")
    strong = TagBuilder("strong")
    sub = TagBuilder("sub")
    sup = TagBuilder("sup")
    time = TagBuilder("time")
    u = TagBuilder("u")
    var = TagBuilder("var")

    # List tags
    ul = TagBuilder("ul")
    ol = TagBuilder("ol")
    li = TagBuilder("li")
    dl = TagBuilder("dl")
    dt = TagBuilder("dt")
    dd = TagBuilder("dd")

    # Form tags
    form = TagBuilder("form")
    input = TagBuilder("input")
    textarea = TagBuilder("textarea")
    button = TagBuilder("button")
    label = TagBuilder("label")
    select = TagBuilder("select")
    optgroup = TagBuilder("optgroup")
    option = TagBuilder("option")
    fieldset = TagBuilder("fieldset")
    legend = TagBuilder("legend")

    # Other common tags
    table = TagBuilder("table")
    thead = TagBuilder("thead")
    tbody = TagBuilder("tbody")
    tfoot = TagBuilder("tfoot")
    tr = TagBuilder("tr")
    th = TagBuilder("th")
    td = TagBuilder("td")
    caption = TagBuilder("caption")
    colgroup = TagBuilder("colgroup")
    col = TagBuilder("col")

    # Media tags
    audio = TagBuilder("audio")
    video = TagBuilder("video")
    source = TagBuilder("source")
    track = TagBuilder("track")
    embed = TagBuilder("embed")
    object = TagBuilder("object")
    param = TagBuilder("param")
    picture = TagBuilder("picture")

    # Semantic/specialized tags
    section = TagBuilder("section")
    article = TagBuilder("article")
    aside = TagBuilder("aside")
    header = TagBuilder("header")
    footer = TagBuilder("footer")
    nav = TagBuilder("nav")
    figure = TagBuilder("figure")
    figcaption = TagBuilder("figcaption")
    main = TagBuilder("main")
    details = TagBuilder("details")
    summary = TagBuilder("summary")
    dialog = TagBuilder("dialog")

    # Deprecated tags (avoid using)
    basefont = TagBuilder("basefont") 
    big = TagBuilder("big")
    center = TagBuilder("center")
    font = TagBuilder("font")
    strike = TagBuilder("strike")
    tt = TagBuilder("tt")

Blueprint = HTMLTags()