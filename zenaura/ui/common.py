from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Attribute
from .styles import with_theme_colors, btn_one_class, with_theme_colors_text_no_hover
from typing import List
# Base 
def Image(src, alt, width, height, classname=""):
		return Builder("img").with_attributes(
				src=src,
				alt=alt,
				width=width,
				height=height,
		).with_attribute("class", classname).build()

def Header2(text, class_name=""):
		return Builder('h2').with_attribute("class", class_name).with_text(text).build()

def Header1(text, class_names):
		return Builder('h1').with_text(text).with_attribute("class", class_names).build()

def Section(children, class_name="intro"):
		section = Builder('section').with_attribute('class', class_name).build()
		section.children = children
		return section

def HR():
	return Builder("hr").with_attribute('class', "w-full border-b-1 border-light-green dark:border-gray-700 ").build()

def OL(children, attrs):
	"""
		unordered list
		args:
			children - li elements 
			attrs - dictionary of attributes
		retrun:
			<ol>
				<li></li>
				<li></li>
			</ol>
	"""
	return Builder("ol").with_attributes(**attrs).with_children(*children).build()

def LI(child, attrs):
	"""
	list element li tag
	args:
			children - any html element
			attrs - dictionary of attributes
		retrun:
			<li attributes>child</li>
	"""
	return Builder("li").with_attributes(**attrs).with_child(child).build()


def A(child, attrs):
	"""
	list element A tag
	args:
			child - any html element
			attrs - dictionary of attributes
		retrun:
			<a attributes>child</a>
	"""

	return Builder("a").with_attributes(**attrs).with_child(child).build()

def Dialog(children, attrs):
	return Builder("dialog").with_children(*children).with_attributes(**attrs).build()

# features menu

def Paragraph(text, class_name=None):
		builder = Builder('p').with_text(text)
		if class_name:
				builder = builder.with_attribute('class', class_name)
		return builder.build()

def Div(class_name, children):
		div = Builder('div').with_attribute('class', class_name).build()
		div.children = children
		return div

def Button(class_name, text, onclick_handler=None, name=None, attrs={}):
		builder = Builder('button').with_attribute('class', class_name).with_text(text)
		if onclick_handler:
				builder = builder.with_attribute('py-click', onclick_handler)
		if name:
				builder = builder.with_attribute("name", name)
		return builder.with_attributes(**attrs).build()

def ButtonWithAttrsChildren(class_name, attrs, children, onclick_handler=None, name=None):
		return Builder("button") \
			.with_attribute("class", class_name) \
			.with_attributes(**attrs).with_children(*children) \
			.with_attribute("py-click", onclick_handler) \
			.build()

def Loader():
	return Div("loader self-center bg-light-white dark:bg-dark-gray1", [
		Div("", [
			Div("", [
			])
		])
	])


# nav 

def NavItemText(href, text, class_names, click=None):
	tag = Builder('a') \
		.with_attribute("class", class_names) \
		.with_attribute("href", href) \
		.with_text(text)
	if click:
		tag.with_attribute("py-click", click)
	return tag.build()

def NavItemTextNameFactory(href, text, class_names, click=None):
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
	return Builder('a') \
    .with_attribute("class", class_names) \
    .with_attribute("href", href) \
		.with_attribute("target", target) \
    .with_text(text).build()
       
def NavItemIcon(href, img, class_names=""):
  return  Builder('a').with_attribute('href', href).with_attribute("class", class_names).with_child(img).build()

def SvgPath(linecap, linejoin, d):
        return  Builder('path') \
          .with_attribute('stroke-linecap', linecap) \
          .with_attribute('stroke-linejoin', linejoin) \
          .with_attribute('d', d) \
          .build()

def Svg(class_name, fill, viewBox, stroke, path, stroke_width=None):
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
        span =  Builder('span').with_attribute('class', class_name)
        if text:
                span.with_text(text)
        return span.build()

  