from zenaura.client.component import Component

class App(Component):
    def __init__(self, router):
        super().__init__()
        self.router = router

