from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Attribute
from .styles import with_theme_colors, btn_one_class, with_theme_colors_text_no_hover
from typing import List

# Base 
def Image(src, alt, width, height, classname=""):
	"""
	Creates an HTML image element.
	Args:
			src (str): The source URL of the image.
			alt (str): The alternate text for the image.
			width (str): The width of the image.
			height (str): The height of the image.
			classname (str): The class name for the image.
	Returns:
			An HTML img element with the specified attributes.
	"""
	return Builder("img").with_attributes(
		src=src,
		alt=alt,
		width=width,
		height=height,
	).with_attribute("class", classname).build()

def Header2(text, class_name=""):
	"""
	Creates an HTML h2 element.
	Args:
			text (str): The text content of the header.
			class_name (str): The class name for the header.
	Returns:
			An HTML h2 element with the specified attributes and text.
	"""
	return Builder('h2').with_attribute("class", class_name).with_text(text).build()

def Header1(text, class_names):
	"""
	Creates an HTML h1 element.
	Args:
			text (str): The text content of the header.
			class_names (str): The class names for the header.
	Returns:
			An HTML h1 element with the specified attributes and text.
	"""
	return Builder('h1').with_text(text).with_attribute("class", class_names).build()

def Section(children, class_name="intro"):
	"""
	Creates an HTML section element.
	Args:
			children (list): The child elements of the section.
			class_name (str): The class name for the section.
	Returns:
			An HTML section element with the specified attributes and children.
	"""
	section = Builder('section').with_attribute('class', class_name).build()
	section.children = children
	return section

def HR():
	"""
	Creates an HTML hr element.
	Returns:
			An HTML hr element with specified attributes.
	"""
	return Builder("hr").with_attribute('class', "w-full border-b-1 border-light-green dark:border-gray-700 ").build()

def OL(children, attrs):
	"""
	Creates an HTML ordered list (ol) element.
	Args:
			children (list): The child li elements.
			attrs (dict): The attributes for the ol element.
	Returns:
			An HTML ol element with the specified attributes and children.
	"""
	return Builder("ol").with_attributes(**attrs).with_children(*children).build()

def LI(child, attrs):
	"""
	Creates an HTML list item (li) element.
	Args:
			child (element): The child element of the li.
			attrs (dict): The attributes for the li element.
	Returns:
			An HTML li element with the specified attributes and child.
	"""
	return Builder("li").with_attributes(**attrs).with_child(child).build()

def A(child, attrs):
	"""
	Creates an HTML anchor (a) element.
	Args:
			child (element): The child element of the a.
			attrs (dict): The attributes for the a element.
	Returns:
			An HTML a element with the specified attributes and child.
	"""
	return Builder("a").with_attributes(**attrs).with_child(child).build()

def Dialog(children, attrs):
	"""
	Creates an HTML dialog element.
	Args:
			children (list): The child elements of the dialog.
			attrs (dict): The attributes for the dialog element.
	Returns:
			An HTML dialog element with the specified attributes and children.
	"""
	return Builder("dialog").with_children(*children).with_attributes(**attrs).build()

# features menu

def Paragraph(text, class_name=None):
	"""
	Creates an HTML paragraph (p) element.
	Args:
			text (str): The text content of the paragraph.
			class_name (str, optional): The class name for the paragraph.
	Returns:
			An HTML p element with the specified attributes and text.
	"""
	builder = Builder('p').with_text(text)
	if class_name:
			builder = builder.with_attribute('class', class_name)
	return builder.build()

def Div(class_name, children):
	"""
	Creates an HTML div element.
	Args:
			class_name (str): The class name for the div.
			children (list): The child elements of the div.
	Returns:
			An HTML div element with the specified attributes and children.
	"""
	div = Builder('div').with_attribute('class', class_name).build()
	div.children = children
	return div

def Button(class_name, text, onclick_handler=None, name=None, attrs={}):
	"""
	Creates an HTML button element.
	Args:
			class_name (str): The class name for the button.
			text (str): The text content of the button.
			onclick_handler (str, optional): The JavaScript function to call on click.
			name (str, optional): The name of the button.
			attrs (dict): Additional attributes for the button.
	Returns:
			An HTML button element with the specified attributes and text.
	"""
	builder = Builder('button').with_attribute('class', class_name).with_text(text)
	if onclick_handler:
			builder = builder.with_attribute('py-click', onclick_handler)
	if name:
			builder = builder.with_attribute("name", name)
	return builder.with_attributes(**attrs).build()

