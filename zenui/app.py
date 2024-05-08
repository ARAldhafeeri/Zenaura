from zenui.component import ZenUIComponent
from .router import Router

class ZenUIApp(ZenUIComponent):
    def __init__(self, router: Router):
        super().__init__()
        self.router = router

