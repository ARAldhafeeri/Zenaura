from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Node
from zenaura.client.tags.attribute import Attribute
from zenaura.client.config import self_closing_tags
from functools import partial
from typing import Any, List, Union, Dict
from zenaura.client.compiler.attribute import AttributeProccessor

attribute_processor = AttributeProccessor() 

attribute_processor.attrKeyWords, 
attribute_processor.attrValueWords
def tag(
    name__: str,
    text: str = "",
    *children: Union["Node", str],
    **attributes: Any, 
) -> Node:
  """
    Abstraction on top of builder interface speed up
    developer creating html elements 
     Args:
        name (str): The tag name (e.g., 'div', 'span').
        *children: Child nodes or strings.
        text (str, optional): Text content inside the tag.
        **attributes: Keyword arguments for tag attributes.

    Returns:
        Node: The constructed Node object.
    
    Usage:
      tag1("div", attr1="test", attr2"test", tag("button"), tag("button"), text="123" )
      renders:
        <div attr1="test" attr2="test">
          <button></button>
          <button></button>
          123 
        </div
  """
  builder = Builder(name__)
  if children:
      builder.with_children(*children)
  if attributes:
      builder.with_attributes(**attributes)
  if text:
      builder.with_text(text)
  # print("data", builder.node.children, builder.node.attributes)
  return builder.build()


def self_closing(name__: str, **attributes: Any) -> Node:
    """
        the following element ins html self closing tag
        accept only attributes:
        
    """
    return tag(name__, **attributes)

def self_closing(name__: str, **attributes: Any) -> Node:
    """
    Creates a self-closing {name} element with the specified tag name and attributes.

    Parameters:
        **attributes (Any): html element attrbiutes,
        special attributes keys:
        {[f"html : {k} -> zenaura : {v}" for k,v in attribute_processor.attrKeyWords.items()]}
        special attribute values:
        {[f"html : {k} -> zenaura : {v}" for k,v in attribute_processor.attrValueWords.items()]}
    Returns:
        <{name} [attributes] />

    example:
        {name}(name__="val" hidden=True)
    """
    return tag(name__, **attributes)

def nestable(name__: str, *children: Union[Node, str], **attributes: Any) -> Node:
    """
    Creates a an html {name} element with the specified tag name and attributes.

    Parameters:
        **children (Any): element from zenaura.ui.tags or plain text,
        **attributes (Any): html element attrbiutes,
        special attributes keys:
        {attribute_processor.attrKeyWords}
        special attribute values:
        {attribute_processor.attrValueWords}
    Returns:
        <{name} [attributes]>[children]</{name}>

    example:
        {name}(name__="val" hidden=True, div())
    """
    return tag(name__, None, *children, **attributes)

