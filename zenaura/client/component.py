#!/usr/bin/env python3
#!/usr/bin/env python3
import itertools
import hashlib
from abc import abstractmethod
from collections import defaultdict

_is_reuseable = defaultdict(lambda: False)


class UUIDManager:
    @staticmethod
    def generate_uuid(cls_name, count):
        # Combine class name and count to create a unique string
        unique_string = f"{cls_name}{count}"
        # Hash the unique string to produce a 32-bit UUID
        uuid_hash = hashlib.md5(unique_string.encode()).hexdigest()[:8]
        return uuid_hash

def Reuseable(cls):
    """
    Decorator to mark a component as reusable.

    Reusable components can be instantiated multiple times and will maintain their own state.

    Args:
        cls (type): The component class to be decorated.

    Returns:
        type: The decorated component class.
    """

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        cls.count = next(cls._component_count)
        self.id = UUIDManager.generate_uuid(cls.__name__, self.count)
        _is_reuseable[cls.__name__] = True

    cls.__init__ = new_init
    return cls
    
class Component:
    """
    Base class for all Zenaura components.

    Components are the building blocks of Zenaura applications. They represent reusable units of functionality that can be composed to create complex user interfaces.

    Attributes:
        id (str): A unique identifier for the component.
        state (dict): The state of the component.
        _state (dict): The internal state of the component.
        _track_instances (dict): A dictionary tracking the number of instances created for each component class.
        _component_count (itertools.count): An iterator that generates unique counts for each component instance.

    Methods:
        __init_subclass__(cls, **kwargs):
            Initializes the subclass and sets the initial count for the component class.
        __init__(self):
            Initializes the component instance and sets the unique identifier.
        get_state(self):
            Returns the state of the component.
        set_state(self, state):
            Sets the state of the component.
        render(self):
            Abstract method that must be implemented by subclasses to define the behavior of the component.
    """

    _state = defaultdict(str)
    _track_instances = defaultdict(int)
    _component_count = itertools.count(0)

    def __init_subclass__(cls, **kwargs):
        """
        Initializes the subclass and sets the initial count for the component class.
        """
        cls.count = next(cls._component_count)
        cls.id = UUIDManager.generate_uuid(cls.__name__, cls.count)
        super().__init_subclass__(**kwargs)
        
    def __init__(self):
        """
        Initializes the component instance and sets the unique identifier.
        """
        cls = self.__class__
        Component._track_instances[cls.__name__] += 1
        if Component._track_instances[cls.__name__] > 1 and not _is_reuseable[cls.__name__]:
            raise TypeError(
"""
    Zenaura class component are limted by design. \n
    Decorate component with @Reuseable to implicitly  \n
    state the component is meant to be reused:  \n
    example :  \n
        class ThisIsLimited(Component):  \n
            pass
        c1 = ThisIsLimited() // no error  \n
        c2 = ThisIsLimited() // throws error  \n

        @Reuseable  \n
        class ThisIsReuseable(Component):  \n
        c1 = ThisIsReuseable() // no error  \n
        c2 = ThisIsReuseable() // no error  \n
"""
            )
        
        
        # print(Component._track_instances[cls.__name__], cls.__name__, is_decorated_with_reuseable(cls))
       
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
    def render():
        """
        Abstract method to be implemented by subclasses.

        This method should be implemented by subclasses to define the behavior of the component.

        Returns:
        None
        """