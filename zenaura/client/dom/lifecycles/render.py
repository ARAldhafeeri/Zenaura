class RenderLifeCycle:
    async def on_mutation(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations before updating
        if hasattr(comp, 'on_mutation'):
            await comp.on_mutation()

    async def on_settled(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'on_settled'):
            await comp.on_settled()