import unittest
import asyncio
import sys
from unittest.mock import patch, MagicMock

from unittest.mock import patch, MagicMock

sys.modules["pyscript"] = MagicMock()

class TestDom(unittest.TestCase):

    @patch('pyscript.document')
    @patch('pyscript.window')
    def setUp(self, document, window):  # Run before each test
        from zenaura.client.hydrator.tasker import Tasker
        self.tasker = Tasker()

    def test_get_or_create_task_queue_new_queue(self):
        component_id = "comp-id1"
        queue = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)
        self.assertIsInstance(queue, asyncio.Queue)
        self.assertEqual(self.tasker.queue_lookup[component_id], queue)

    def test_get_or_create_task_queue_existing_queue(self):
        component_id = "comp-id1"
        queue1 = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)
        queue2 = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)
        self.assertEqual(queue1, queue2)

    def test_enqueue_task_success(self):
        component_id = "comp-id3"
        queue = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)
        task = MagicMock()
        result = self.tasker.hyd_tsk_enqueue_task(component_id, task)
        self.assertTrue(result)
        self.assertEqual(queue.qsize(), 1)
        dequeued_task = self.tasker.hyd_tsk_dequeue_task(component_id)
        self.assertEqual(dequeued_task, task)
        self.assertEqual(queue.qsize(), 0)
        # task queue cleaned after emptied
        self.assertEqual(self.tasker.queue_lookup[component_id], "")
