from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Create observers for subjects to notify.
    """

    @abstractmethod
    def update(self, value):
        """
        Update method to be implemented by concrete observers.

        Parameters:
        value (dict): The updated value from the subject.

        Returns:
        None
        """
        pass