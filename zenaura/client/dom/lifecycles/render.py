class RenderLifeCycle:
    def on_mutation(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'on_mutation'):
            comp.on_mutation()

    def on_settled(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'on_settled'):
            comp.on_settled()