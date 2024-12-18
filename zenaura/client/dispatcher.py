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
        if in_browser:
            asyncio.get_running_loop().run_until_complete(coro_func(*args, **kwargs))

    def bind(self, id, event, maybe_awaitable):
        """
        Subscribe an event to an element, window, or document and dispatch a sync or async callback.
        Ensures the provided function has the correct signature.

        :param id: ID attached to the component, or 'window'/'document' for global bindings.
        :param event: Event name (e.g., "click", "resize", "keydown").
        :param coroutine: Callback coroutine function.
        :return: None if binding succeeds; raises an exception otherwise.
        """

        if not callable(maybe_awaitable):
            raise TypeError("The callback must be callable.")

        target = None

        # Determine the target based on id
        if id == "window":
            target = window
        elif id == "document":
            target = document
        else:
            target = document.getElementById(id)

        # Bind the event listener
        try:
            print(target, )
            if  asyncio.iscoroutine(maybe_awaitable) and  asyncio.iscoroutinefunction(maybe_awaitable):
                target.addEventListener(event, create_proxy(lambda e: self.dispatch(maybe_awaitable, e)))
            else:
                target.addEventListener(event, create_proxy(lambda e: maybe_awaitable(e)))
        except Exception as e:
            print(f"WARNING:  ignoring to bind in build '{maybe_awaitable.__name__}' to '{event}' on target '{id}'")


dispatcher = AsyncDispatcher()