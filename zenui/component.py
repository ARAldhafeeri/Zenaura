#!/usr/bin/env python3
import uuid
from abc import abstractmethod
from zenui.zenui_dom import zenui_dom



class ZenUIComponent:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.componentId = uuid.uuid4().hex
    global_state = {}

    
    # Initialize an internal (private) dictionary to store component state
    _state = {}  
        
    @property
    def state(self):
        return self.get_state()

    @state.setter
    def value(self, value):
        self.set_state(value)
        #  re-render call Comp.node(self, self.get_state)
        zenui_dom.render(zenui_dom.curr_mounted_node)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state  # Update the internal state
    
    @abstractmethod
    def node():
        pass

