import sys
import unittest
from unittest.mock import MagicMock, patch
from zenaura.client.page import Page
from zenaura.client.layout import Layout


sys.modules["pyscript"] = MagicMock()

class TestApp(unittest.TestCase):

    def setUp(self):  # Run before each test
        from zenaura.client.app import HistoryNode, PageHistory, NotFound, App, Route
        from .mocks.counter_mocks import Counter
        from .mocks.browser_mocks import MockDocument, MockWindow
        self.middleware = MagicMock()
        self.page = Page([Counter([])])
        self.route = Route("test", "/test",self.page, self.middleware  ) 
        self.new_route = Route
        self.router = App()
        self.router.add_route(self.route)

        self.history_node = HistoryNode
        self.page_history = PageHistory
        self.not_found = NotFound()
        self.document = MockDocument()
        self.window = MockWindow()
        self.dom_patcher = patch("zenaura.client.app.document", self.document)
        self.dom_patcher.start()
        self.window_patcher = patch("zenaura.client.app.window", self.window)
        self.window_patcher.start()
        self.page_with_empty_attrs = Page([Counter([])], {})
        self.page_with_attrs = Page([Counter([])], {"k" : "test"})

    def test_history_node_init(self):
        node = self.history_node()
        self.assertIsNone(node.page)
        self.assertIsNone(node.prev)
        self.assertIsNone(node.next)

    def test_page_history_visit(self):
        home_page = MagicMock()
        page_history = self.page_history()
        new_page = MagicMock()
        page_history.visit(new_page)
        self.assertEqual(page_history.current.page, new_page)

    def test_page_history_back(self):
        home_page = MagicMock()
        page_history = self.page_history()
        new_page = MagicMock()
        page_history.visit(home_page)
        page_history.visit(new_page)
        self.assertEqual(page_history.back(), home_page)

    def test_page_history_forward(self):
        home_page = MagicMock()
        page_history = self.page_history()
        new_page = MagicMock()
        page_history.visit(new_page)
        self.assertTrue(page_history.forward())

    def test_not_found_render(self):
        node = self.not_found.render()
        # Add assertions to check the structure of the generated node

    def test_route_init(self):
        route = self.route
        self.assertEqual(route.title, "test")
        self.assertEqual(route.path, "/test")
        # Add more assertions to check other attributes of the route

    def test_router_init(self):
        router = self.router
        self.assertEqual(router.paths, ["/test"])


    def test_page_with_attrs(self):
        # test passing attributes to page
        self.assertEqual(self.page_with_empty_attrs.attributes, {})
        self.assertTrue(self.page_with_attrs.attributes["k"])


