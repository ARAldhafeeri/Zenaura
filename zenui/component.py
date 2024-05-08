#!/usr/bin/env python3
from zenui.zenui_dom import zenui_dom
import random
import time

def generate_simple_uuid():
    random_part = hex(random.getrandbits(128))[2:]  # 128-bit random number
    timestamp_part = hex(int(time.time()))[2:]
    return f'{timestamp_part}-{random_part}' 


class ZenUIComponent:
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.componentId = generate_simple_uuid()
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
    
    def element():
        pass