def ButtonWithAttrsChildren(class_name, attrs, children, onclick_handler=None, name=None):
	"""
	Creates an HTML button element with specified attributes and children.
	Args:
			class_name (str): The class name for the button.
			attrs (dict): Additional attributes for the button.
			children (list): The child elements of the button.
			onclick_handler (str, optional): The JavaScript function to call on click.
			name (str, optional): The name of the button.
	Returns:
			An HTML button element with the specified attributes and children.
	"""
	return Builder("button") \
			.with_attribute("class", class_name) \
			.with_attributes(**attrs).with_children(*children) \
			.with_attribute("py-click", onclick_handler) \
			.build()

def Loader():
	"""
	Creates a loader div element.
	Returns:
			An HTML div element representing a loader.
	"""
	return Div("loader self-center bg-light-white dark:bg-dark-gray1", [
		Div("", [
			Div("", [
			])
		])
	])

# nav 

def NavItemText(href, text, class_names, click=None):
	"""
	Creates a navigation item with text.
	Args:
			href (str): The URL the item links to.
			text (str): The text content of the item.
			class_names (str): The class names for the item.
			click (str, optional): The JavaScript function to call on click.
	Returns:
			An HTML a element with the specified attributes and text.
	"""
	tag = Builder('a') \
		.with_attribute("class", class_names) \
		.with_attribute("href", href) \
		.with_text(text)
	if click:
			tag.with_attribute("py-click", click)
	return tag.build()

def NavItemTextNameFactory(href, text, class_names, click=None):
	"""
	Creates a navigation item with text and a name attribute.
	Args:
			href (str): The URL the item links to.
			text (str): The text content of the item.
			class_names (str): The class names for the item.
			click (str, optional): The JavaScript function to call on click.
	Returns:
			An HTML a element with the specified attributes, text, and name.
	"""
	tag = Builder('a') \
		.with_attribute("class", class_names) \
		.with_attribute("href", href) \
		.with_text(text)
	if click:
		tag.with_attribute("py-click", click)
	name = text.lower()
	tag.with_attribute("name", name)
	return tag.build()

def Link(href, text, class_names, target="_blank"):
	"""
	Creates an HTML anchor (a) element.
	Args:
			href (str): The URL the link points to.
			text (str): The text content of the link.
			class_names (str): The class names for the link.
			target (str): The target attribute for the link.
	Returns:
			An HTML a element with the specified attributes and text.
	"""
	return Builder('a') \
		.with_attribute("class", class_names) \
		.with_attribute("href", href) \
		.with_attribute("target", target) \
		.with_text(text).build()
       
def NavItemIcon(href, img, class_names=""):
	"""
	Creates a navigation item with an icon.
	Args:
			href (str): The URL the item links to.
			img (element): The image element for the icon.
			class_names (str): The class names for the item.
	Returns:
			An HTML a element with the specified attributes and icon.
	"""
	return Builder('a').with_attribute('href', href).with_attribute("class", class_names).with_child(img).build()

def SvgPath(linecap, linejoin, d):
	"""
	Creates an SVG path element.
	Args:
			linecap (str): The stroke-linecap attribute.
			linejoin (str): The stroke-linejoin attribute.
			d (

str): The path data.
	Returns:
			An SVG path element with the specified attributes.
	"""
	return Builder('path') \
		.with_attribute('stroke-linecap', linecap) \
		.with_attribute('stroke-linejoin', linejoin) \
		.with_attribute('d', d) \
		.build()

def Svg(class_name, fill, viewBox, stroke, path, stroke_width=None):
	"""
	Creates an SVG element.
	Args:
			class_name (str): The class name for the SVG.
			fill (str): The fill attribute.
			viewBox (str): The viewBox attribute.
			stroke (str): The stroke attribute.
			path (element): The path element inside the SVG.
			stroke_width (str, optional): The stroke-width attribute.
	Returns:
			An SVG element with the specified attributes and path.
	"""
	svg = Builder('svg') \
		.with_attribute('class', class_name) \
		.with_attributes(
				fill=fill,
				viewBox=viewBox,
				stroke=stroke
		).with_child(
				path
		)
	if stroke_width:
			svg.with_attribute('stroke-width', stroke_width)
	return svg.build()

def Span(class_name, text=None):
	"""
	Creates an HTML span element.
	Args:
			class_name (str): The class name for the span.
			text (str, optional): The text content of the span.
	Returns:
			An HTML span element with the specified attributes and text.
	"""
	span = Builder('span').with_attribute('class', class_name)
	if text:
			span.with_text(text)
	return span.build()