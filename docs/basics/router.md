# Zenaura Router Guide

The Zenaura Router, encapsulated in the `App` class, provides a powerful and flexible way to manage routes and navigation in your application. This guide will walk you through the essential aspects of setting up and using the router.

When you build zenaura client app, zenaura will rewrite index.html as the pages wihin your application. Each page will have hidden, except /. Each route by default is set to ssr = False, ssr can be used to allow the client route to ignore the server side rendered components. 

When you visit a page within a zenaura application , the page previous page will be set to hidden, the current page hidden attribute will be removed.

This is simple way to achieve single page application UI/UX. 

## Overview

The `App` class manages routes, navigation, and the current location in a Zenaura application. It supports adding routes, navigating between pages, and handling browser history.

### Key Features

- **Routing**: Define paths and associate them with components.
- **Navigation**: Move between different routes programmatically.
- **History Management**: Keep track of navigation history and handle forward/backward navigation.
- **SSR Support**: Handle server-side rendered (SSR) pages.

## App Class

### Attributes

- `routes` (dict): Maps paths to their associated pages and titles.
- `paths` (list): List of registered paths.
- `history` (PageHistory): Manages the history of visited pages.

### Methods

- `__init__()`
- `navigate(path)`
- `handle_location()`
- `add_route(route)`
- `back()`
- `forward()`
- `get_current_route()`

## Setting Up the Router

### Initialization

To start using the router, instantiate the `App` class:

```python
from zenaura.client.app import App

app = App()
```

### Adding Routes

Define routes using the `add_route` method. Each route is represented by a `Route` object, which includes the path, page, title, and optional middleware and SSR settings.

```python
from zenaura.client.app import Route
from zenaura.client.component import Page

# Define your page components
home_page = Page([HomeComponent()])
about_page = Page([AboutComponent()])

# Add routes
app.add_route(Route(title="Home", path="/", page=home_page))
app.add_route(Route(title="About", path="/about", page=about_page))
```

### Navigating Between Routes

Use the `navigate` method to programmatically navigate to a different route.

```python
await app.navigate("/about")
```

### Handling Current Location

The `handle_location` method mounts the page associated with the current location.

```python
await app.handle_location()
```

### Navigation History

Navigate back and forth through the history stack using the `back` and `forward` methods.

```python
await app.back()
await app.forward()
```

### Getting the Current Route

Retrieve the current route's page and title using the `get_current_route` method.

```python
current_route = app.get_current_route() 
print(current_route)
```

### Handle params and queries 
Retrieve the current route with it's params and queries

```python
route = Route("test", "/test", Page([]), None)
router = App()
router.add_route(route)
self.window.location.pathname = "/test/123/123?k=1&k2=3"
current_route, info = self.router.get_current_route()
print(info["wildcard"]["params"]) #  ["123", "123"]
print(info["wildcard"]["query"]["k"]) # 1
print(info["wildcard"]["query"]["k2"]) # 3
```

### Handle wild card client routes
Zenaura router handles wild card routes if they are defined as follow :
```Python

route = Route("wildcard", "/users/*", Page([]), None)
router = App()
router.add_route(route)
self.window.location.pathname = "/users/123/123?k=1&k2=3"
current_route, info = self.router.get_current_route()
print(info["wildcard"]["params"]) #  ["123", "123"]
print(info["wildcard"]["query"]["k"]) # 1
print(info["wildcard"]["query"]["k2"]) # 3
```

### Adding middleware that runs before the route is matched
In every route you can define a middleware a specific logic that runs before zenaura match the route and mount the page:
```Py
middleware_order = []
def middleware1():
    middleware_order.append(1)
    print(middleware_order)

def middleware2():
    middleware_order.append(2)
    print(middleware_order)

def middleware():
    middleware1()
    middleware2()

route = Route("middlewareorder", "/middleware", Page([]), middleware)
router = App()
router.add_route(route)
await router.navigate("/middleware") 
# prints [1]
# prints [1, 2]
```

## Route Configuration

The `Route` class represents the configuration for each route.

### Attributes

- `title` (str): The title of the route.
- `path` (str): The path of the route.
- `page` (Page): The page component associated with the route.
- `middleware` (Optional[Callable]): Optional middleware function to be executed.
- `ssr` (bool): Indicates if the route is server-side rendered.

### Example

```python
route = Route(title="Home", path="/", page=home_page)
app.add_route(route)
```

## Handling Not Found Pages

If a route is not found, the `not_found` method displays a "Page Not Found" message.

```python
class NotFound(Page):
    def render(self):
        return Builder("div").with_text("Page Not Found").build()

app.not_found_page = NotFound()
```

## Example: Complete Router Setup

Here's an example demonstrating the full setup of the Zenaura Router:

```python
from zenaura.client.app import App, Route
from zenaura.client.component import Page
from zenaura.client.tags.builder import Builder

class HomeComponent(Page):
    def render(self):
        return Builder("div").with_text("Welcome to the Home Page").build()

class AboutComponent(Page):
    def render(self):
        return Builder("div").with_text("About Us").build()

class NotFound(Page):
    def render(self):
        return Builder("div").with_text("Page Not Found").build()

# Initialize the app
app = App()

# Define pages
home_page = Page([HomeComponent()])
about_page = Page([AboutComponent()])

# Add routes
app.add_route(Route(title="Home", path="/", page=home_page))
app.add_route(Route(title="About", path="/about", page=about_page))

# Set not found page
app.not_found_page = NotFound()

# Handle initial location
await app.handle_location()

# Navigate to a different route
await app.navigate("/about")

# Navigate back and forth
await app.back()
await app.forward()
```

## Summary

The Zenaura Router (`App` class) provides a robust way to manage routes and navigation within your application. By defining routes, handling navigation, and managing browser history, you can create a seamless user experience. This guide covers the essential methods and setup needed to get started with routing in Zenaura.