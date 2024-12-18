import functools
import asyncio 
from zenaura.client.dispatcher import dispatcher
from zenaura.client.dom import zenaura_dom



def mutator(coroutine):
    """
    Decorator to automatically render the DOM after the decorated coroutine executes.

    This decorator is useful for functions that modify the state of the application,
    triggering a re-rendering of the DOM to reflect the changes.

    Args:
        coroutine: The function to be decorated.

    Returns:
        wrapper_func: A wrapper function that executes the original function and then renders the DOM.

    Raises:
        TypeError: If `func` is not a callable.
    """

    if not callable(coroutine):
        raise TypeError("mutator can only decorate callables")
    
    if not asyncio.iscoroutine(coroutine) and not asyncio.iscoroutinefunction(coroutine):
        raise TypeError(f"'{coroutine}' is not a valid aysncio coroutine. use @mutates to decorate regular python callbacks'.")


    @functools.wraps(coroutine)
    async def wrapper_func(component, *args, **kwargs):
        """
        Wrapper function that executes the original function and then renders the DOM.

        Args:
            component: The instance of the class.
            *args: Positional arguments for the original function.
            **kwargs: Keyword arguments for the original function.

        Returns:
            None
        """
        dispatcher.dispatch(coroutine, component, *args, **kwargs)
        dispatcher.dispatch(zenaura_dom.render, component)

    return wrapper_func


def mutates(func):
    """
    Decorator to automatically render the DOM after the decorated function executes.

    This decorator is useful for functions that modify the state of the application,
    triggering a re-rendering of the DOM to reflect the changes.

    Args:
        coroutine: The function to be decorated.

    Returns:
        wrapper_func: A wrapper function that executes the original function and then renders the DOM.

    Raises:
        TypeError: If `func` is not a callable.
    """

    if not callable(func):
        raise TypeError("mutator can only decorate functions")
    
    if asyncio.iscoroutine(func) or asyncio.iscoroutinefunction(func):
        raise TypeError(f"'{func}' is an a aysncio coroutine. use @mutator to decorate coroutines'.")


    @functools.wraps(func)
    def wrapper_func(component, *args, **kwargs):
        """
        Wrapper function that executes the original function and then renders the DOM.

        Args:
            component: The instance of the class.
            *args: Positional arguments for the original function.
            **kwargs: Keyword arguments for the original function.

        Returns:
            None
        """
        func(component, *args, **kwargs)
        dispatcher.dispatch(zenaura_dom.render, component)
    return wrapper_func