class TestAsync(unittest.IsolatedAsyncioTestCase):
    def setUp(self):  # Run before each test
        from zenaura.client.app import HistoryNode, PageHistory, NotFound, App, Route
        from .mocks.counter_mocks import Counter
        from .mocks.browser_mocks import MockDocument, MockWindow
        self.middleware = MagicMock()
        self.page = Page([Counter([])])
        self.route = Route("test", "/test",self.page, self.middleware  ) 
        self.new_route = Route
        self.router = App()
        self.router.add_route(self.route)
        self.page1 = Page([Counter([])])
        self.page2 = Page([Counter([])])
        self.home_page = Page([Counter([])])
        self.history_node = HistoryNode
        self.page_history = PageHistory
        self.not_found = NotFound()
        self.document = MockDocument()
        self.window = MockWindow()
        self.dom_patcher = patch("zenaura.client.app.document", self.document)
        self.dom_patcher.start()
        self.window_patcher = patch("zenaura.client.app.window", self.window)
        self.window_patcher.start()
        self.page_with_empty_attrs = Page([Counter([])], {})
        self.page_with_attrs = Page([Counter([])], {"k" : "test"})
    
        self.router.history.current = self.history_node(self.page)
        self.document.setElementById(self.page.id, self.page)
        self.document.setElementById(self.page1.id, self.page1)
        self.document.setElementById(self.page2.id, self.page2)
        self.document.setElementById(self.home_page.id, self.home_page)

    # async def test_router_navigate_to_unknown_path(self):

    #     # Navigating to an unknown path should trigger the not-found route
    #     unknown_path = "/unknown"
    #     await self.router.navigate(unknown_path)
    #     self.assertEqual(self.document.title, "Page Not Found")
    #     # Add more assertions to check if the NotFound component is mounted and middleware is called

    # async def test_router_navigate_to_known_path(self):
    #     # Navigating to a known path should mount the associated page and update the document title
    #     known_path = "/test"
    #     await self.router.navigate(known_path)
    #     self.assertEqual(self.document.title, "test")
    #     # Add more assertions to check if the page is mounted and middleware is called

    # async def test_router_navigate_back(self):
    #     self.router.history.current = self.history_node(self.page)

    #     # Navigating back should return to the previous page in the history
    #     home_page = MagicMock()
    #     page1 = MagicMock()
    #     page2 = MagicMock()
    #     self.document.setElementById("page1", page1)
    #     self.document.setElementById("page2", page2)
    #     self.document.setElementById("homepage", home_page)
    #     page_history = self.page_history()
    #     page_history.visit(home_page)
    #     page_history.visit(page1)
    #     page_history.visit(page2)
    #     self.router.handle_location()  # Simulate navigating to page2
    #     await self.router.back()
    #     # Add assertions to check if page1 is mounted and document title is updated
        
    # async def test_router_navigate_forward(self):
    #     # Navigating forward should move to the next page in the history
    #     self.router.history.current = self.history_node(self.page)

    #     page_history = self.page_history()
    #     page_history.visit(self.home_page)
    #     page_history.visit(self.page1)
    #     page_history.visit(self.page2)
    #     self.router.handle_location()  # Simulate navigating to page2
    #     print("ids", self.document.elementsById)
    #     await self.router.back()
    #     # await self.router.forward()


    # async def test_router_wildcard_route_matching(self):
    #     route = self.new_route("wildcard", "/users/*", self.page , None)
    #     self.router.add_route(route)
    #     self.router.history.current = self.history_node(self.page)
    #     await self.router.navigate("/users/123/123?k=1&k2=3")
    #     self.window.location.pathname = "/users/123/123?k=1&k2=3"
    #     current_route, info = self.router.get_current_route()
    #     self.assertEqual(info["wildcard"]["params"], ["123", "123"])
    #     self.assertEqual(info["wildcard"]["query"]["k"], "1" )
    #     self.assertEqual(info["wildcard"]["query"]["k2"], "3" )


    # async def test_router_nested_routes(self):
    #     # Test navigation with nested routes
    #     parent_route = self.new_route("parent", "/parent", self.page, None)
    #     child_route = self.new_route("child", "/parent/child", self.page, None)

    #     self.router.add_route(parent_route)
    #     self.router.add_route(child_route)
    #     await self.router.navigate("/parent/child")
    #     self.window.location.pathname = "/parent/child"
    #     current_route, info = self.router.get_current_route()
    #     self.assertEqual(current_route[0].id, child_route.page.id)

    # async def test_router_case_sensitive_paths(self):
    #     # Test case sensitivity of route paths
    #     case_sensitive_route = self.new_route("case_sensitive", "/CaseSensitive", self.page, None)
    #     self.router.add_route(case_sensitive_route)
    #     await self.router.navigate("/casesensitive")  # Attempting to navigate with different case
    #     self.assertEqual(self.document.title, "Page Not Found")

    # async def test_router_middleware_execution_order(self):
    #     # Test the execution order of middleware
    #     middleware_order = []

    #     def middleware1():
    #         middleware_order.append(1)

    #     def middleware2():
    #         middleware_order.append(2)

    #     def middleware():
    #         middleware1()
    #         middleware2()

    #     route_with_middleware = self.new_route("middleware_order", "/middleware", self.page, middleware)
    #     self.router.add_route(route_with_middleware)
    #     await self.router.navigate("/middleware")
    #     self.assertEqual(middleware_order, [1, 2])

    async def test_layout_attached(self):
        from zenaura.client.component import Component, Reuseable
        magic_method = MagicMock() 

        class TestComponentMagicMethodAttached(Component):
            def __init__(self, mock_method):
                self.mock_method = mock_method

            async def attached(self):
                self.mock_method()
        attached_comp = TestComponentMagicMethodAttached(magic_method)
        app_layout = Layout(
            [attached_comp],
            self.router.routes, 
            [attached_comp]
        )
        self.router.layout = app_layout
        await self.router.navigate("/test")
        self.assertEqual(attached_comp.mock_method.call_count, 2)