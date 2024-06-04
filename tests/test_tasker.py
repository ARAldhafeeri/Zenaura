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
        from zenaura.client.hydrator.tasker import HydratorTasker
        self.tasker = HydratorTasker()

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
        self.assertEqual(queue.qsize(),0)
        self.tasker.hyd_tsk_dequeue_task(component_id)
        # task queue cleaned after emptied
        self.assertTrue(self.tasker.queue_lookup[component_id].empty())
    
    def test_dequeue_task_empty_queue(self):
        component_id = "comp-id5"
        queue = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)

        result = self.tasker.hyd_tsk_dequeue_task(component_id)

        self.assertTrue(callable(result))
        self.assertTrue(self.tasker.queue_lookup[component_id].empty())
    
    def test_dequeue_task_non_existent_queue(self):
        component_id = "comp-id6"
        queue = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)

        result = self.tasker.hyd_tsk_dequeue_task(component_id)
        self.assertTrue(callable(result))
        self.assertTrue(self.tasker.queue_lookup[component_id].empty())

    def test_dequeue_task_multiple_tasks(self):
        component_id = "comp-id7"
        queue = self.tasker.hyd_tsk_get_or_create_task_queue(component_id)
        task1 = MagicMock()
        task2 = MagicMock()
        task3 = MagicMock()
        queue.put_nowait(task1)
        queue.put_nowait(task2)
        queue.put_nowait(task3)
        dequeued_task1 = self.tasker.hyd_tsk_dequeue_task(component_id)
        dequeued_task2 = self.tasker.hyd_tsk_dequeue_task(component_id)
        dequeued_task3 = self.tasker.hyd_tsk_dequeue_task(component_id)
        self.tasker.hyd_tsk_dequeue_task(component_id)
        self.assertEqual(dequeued_task1, task1)
        self.assertEqual(dequeued_task2, task2)
        self.assertEqual(dequeued_task3, task3)
        self.assertEqual(queue.qsize(), 0)
        self.assertTrue(self.tasker.queue_lookup[component_id].empty())


