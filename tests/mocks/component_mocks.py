from zenaura.client.component import Component, Reuseable

class Counter(Component):
    pass

class Counter2(Component):
    pass

class componentWIthInitState(Component):
    def __init__(self):
        super().set_state({"test" : "test"})
        
    def init_(self):
        return self.state
    

