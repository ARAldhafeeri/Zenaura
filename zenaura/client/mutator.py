from zenaura.client.dom import zenaura_dom
import functools

def mutator(func):
    """
    Decorator to automatically render the DOM after the decorated function executes.

    This decorator is useful for functions that modify the state of the application,
    triggering a re-rendering of the DOM to reflect the changes.

    Args:
        func: The function to be decorated.

    Returns:
        wrapper_func: A wrapper function that executes the original function and then renders the DOM.

    Raises:
        TypeError: If `func` is not a callable.
    """

    if not callable(func):
        raise TypeError("mutator can only decorate functions")

    @functools.wraps(func)
    async def wrapper_func(self, *args, **kwargs):
        """
        Wrapper function that executes the original function and then renders the DOM.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the original function.
            **kwargs: Keyword arguments for the original function.

        Returns:
            None
        """

        await func(self, *args, **kwargs)
        await zenaura_dom.render(self)

    return wrapper_func
