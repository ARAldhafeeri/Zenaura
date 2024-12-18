import unittest
from unittest.mock import patch, AsyncMock, MagicMock, AsyncMock
from zenaura.client.dispatcher import AsyncDispatcher
from tests.mocks.browser_mocks import MockDocument, MockWindow, create_proxy, MockElement

class TestAsyncDispatcher(unittest.TestCase):
    def setUp(self):
        self.dispatcher = AsyncDispatcher()

    
    @patch("zenaura.web.utils.document")
    def test_dispatch_runs_coroutine(self, document):
        """Test that dispatch runs a coroutine."""
        async def sample_coro(arg1, arg2):
            return arg1 + arg2
        
        document.ready_state = "interactive"

        coro_mock = AsyncMock(side_effect=sample_coro)

        self.dispatcher.dispatch(coro_mock, 2, 3)


    @patch("zenaura.web.utils.document.getElementById")
    def test_bind_event_on_element(self, getElementById):
        """Test bind method binds events to elements."""

        async def test_callback(event):
            pass

        self.dispatcher.bind("test_id", "click", test_callback)

        getElementById.assert_called_with("test_id")

        
    @patch("zenaura.web.utils.document.addEventListener")
    def test_bind_to_window(self, addEventListener):
        """Test bind attaches an event to the window."""
        
        async def test_callback(event):
            pass

        self.dispatcher.bind("document", "load", test_callback)
        addEventListener.assert_called_once()


    @patch("zenaura.web.utils.window.addEventListener")
    def test_bind_to_window(self, addEventListener):
        """Test bind attaches an event to the window."""
        
        async def test_callback(event):
            pass

        self.dispatcher.bind("window", "resize", test_callback)
        addEventListener.assert_called_once()


if __name__ == '__main__':
    unittest.main()
