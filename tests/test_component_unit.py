import unittest
from .mocks.component_mocks import Counter, Counter2, componentWIthInitState
from zenaura.client.persistance import registry
import hashlib
c = Counter()
c2 = Counter2()
initState = componentWIthInitState()


class TestComponent(unittest.TestCase):
    def setUp(self) -> None:
        self.c = c
        self.c2 = c2
        self.initState = initState


    def test_state(self):
        state = {"test" : "test"}
        self.c.set_state(state) 
        self.assertEqual(state, self.c.get_state())

    def test_init_state(self):
        state = {"test" : "test"}
        self.assertEqual(state, self.initState.get_state())
        self.assertEqual(self.initState.init_(), self.initState.get_state())
        self.assertEqual(self.initState.init_(), self.initState.state)

    def test_unique_local_states(self):
        state1 = {"test" : "test1"}
        state2 = {"test" : "test2"}
        self.c.set_state(state1)
        self.c2.set_state(state2) 
        self.assertNotEqual(self.c.get_state(), self.c2.get_state())

    def test_unique_comp_ids(self):
        self.assertNotEqual(self.c2.id, self.c.id)

    def test_uuid_presistance(self):
        count = self.c.count
        uuid = self.c.id 
        hash = hashlib.md5(f"{self.c.__class__.__name__}{count}".encode()).hexdigest()[:8]
        self.assertEqual(uuid, hash)        