def textable(name__: str, text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    """
    Creates a an html {name} element with the specified tag name and attributes with text.

    Parameters:
        **children (Any): element from zenaura.ui.tags or plain text,
        **attributes (Any): html element attrbiutes,
        special attributes keys:
        {attribute_processor.attrKeyWords}
        special attribute values:
        {attribute_processor.attrValueWords}
    Returns:
        <{name} [attributes]>[text]</{name}>

    example:
        {name}(name__="val" hidden=True, div())
    """
    return tag(name__, text, *children, **attributes)

def nestable_no_attrs(name__: str, *children: Union[Node, str]) -> Node:
    """
    Creates a an html {name} element with children and no attributes.
    Parameters:
        **children (Any): element from zenaura.ui.tags or plain text,
        **attributes (Any): html element attrbiutes,
        special attributes keys:
        {attribute_processor.attrKeyWords}
        special attribute values:
        {attribute_processor.attrValueWords}
    Returns:
        <{name}>[children]</{name}>

    example:
        {name}(name__="val" hidden=True, div())
    """
    return tag(name__, None, *children)

tag_config = {
    # root
    "html": "nestable",
    "main": "nestable",
    "body": "nestable",
    
    # Document meta Data
    "base": "self_closing",
    "head": "nestable_no_attrs",
    "link": "self_closing",
    "meta": "self_closing",
    "style": "textable",
    "title": "textable",

    # Section root elements
    "address": "textable",
    "article": "nestable",
    "aside": "nestable",
    "footer": "nestable",
    "header": "nestable",
    "h1": "textable",
    "h2": "textable",
    "h3": "textable",
    "h4": "textable",
    "h5": "textable",
    "h6": "textable",
    "hgroup": "nestable",
    "nav": "nestable",
    "section": "nestable",
    "search": "nestable",

    # Text content elements
    "blockquote": "textable",
    "dd": "textable",
    "div": "nestable",
    "dl": "nestable",
    "dt": "textable",
    "figcaption": "textable",
    "figure": "nestable",
    "hr": "self_closing",
    "li": "textable",
    "menu": "nestable",
    "ol": "nestable",
    "p": "textable",
    "pre": "nestable",
    "ul": "nestable",

    # Inline text semantic elements
    "a": "nestable",
    "abbr": "textable",
    "b": "nestable",
    "bdi": "nestable",
    "bdo": "nestable",
    "br": "self_closing",
    "cite": "textable",
    "code": "nestable",
    "data": "textable",
    "dfn": "textable",
    "em": "textable",
    "i": "nestable",
    "kbd": "textable",
    "mark": "textable",
    "q": "textable",
    "rp": "nestable",
    "rt": "nestable",
    "ruby": "nestable",
    "s": "textable",
    "samp": "textable",
    "small": "textable",
    "span": "nestable",
    "strong": "textable",
    "sub": "textable",
    "sup": "textable",
    "time": "textable",
    "u": "nestable",
    "var": "textable",

    # Forms
    "form": "nestable",
    "input_": "self_closing",
    "label": "textable",
    "select": "nestable",
    "option": "textable",
    "textarea": "textable",
    "fieldset": "nestable",
    "datalist": "nestable",
    "meter": "nestable",
    "optgroup": "nestable",
    "output": "textable",
    "progress": "nestable",

    # Scripting elements
    "script": "nestable",

    # Media elements
    "img": "self_closing",
    "audio": "nestable",
    "source": "self_closing",
    "track": "self_closing",
    "video": "nestable",

    # Table elements
    "caption": "nestable",
    "col": "self_closing",
    "colgroup": "nestable",
    "table": "nestable",
    "tbody": "nestable",
    "tfoot": "nestable",
    "th": "textable",
    "tr": "nestable",
    "td": "textable",
    "thead": "nestable",

    # Embedded content
    "embed": "self_closing",
    "fencedframe": "nestable",
    "iframe": "nestable",
    "object_": "nestable",
    "picture": "nestable",
    "portal": "nestable",

    # SVG and MathML
    "svg": "nestable",
    "math": "nestable",
    "circle": "nestable",
    "ellipse": "nestable",
    "line": "nestable",
    "polyline": "nestable",
    "polygon": "nestable",
    "path": "nestable",
    "rect": "nestable",
    "rect": "nestable",
    # Noscript
    "noscript": "nestable",

    # Miscellaneous content
    "del_": "self_closing",
    "ins": "self_closing",
}

tags_factory = {
    "nestable": lambda name__ : f"""
{name__ }= partial(nestable,"{name__}")
{name__}.__doc__ = nestable.__doc__
""",
    "textable": lambda name__ : f"""
{name__} = partial(textable, "{name__}")
""",
    "self_closing": lambda name__ : f"""
{name__ }= partial(self_closing, "{name__}")
""",
 "nestable_no_attrs": lambda name__ : f"""
{name__ }= partial(nestable_no_attrs,"{name__}")
"""
}

for k,v in tag_config.items():
    exec(tags_factory[v](k), globals())
