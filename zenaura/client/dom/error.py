from zenaura.client.component import Component, Reuseable
from zenaura.client.tags import Node
from zenaura.client.compiler import compiler
from zenaura.client.hydrator import Hydrator

@Reuseable
class DefaultDomErrorComponent(Component):
    """
    Displays a default error message component.

    Attributes:
        error_message (str): The error message to display.

    Methods:
        render(): Returns a Node representing the error message.
    """

    def __init__(self, error_message):
        super().__init__()
        self.error_message = error_message

    def render(self):
        return Node("div", children=[Node(text=str(self.error_message))])


class GracefulDegenerationLifeCycleWrapper(
    Hydrator
):
    """
    Wraps components to handle errors gracefully.

    This class provides a `on_error` method that allows components
    to handle errors gracefully. If a component throws an error, the
    `on_error` method will be called with the error message. The
    component can then return a new component to display in place of the original
    component.

    If the component does not have a `on_error` method, a default
    error message component will be displayed.
    """

    def on_error(self, comp, error) -> None:
        """
        Handles errors gracefully.

        This method is called when a component throws an error. It allows the
        component to handle the error gracefully by returning a new component to
        display in place of the original component.

        Args:
            comp (Component): The component that threw the error.
            error (Exception): The error that was thrown.
        """

        # Cleanup the Zen DOM table.
        self.zen_dom_table.clear()

        if hasattr(comp, "on_error"):
            # Call the component's `on_error` method.
            error_comp = comp.on_error(str(error))

            # Compile and render the error component.
            compiled_comp = self.hyd_comp_compile_render(error_comp)

            # Attach the compiled component to the real DOM.
            self.hyd_rdom_attach_to_root(compiled_comp)

            # Update the virtual DOM with the new render.
            self.hyd_vdom_update_with_new_render(comp, error_comp.render())

        else:
            # Create a default error message component.
            error_comp = DefaultDomErrorComponent(error_message=str(error))

            # Compile and render the default error component.
            compiled_comp = self.hyd_comp_compile_render(error_comp)

            # Attach the compiled component to the real DOM.
            self.hyd_rdom_attach_to_root(compiled_comp)

            # Update the virtual DOM with the new render.
            self.hyd_vdom_update_with_new_render(comp, error_comp.render())
