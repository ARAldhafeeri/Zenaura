import unittest
import io
from zenaura.client.page import Page 
from .mocks.counter_mocks import Counter
from zenaura.client.hydrator import HydratorCompilerAdapter
from zenaura.server.server import ZenauraServer, template
from zenaura.client.app import App 
from unittest.mock import MagicMock, patch


class TestZenauraServer(unittest.TestCase):

    def setUp(self):
        self.page = Page([Counter([])])
        self.page.id = 'test-page-id'
        self.page_content = '<div>Test Page Content</div>'
        self.compiler_adapter = HydratorCompilerAdapter()
        self.maxDiff = None
        
        global compiler_adapter
        compiler_adapter = self.compiler_adapter  # Mocking the global instance
        
        self.template_content = template

    def test_hydrate_page(self):
        result = ZenauraServer.hydrate_page(self.page)
        self.assertEqual(result, self.template_content(self.compiler_adapter.hyd_comp_compile_page(self.page),  title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js"))
    

if __name__ == '__main__':
    unittest.main()