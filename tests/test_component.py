import unittest
from zenui.component import ZenUIComponent

class TestComponent(unittest.TestCase):
    def setUp(self) -> None:
        class Counter(ZenUIComponent):
            def __init__(self):
                super().__init__()

        class Counter2(ZenUIComponent):
            def __init__(self):
                ZenUIComponent.__init__(self)
                
        self.c = Counter()
        self.c2 = Counter2()

    
    def test_singleton_dom(self):
        self.assertEqual(id(self.c.dom), id(self.c2.dom))

    def test_singleton_global_events(self):
        self.assertEqual(id(self.c.globalEmitter), id(self.c2.globalEmitter))

    def test_local_event_emitter(self):
        self.assertNotEqual(id(self.c.localEmitter), id(self.c2.localEmitter))

    def test_render(self):
        self.assertEqual(id(self.c.render), id(self.c2.render))
