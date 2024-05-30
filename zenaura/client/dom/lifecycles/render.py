class RenderLifeCycle:
    """
    This class provides lifecycle methods for components that are rendered to the DOM.

    It allows components to perform actions before and after they are updated and re-rendered in the DOM.

    Attributes:
        None
    """

    async def on_mutation(self, comp) -> None:
        """
        This method is called after the component is updated in the DOM and re-rendered.

        It allows the component to perform any necessary actions before the update is applied, such as:

        - Updating state based on new props
        - Setting up event listeners
        - Making API calls
        - Performing animations

        Args:
            comp: An instance of the Component class.

        Returns:
            None
        """

        # Perform operations before updating
        if hasattr(comp, 'on_mutation'):
            await comp.on_mutation()

    async def on_settled(self, comp) -> None:
        """
        This method is called after the component is updated in the DOM and re-rendered.

        It allows the component to perform any necessary actions after the update is applied, such as:

        - Focusing on an input element
        - Scrolling to a specific position
        - Triggering custom events

        Args:
            comp: An instance of the Component class.

        Returns:
            None
        """

        # Perform operations after updating
        if hasattr(comp, 'on_settled'):
            await comp.on_settled()
