from .common import *

def Message(content, close, show, class_names="fixed top-0 px-4 py-4 right-0 mt-2  shadow z-40 rounded bg-light-white dark:bg-dark-black"):
	"""
	Creates a closeable message notification
	
	args:
			text: content of message
			close: close handler
			class_names : Default class names
			show : boolean show or hide message
	"""
	main = "relative" if show else "hidden"
	return Div(main, [
		Div(class_names, [
			Div("relative", [
				content,
				Button("fixed top-0 right-0 dark:text-dark-page1 ", "X", attrs={
				"py-click": close
				})
			])
		])
	])
