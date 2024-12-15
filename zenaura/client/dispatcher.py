import asyncio 
from zenaura.web.utils import document, window, in_browser, create_proxy
class AsyncDispatcher:
    def __init__(self):
        self.loop = None

    def dispatch(self, coro_func, *args, **kwargs):
        """
        Wrap asyncio.run to schedule and run the given coroutine.
        
        :param coro_func: The coroutine function to execute.
        :param args: Positional arguments for the coroutine.
        :param kwargs: Keyword arguments for the coroutine.
        """
        # Initialize the event loop if it's not running)
        if not self.loop or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)


        # waits for document to be interactive 
        self.loop.dispatch(dispatcher.wait_for_ready_state)

        # Run the coroutine
        self.loop.run_until_complete(coro_func(*args, **kwargs))

    async def wait_for_ready_state(self, target_state="interactive", retries=5, delay=2):
        """
        Waits for the document's readyState to match the target state.
        Retries with a delay if the state is not yet reached.

        :param target_state: The desired readyState (e.g., "interactive").
        :param retries: Number of retries before giving up.
        :param delay: Delay in seconds between retries.
        :return: True if the desired state is reached, False otherwise.
        """
        while not document.readyState == "interactive":
            await asyncio.sleep(0.01)
        return True
    
    def bind(self, id, event, coroutine):
        """
        Subscribe an event to an element, window, or document and dispatch a sync or async callback.
        Ensures the provided function has the correct signature.

        :param id: ID attached to the component, or 'window'/'document' for global bindings.
        :param event: Event name (e.g., "click", "resize", "keydown").
        :param coroutine: Callback coroutine function.
        :return: None if binding succeeds; raises an exception otherwise.
        """

        if not callable(coroutine):
            raise TypeError("The callback must be callable.")

        if not asyncio.iscoroutine(coroutine) and not asyncio.iscoroutinefunction(coroutine):
            raise TypeError(f"'{coroutine}' is not a valid asyncio coroutine. The callback must be 'async def'.")

        target = None

        # Determine the target based on id
        if id == "window":
            target = window
        elif id == "document":
            target = document
        else:
            target = document.getElementById(id)

        # if user not in development server and target not found
        # throw an error 
        if not target :
            if not in_browser:
              raise ValueError(f"Element with id '{id}' not found. Cannot bind '{coroutine.__name__}' to '{event}'.")

        # Bind the event listener
        try:
            target.addEventListener(event, create_proxy(lambda e: self.dispatch(coroutine, e)))
        except Exception as e:
            raise RuntimeError(f"Failed to bind '{coroutine.__name__}' to '{event}' on target '{id}': {e}")


dispatcher = AsyncDispatcher()
