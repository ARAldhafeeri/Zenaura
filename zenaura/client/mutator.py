from zenaura.client.dom import zenaura_dom
import functools

def mutator(func):
    """
    Decorator function to render the DOM after the execution of the decorated function.

    Args:
    - func: The function to be decorated.

    Returns:
    - wrapper_func: The wrapper function that executes the original function and then renders the DOM.
    """
    @functools.wraps(func)
    async def wrapper_func(self, *args, **kwargs):
        """
        Wrapper function that executes the original function and then renders the DOM.

        Args:
        - self: The instance of the class.
        - *args: Positional arguments for the original function.
        - **kwargs: Keyword arguments for the original function.

        Returns:
        - None
        """
        await func(self, *args, **kwargs)
        await zenaura_dom.render(self)
    return wrapper_func