import unittest
import io
from zenaura.client.page import Page 
from .mocks.counter_mocks import Counter
from zenaura.client.hydrator import HydratorCompilerAdapter
from zenaura.server.server import ZenauraServer, template
from zenaura.client.app import App 
from unittest.mock import MagicMock, patch
from zenaura.client.layout import Layout


class TestZenauraServer(unittest.TestCase):

    def setUp(self):
        from zenaura.client.app import HistoryNode, PageHistory, NotFound, App, Route
        from .mocks.counter_mocks import Counter
        from .mocks.browser_mocks import MockDocument, MockWindow
        self.page = Page([Counter([])])
        self.page.id = 'test-page-id'
        self.page_content = '<div>Test Page Content</div>'
        self.compiler_adapter = HydratorCompilerAdapter()
        self.maxDiff = None
        self.middleware = MagicMock()
        self.page = Page([Counter([])])
        self.route = Route("test", "/test", self.page, self.middleware) 
        self.route_home = Route("test3", "/", self.page, self.middleware) 
        self.route2 = Route("test2", "/2", self.page, self.middleware) 
        self.new_route = Route
        self.router = App()
        self.router.add_route(self.route)
        self.router.add_route(self.route_home)
        self.router.add_route(self.route2)

        self.history_node = HistoryNode
        self.page_history = PageHistory
        self.not_found = NotFound()
        self.document = MockDocument()
        self.window = MockWindow()
        self.dom_patcher = patch("zenaura.client.app.document", self.document)
        self.dom_patcher.start()
        self.window_patcher = patch("zenaura.client.app.window", self.window)
        self.window_patcher.start()

        self.router_without_home = App()
        self.router_without_home.add_route(self.route)
        self.router_without_home.add_route(self.route2)
        self.page_with_attrs = Page([Counter([])], {"k" : "test"})
        self.router_page_with_attrs = App()
        self.router_page_with_attrs.add_route(
            Route("test", "/test",self.page_with_attrs, self.middleware )
        )
        
        global compiler_adapter
        compiler_adapter = self.compiler_adapter  # Mocking the global instance
        
        self.template_content = template

    def tearDown(self):
        self.dom_patcher.stop()
        self.window_patcher.stop()

    def test_hydrate_page(self):
        result = ZenauraServer.hydrate_page(self.page)
        self.assertEqual(result, self.template_content(self.compiler_adapter.hyd_comp_compile_page(self.page), title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js"))

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_home_defined(self, mock_open):
        result = ZenauraServer.hydrate_app(self.router)
        routes = self.router.routes 
        pages = []
        for _, route in routes.items():
            page, _, _, _ = route
            pages.append(page.id)
        # / path is not hidden
        self.assertIn(
            f'<div data-zenaura="{pages[0]}">',
            result, 
        )
        # rest are hidden
        self.assertIn(
            f'<div hidden data-zenaura="{pages[1]}">',
            result, 
        )
        self.assertIn(
            f'<div hidden data-zenaura="{pages[2]}">',
            result, 
        )
    
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_home_not_defined_first_in_stack_shown(self, mock_open):        
        result = ZenauraServer.hydrate_app(self.router_without_home)
        
        routes = self.router_without_home.routes 

        pages = []
        for _, route in routes.items():
            page, _, _, _ = route
            pages.append(page.id)
        # / path is not hidden
        self.assertIn(
            f'<div hidden data-zenaura="{pages[0]}">',
            result, 
        )
        # rest are hidden
        self.assertIn(
            f'<div hidden data-zenaura="{pages[1]}">',
            result, 
        )


    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_pages_with_attrs(self, mock_open):        
        result = ZenauraServer.hydrate_app(self.router_page_with_attrs)
        
        routes = self.router_page_with_attrs.routes 

        pages = []
        for _, route in routes.items():
            page, _, _, _ = route
            pages.append(page.id)
        # / path is not hidden
        self.assertIn(
            f'<div k="test" data-zenaura="{pages[0]}">',
            result, 
        )

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_layout_pages_with_attrs(self, mock_open):
        layout = Layout([Counter([])], self.router_page_with_attrs.routes,[Counter([]) ] )
        result = ZenauraServer.hydrate_app_layout(layout)
        routes = layout.routes
        pages = []
        for _, route in routes.items():
            page, _, _, _ = route
            pages.append(page.id)

        # Page with attributes is not hidden
        self.assertIn(f'<div k="test" data-zenaura="{pages[0]}">', result)
        self.assertEqual(result.count(f'data-zenaura="{Counter([]).id}"') , 3)

    
if __name__ == '__main__':
    unittest.main()
