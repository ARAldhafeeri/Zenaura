from .common import *

def Menu(main_btn : Button, children: List[ButtonWithAttrsChildren], show : bool) -> "Menu":
	"""
		Display a menu to the user - triggered by py-click

		args : 
			main_btn -> button used to toggle dropdown menu on click.
			children -> menu children 
			show -> used to toggle menu visibility
		return : 
			Togglable menu with options
	"""

	menu = Div(
		"absolute right-0 z-20 w-56 py-2 mt-2 overflow-hidden bg-white rounded-md shadow-xl dark:bg-dark-gray1" + (" hidden" if not show else ""),
		children
	)

	return Div("flex justify-center", [
		Div("relative inline-block mb-20", [
			main_btn, 
			menu

		])
	])
