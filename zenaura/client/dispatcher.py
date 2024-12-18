import asyncio 
from zenaura.web.utils import document, window, in_browser, create_proxy
import nest_asyncio
nest_asyncio.apply()
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
        if not self.loop or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
        self.loop.run_until_complete(coro_func(*args, **kwargs))

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
            print("yes window", target)
        elif id == "document":
            target = document
        else:
            target = document.getElementById(id)

        # if user not in development server and target not found
        # throw an error 
        if not target and (in_browser):
            if in_browser:
              raise ValueError(f"Element with id '{id}' not found. Cannot bind '{coroutine.__name__}' to '{event}'.")

        # Bind the event listener
        try:
            target.addEventListener(event, create_proxy(lambda e: self.dispatch(coroutine, e)))
        except Exception as e:
            raise RuntimeError(f"Failed to bind '{coroutine.__name__}' to '{event}' on target '{id}': {e}")


dispatcher = AsyncDispatcher()