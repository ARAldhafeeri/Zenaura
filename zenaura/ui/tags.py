from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Node
from zenaura.client.tags.attribute import Attribute
from zenaura.client.config import self_closing_tags

from typing import Any, List, Union, Dict

def tag(
    name: str,
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
  builder = Builder(name)
  if children:
      builder.with_children(*children)
  if attributes:
      builder.with_attributes(**attributes)
  if text:
      builder.with_text(text)
  # print("data", builder.node.children, builder.node.attributes)
  return builder.build()


def self_closing(name: str, **attributes: Any) -> Node:
    return tag(name, **attributes)

def nestable(name, *children: Union[Node, str], **attributes: Any) -> Node:
    return tag(name, None, *children, **attributes)

def textable(name: str, text: str, *children: Union[Node, str], **attributes: Any) -> Node:
  return tag(name, text, *children, **attributes)

def nestable_no_attrs(name: str, *children: Union[Node, str] ) -> Node:
    return tag(name, None, *children)
 # from https://developer.mozilla.org/en-US/docs/Web/HTML/Element

# Main root elements
def html(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("html", *children, **attributes)

def main(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("main", *children, **attributes)

# Document meta data elements
def base(**attributes: Any) -> Node:
    return self_closing("base", **attributes)

def head(*children: Union[Node, str]) -> Node:
    return nestable_no_attrs("head", *children)

def link(**attributes: Any) -> Node:
    return self_closing("link", **attributes)

def meta(**attributes: Any) -> Node:
    return self_closing("meta", **attributes)

def style(*children: Union[Node, str], **attributes: Any) -> Node:
    return textable("style", *children, **attributes)

def title(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("title", text, *children, **attributes)

# Section root elements
def body(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("body", *children, **attributes)

# Content sectioning elements
def address(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("address", text, *children, **attributes)

def article(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("article", *children, **attributes)

def aside(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("aside", *children, **attributes)

def footer(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("footer", *children, **attributes)

def header(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("header", *children, **attributes)

def h1(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h1", text, *children, **attributes)

def h2(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h2", text, *children, **attributes)

def h3(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h3", text, *children, **attributes)

def h4(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h4", text, *children, **attributes)

def h5(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h5", text, *children, **attributes)

def h6(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("h6", text, *children, **attributes)

def hgroup(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("hgroup", *children, **attributes)

def nav(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("nav", *children, **attributes)

def section(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("section", *children, **attributes)

def search(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("search", *children, **attributes)

# Text content elements
def blockquote(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("blockquote", text, *children, **attributes)

def dd(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("dd", text, *children, **attributes)

def div(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("div", *children, **attributes)

def dl(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("dl", *children, **attributes)

def dt(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("dt", text, *children, **attributes)

def figcaption(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("figcaption", text, *children, **attributes)

def figure(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("figure", *children, **attributes)

def hr(**attributes: Any) -> Node:
    return self_closing("hr", **attributes)

def li(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("li", text, *children, **attributes)

def menu(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("menu", *children, **attributes)

def ol(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("ol", *children, **attributes)

def p(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("p", text, *children, **attributes)

def pre(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("pre", *children, **attributes)

def ul(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("ul", *children, **attributes)

# Inline text semantic elements
def a(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("a", *children, **attributes)

def abbr(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("abbr", text, *children, **attributes)

def b(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("b", *children, **attributes)

def bdi(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("bdi", *children, **attributes)

def bdo(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("bdo", *children, **attributes)

def br(**attributes: Any) -> Node:
    return self_closing("br", **attributes)

def cite(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("cite", text, *children, **attributes)

def code(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("code", *children, **attributes)

def data(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("data", text, *children, **attributes)

def dfn(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("dfn", text, *children, **attributes)

def em(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("em", text, *children, **attributes)

def i(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("i", *children, **attributes)

def kbd(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("kbd", text, *children, **attributes)

def mark(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("mark", text, *children, **attributes)

def q(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("q", text, *children, **attributes)

def rp(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("rp", *children, **attributes)

def rt(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("rt", *children, **attributes)

def ruby(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("ruby", *children, **attributes)

def s(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("s", text, *children, **attributes)

def samp(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("samp", text, *children, **attributes)

def small(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("small", text, *children, **attributes)

def span(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("span", *children, **attributes)

def strong(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("strong", text, *children, **attributes)

def sub(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("sub", text, *children, **attributes)

def sup(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("sup", text, *children, **attributes)

def time(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("time", text, *children, **attributes)

def u(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("u", *children, **attributes)

def var(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("var", text, *children, **attributes)

# Forms
def form(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("form", *children, **attributes)

def input(**attributes: Any) -> Node:
    return self_closing("input", **attributes)

def label(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("label", text, *children, **attributes)

def select(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("select", *children, **attributes)

def option(text, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("option",text, *children, **attributes)

def textarea(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("textarea", text, *children, **attributes)

# TODO forms : fieldset, datlalist, meter, optgroup, output, progress

# Scripting elements
def script(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("script", *children, **attributes)

# Media elements
def img(**attributes: Any) -> Node:
    return self_closing("img", **attributes)
    
def audio(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("audio", *children, **attributes)

def video(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("video", *children, **attributes)

def source(**attributes: Any) -> Node:
    return self_closing("source", **attributes)

# Table elements
def caption(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("caption", text, *children, **attributes)

def col(**attributes: Any) -> Node:
    return self_closing("col", **attributes)

def colgroup(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("colgroup", *children, **attributes)

def table(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("table", *children, **attributes)

def tbody(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("tbody", *children, **attributes)

def td(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("td", text, *children, **attributes)

def tfoot(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("tfoot", *children, **attributes)

def th(text: str, *children: Union[Node, str], **attributes: Any) -> Node:
    return textable("th", text, *children, **attributes)

def thead(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("thead", *children, **attributes)

def tr(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("tr", *children, **attributes)

# List elements
def ol(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("ol", *children, **attributes)

def ul(*children: Union[Node, str], **attributes: Any) -> Node:
    return nestable("ul", *children, **attributes)


# TODO embedded content embed, fencedframe, iframe, object, picture, portal

# TODO svgt and math ml svg, math 

# TODO  canvas, noscript, 

# del, ins



