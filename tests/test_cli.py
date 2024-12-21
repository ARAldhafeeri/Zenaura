import unittest
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from zenaura.cli.cli import init_project, build_project, run_project 

class TestZenauraCLI(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    @patch("zenaura.zenaura_logger.info")
    def test_init_project(self, mock_logger):
        init_project()

        public_dir = os.path.join(self.test_dir, "public")
        self.assertTrue(os.path.exists(public_dir))

        expected_files = ["__init__.py", "main.py", "main.css", "index.html", "config.json"]
        for file in expected_files:
            self.assertTrue(os.path.isfile(os.path.join(public_dir, file)))

        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "build.py")))
        self.assertTrue(os.path.isfile(os.path.join(self.test_dir, "index.py")))

        mock_logger.assert_any_call("Creating new zenaura project")

    @patch("os.system")
    def test_build_project(self, mock_system):
        build_project()

        mock_system.assert_called_once_with("python build.py")

    @patch("os.system")
    def test_run_project(self, mock_system):
        run_project()

        mock_system.assert_called_once_with("python index.py")

if __name__ == "__main__":
    unittest.main()
