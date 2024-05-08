#!/usr/bin/env python3
import uuid
from EventEmitterPy.emitter import EventEmitter
from abc import abstractmethod
from zenui.zenui_dom import zenui_dom


# global event emitter accessible by all component classes
globalEmitter = EventEmitter() 

class ZenUIComponent:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.componentId = uuid.uuid4().hex
    # Make the global EventEmitter accessible within the component class 
    globalEmitter = globalEmitter  
    global_state = {}

    
    # Initialize an internal (private) dictionary to store component state
    _state = {}  
        
    @property
    def state(self): 
        return self.get_state()

    @state.setter
    def value(self, value):
        self.set_state(value)
        #  re-render call Comp.element(self, self.get_state)
        zenui_dom.render(zenui_dom.curr_mounted_element)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state  # Update the internal state

    def get_local_emiter(self):
        # create local event emitter
        return EventEmitter()
    
    @abstractmethod
    def element():
        pass

