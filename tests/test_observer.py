import unittest
from unittest.mock import MagicMock 
from zenaura.client.observer import Observer, Subject

observer1 = MagicMock(spec=Observer)

observer2 = MagicMock(spec=Observer)

observer1.update = MagicMock(return_value=3)

observer2.update = MagicMock(return_value=3)

class TestSubject(unittest.TestCase):
    def test_state_set_to_none(self):
        subject = Subject()
        subject.state = None

    def test_state_set_to_empty_dict(self):
        subject = Subject()
        subject.state = {}

    def test_notify_observers(self):
        subject = Subject()

        subject.attach(observer1)
        subject.attach(observer2)
        subject.state = None
        observer1.update.assert_called_once_with(None)
        observer2.update.assert_called_once_with(None)

    def test_state_set_to_none(self):
        subject = Subject()
        subject.state = None
        self.assertIsNone(subject.state)

    def test_state_set_to_empty_dict(self):
        subject = Subject()
        subject.state = {}
        self.assertDictEqual(subject.state, {})

    def test_detach_observer(self):
        subject = Subject()
        observer = MagicMock()
        subject.attach(observer)
        self.assertIn(observer, subject._observers)
        subject.detach(observer)
        self.assertNotIn(observer, subject._observers)


if __name__ == '__main__':
    unittest.main()