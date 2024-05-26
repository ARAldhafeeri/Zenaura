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
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        cls.count = next(cls._component_count)
        self.id = UUIDManager.generate_uuid(cls.__name__, self.count)
        _is_reuseable[cls.__name__] = True

    cls.__init__ = new_init
    return cls

class SelectiveSingleton(type):
    _instances = defaultdict(str)

    def __call__(cls, *args, **kwargs):
        # Check if the class has the _is_reuseable attribute set to True
        if not _is_reuseable[cls.__name__]:
            return super().__call__(*args, **kwargs)

        reuseableId = f"{cls.__name__ + str(cls.count)}"   
        if cls not in cls._instances and reuseableId not in cls._instances and _is_reuseable[cls.__name__]:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        else:
            instance = super().__call__(*args, **kwargs)
            cls._instances[reuseableId] = instance
        return cls._instances[cls]
    
class Component(metaclass=SelectiveSingleton):
    _state = defaultdict(str)
    _track_instances = defaultdict(int)
    _component_count = itertools.count(0)

    def __init_subclass__(cls, **kwargs):
        cls.count = next(cls._component_count)
        cls.id = UUIDManager.generate_uuid(cls.__name__, cls.count)
        super().__init_subclass__(**kwargs)
        
    def __init__(self):
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