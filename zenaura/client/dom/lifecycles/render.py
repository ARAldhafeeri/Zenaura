class RenderLifeCycle:
    def componentWillUpdate(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'componentWillUpdate'):
            comp.componentWillUpdate()

    def componentDidUpdate(self, comp) -> None:
        """
        Method called after the component is updated in the DOM and re-rendered.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # Perform operations after updating
        if hasattr(comp, 'componentDidUpdate'):
            comp.componentDidUpdate()