from .lifecycles.mount import MountLifeCycles
from .error import GracefulDegenerationLifeCycleWrapper
from zenaura.client.page import Page
from zenaura.client.hydrator import HydratorRealDomAdapter
import traceback

rdom_hyd = HydratorRealDomAdapter()

class Mount(
    GracefulDegenerationLifeCycleWrapper,
    MountLifeCycles,
    ):
    """
    Mounts a single `Page` instance to the DOM.

    This class handles the mounting of a single `Page` instance to the DOM. It ensures that only one page is mounted at a time and provides lifecycle methods for handling the mounting process.

    **Lifecycle:**

    1. **Server-side:**
        - The server hydrates all app pages and overwrites the `index.html` file.
        - The `App` class toggles the visibility of the mounted page.
    2. **Client-side:**
        - The `Mount` class triggers the `attached` lifecycle method for the page components.

    **Error Handling:**

    - If an error occurs during mounting, the `on_error` method is called with the error message.
    - This method allows components to handle errors gracefully by returning a new component to display in place of the original component.
    - If the component does not have a `on_error` method, a default error message component is displayed.

    **Parameters:**

    - `page`: An instance of the `Page` class.

    **Returns:**

    None
    """

    async def mount(self, page: Page) -> None:
        """
        Mounts the given `Page` instance to the DOM.

        This method attempts to mount the provided `Page` instance to the DOM. It iterates through the page's children, updating their state in the virtual DOM and triggering the `attached` lifecycle method for each component.

        **Error Handling:**

        - If an error occurs during mounting, the `on_error` method is called with the error message.
        - This method allows components to handle errors gracefully by returning a new component to display in place of the original component.
        - If the component does not have a `on_error` method, a default error message component is displayed.

        **Parameters:**

        - `page`: An instance of the `Page` class.

        **Returns:**

        None
        """

        try:
            for comp in page.children:
                # Update state in vdom
                self.hyd_vdom_update(comp)
                # Trigger attached for page components
                await self.attached(comp)

        except Exception as e:
            self.on_error(page.children[0], traceback.format_exc())
