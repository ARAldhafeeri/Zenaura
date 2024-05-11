from abc import ABC, abstractmethod

class Subject:
    """
        create subjects for components to communicate on 
    """
    def __init__(self):
        self._observers = set()
        self._state= {}

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def notify(self, value):
        for observer in self._observers:
            observer.update(value)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_value):
        self._state= new_value
        self.notify()


class Observer(ABC):
    """
        create observers for subjects to notify
    """
    @abstractmethod
    def update(self, value):
        pass