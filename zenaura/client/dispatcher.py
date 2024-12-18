import asyncio 
from zenaura.web.utils import document, window, in_browser, create_proxy


class AsyncDispatcher:
    def dispatch(self, coro_func, *args, **kwargs):
        """
        Wrap asyncio.run to schedule and run the given coroutine.
        
        :param coro_func: The coroutine function to execute.
        :param args: Positional arguments for the coroutine.
        :param kwargs: Keyword arguments for the coroutine.
        """ 
        # nest_aysncio loops throws this error in browser :
        # ValueError: Can't patch loop of type <class 'pyodide.webloop.WebLoop'>
        # use pyodide  pyodide.webloop in browser.        
        if in_browser:
            print("in browser , lslksdfkj")
            asyncio.get_running_loop().run_until_complete(coro_func(*args, **kwargs))

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

        # Bind the event listener
        try:
            target.addEventListener(event, create_proxy(lambda e: self.dispatch(coroutine, e)))
        except Exception as e:
            print(f"WARNING:  ignoring to bind in build '{coroutine.__name__}' to '{event}' on target '{id}'")


dispatcher = AsyncDispatcher()