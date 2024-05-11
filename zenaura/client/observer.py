from abc import ABC, abstractmethod

class Subject:
    """
    Create subjects for components to communicate on.
    """

    def __init__(self):
        """
        Initialize a new Subject.

        Parameters:
        None

        Returns:
        None
        """
        self._observers = set()
        self._state = {}

    def attach(self, observer):
        """
        Attach an observer to the subject.

        Parameters:
        observer (Observer): The observer to attach.

        Returns:
        None
        """
        self._observers.add(observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.

        Parameters:
        observer (Observer): The observer to detach.

        Returns:
        None
        """
        self._observers.discard(observer)

    def notify(self):
        """
        Notify all attached observers.

        Parameters:
        None

        Returns:
        None
        """
        for observer in self._observers:
            observer.update(self._state)

    @property
    def state(self):
        """
        Get the state of the subject.

        Parameters:
        None

        Returns:
        dict: The state of the subject.
        """
        return self._state

    @state.setter
    def state(self, new_value):
        """
        Set the state of the subject and notify observers.

        Parameters:
        new_value (dict): The new state of the subject.

        Returns:
        None
        """
        self._state = new_value
        self.notify()


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