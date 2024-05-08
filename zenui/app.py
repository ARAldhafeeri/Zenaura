from zenui.component import ZenUIComponent

class ZenUIApp(ZenUIComponent):
    def __init__(self, router):
        super().__init__()
        self.router = router

