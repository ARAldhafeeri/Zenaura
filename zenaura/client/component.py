#!/usr/bin/env python3
import uuid
from abc import abstractmethod

class Component:
    _state = {}  # Internal state of the component

    def __init_subclass__(cls):
        """
        Initialize a new subclass of Component.

        This method generates a unique componentId for each subclass using uuid.

        Args:
        cls: The subclass being initialized.

        Returns:
        None
        """

        super().__init_subclass__()

        #shorter version for accessibility purposes
        cls.componentId = uuid.uuid4().hex[:8]

    @property
    def state(self):
        """
        Get the state of the component.

        Returns:
        dict: The state of the component.
        """

        return self.get_state()

    @state.setter
    def state(self, value):
        """
        Set the state of the component.

        Args:
        value (dict): The new state of the component.

        Returns:
        None
        """

        self.set_state(value)

    def get_state(self):
        """
        Get the state of the component.

        Returns:
        dict: The state of the component.
        """

        return self._state

    def set_state(self, state):
        """
        Set the state of the component.

        Args:
        state (dict): The new state of the component.

        Returns:
        None
        """

        self._state = state  # Update the internal state

    @abstractmethod
    def node():
        """
        Abstract method to be implemented by subclasses.

        This method should be implemented by subclasses to define the behavior of the component.

        Returns:
        None
        """