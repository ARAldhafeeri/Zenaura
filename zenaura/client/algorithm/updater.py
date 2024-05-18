from zenaura.client.hydrator import HydratorRealDomAdapter
import operations

class Updater(HydratorRealDomAdapter):

    async def update(self, patches):
        """
            1. receive patches with rich context information from searcher
            2. create new task as coroutines based on operation name and context
            2. enqueue tasks for the component in hyderator tasker 
        """
        