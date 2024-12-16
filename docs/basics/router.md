# Zenaura Router Guide

The Zenaura Router, encapsulated in the `App` class, provides a powerful and flexible way to manage routes and navigation in your application.

Users will not feel they are going through pages in your application, everything will feel as if they were using single app and content appear as they switch pages.

### Key Features

- **Routing**: Define paths and associate them with components.
- **Navigation**: Move between different routes programmatically.
- **History Management**: Keep track of navigation history and handle forward/backward navigation.

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

app.run() # this will run the router on page load.
```

### Navigating Between Routes

Use the `navigate` method to programmatically navigate to a different route.

```python
await app.navigate("/about")
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

app.run()
```
