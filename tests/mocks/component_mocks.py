from zenui.component import ZenUIComponent

class Counter(ZenUIComponent):
    pass

class Counter2(ZenUIComponent):
    pass

class componentWIthInitState(ZenUIComponent):
    def __init__(self):
        super().set_state({"test" : "test"})
        
    def init_(self):
        return self.state