class MountLifeCycles:
    
    def unmount(self, comp) -> None:
        """
        Unmounts the component and performs cleanup operations.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        # no component mounted
        if not comp:
            return 
        # if component has componentWillUnmount methd call it before unmounting
        if hasattr(comp, 'componentWillUnmount'):
            comp.componentWillUnmount()  
        # Perform virtual dom cleanup operations here
        del self.zen_dom_table[comp.componentId]

    def componentWillMount(self, comp) -> None:
        """
        Method called before the component is mounted to the DOM.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        if hasattr(comp, 'componentWillMount'):
            comp.componentWillMount()

    def componentWillUnmount(self, comp) -> None:
        """
        Method called before the component is unmounted from the DOM.
        """
        if hasattr(comp, 'componentWillUnmount'):
            comp.componentWillUnmount()

    def componentDidMount(self, comp) -> None:
        """
        Method called after the component is mounted to the DOM.

        Parameters:
        - comp: An instance of the Component class.

        Returns:
        None
        """
        if hasattr(comp, 'componentDidMount'):
            comp.componentDidMount()