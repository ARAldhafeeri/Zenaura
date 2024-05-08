from zenui.component import ZenUIComponent

class Counter(ZenUIComponent):
    def __init__(self):
        self.localEmitter = super().get_local_emiter()

class Counter2(ZenUIComponent):
    def __init__(self):
        self.localEmitter = super().get_local_emiter()

class componentWIthInitState(ZenUIComponent):
    def __init__(self):
        super().set_state({"test" : "test"})
        self.emitter = super().globalEmitter
        
    def init_(self):
        return self.state