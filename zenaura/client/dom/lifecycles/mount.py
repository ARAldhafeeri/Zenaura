from zenaura.client.hydrator import HydratorVirtualDomAdapter
class MountLifeCycles(
    HydratorVirtualDomAdapter
):
    """
    This class provides lifecycle methods for components that are mounted to the DOM.

    It inherits from the `HydratorVirtualDomAdapter` class, which provides methods for interacting with the virtual DOM.
    """

    async def attached(self, comp) -> None:
        """
        This method is called after the component is mounted to the DOM.

        It allows the component to perform any necessary actions after it has been added to the DOM, such as:

        - Initializing state
        - Setting up event listeners
        - Making API calls
        - Performing animations

        Args:
            comp: An instance of the Component class.

        Returns:
            None
        """

        if hasattr(comp, 'attached'):
            await comp.attached()
