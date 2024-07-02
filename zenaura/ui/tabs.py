from .common import *


def TabButton(tab_number, label, active_tab_variable, on_click, class_name, active_class=" me-2 inline-block p-5 border-b-2 border-light-green border-spacing-2 dark:border-dark-page1"):
	class_expression = active_class if tab_number == active_tab_variable else ""
	return ButtonWithAttrsChildren(
			class_name=class_name  + class_expression,
			attrs={
					"py-click": on_click,
					"name": tab_number
			},
			children=[label]
	)

def TabContent(tab_number, active_tab_variable, content):
	is_visible = "block" if tab_number == active_tab_variable else "hidden"
	return Div(
			f"{is_visible} transition-all duration-300 p-4",
			[
				content    
			]
	)

def Tabs(buttons, content, g_class_names ="bg-gray-100 font-sans", buttons_wrapper_class_names="flex  border-b-2 border-light-green dark:border-dark-black"):
	"""
			Create tabs with content for each tab. 
			args:
					buttons : list of TabButton which is a button upon click becomes active and display content
					content : list of TabContent which is the content under each tab.
					g_class_names: global wrapper div class names
					button_wrapper_class_names: button wrapper div class names.
	"""
	return Div(
	g_class_names,
	[
	Div(
		"p-8",
		[
		Div(
			"",
			[
				Div(
					buttons_wrapper_class_names,
					buttons
				),
				Div(
					"mt-3", 
					content
				)
			]
		)
		]
	)
	]
)