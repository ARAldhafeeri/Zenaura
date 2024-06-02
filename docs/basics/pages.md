# Working with Pages in Zenaura

Pages in Zenaura serve as the top-level structure for organizing and rendering your application’s components. This guide will cover the basics of creating and managing pages, adding components to them, and setting up routing to navigate between different pages.

## Overview

A page in Zenaura is essentially a container for components. It defines what components should be displayed and how they are structured. Pages are managed by the router, which handles navigation and rendering based on the application's routes.

### Key Concepts

- **Page**: A top-level container for components.
- **Component**: A building block of the UI, which can be stateful or stateless.
- **Router**: Manages navigation and rendering of pages based on URL routes.

## Creating a Page

To create a page, you need to define which components it contains. Here’s an example of setting up a simple page with some components:

```python
from zenaura.client.page import Page
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder

# Define some sample components
class Header(Component):
    def render(self):
        return Builder("h1").with_text("Welcome to Zenaura!").build()

class Footer(Component):
    def render(self):
        return Builder("footer").with_text("© 2024 Zenaura Inc.").build()

class MainContent(Component):
    def render(self):
        return Builder("div").with_text("This is the main content area.").build()

# Create a page and add components to it
header = Header()
footer = Footer()
main_content = MainContent()

home_page = Page([header, main_content, footer])
```

### Explanation

1. **Define Components**: In this example, we define three simple components: `Header`, `Footer`, and `MainContent`.
2. **Create a Page**: We then create a `Page` instance and pass a list of components that should be rendered on this page.

## Adding Pages to the Router

To enable navigation between pages, we need to add them to the router. The router manages different routes and renders the appropriate page based on the current URL.

```python
from zenaura.client.app import Route, App
from public.routes import ClientRoutes

# Initialize the router
router = App()

# Add routes for different pages
router.add_route(Route(
    title="Home",
    path=ClientRoutes.home.value,
    page=home_page
))

# Add more routes as needed
```

### Explanation

1. **Initialize Router**: We create an instance of the `App` class, which serves as the router.
2. **Add Routes**: We add a route for the `home_page` we created earlier. Each route is defined by a title, a path, and the page to be rendered.

## Navigation Between Pages

To navigate between pages, you can use the `navigate` method provided by the router. This can be done within component event handlers or other parts of your application.

```python
class NavigationComponent(Component):
    async def go_to_home(self, event):
        await router.navigate(ClientRoutes.home.value)

    def render(self):
        return Builder("button").with_text("Go to Home").with_attribute("py-click", f"{self.instance_name}.go_to_home").build()
```

### Explanation

1. **Navigation Method**: The `go_to_home` method uses the `navigate` method of the router to change the current URL to the home path.
2. **Event Handler**: The `py-click` attribute in the `Builder` method links the button click event to the `go_to_home` method, enabling navigation when the button is clicked.

## Example: Complete Application

Let’s put everything together in a complete example:

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.page import Page
from zenaura.client.app import Route, App
from public.routes import ClientRoutes
from zenaura.client.tags.node import Node, Attribute

# Define Components
class Header(Component):
    def render(self):
        return Builder("h1").with_text("Welcome to Zenaura!").build()

class Footer(Component):
    def render(self):
        return Builder("footer").with_text("© 2024 Zenaura Inc.").build()

class MainContent(Component):
    def render(self):
        return Builder("div").with_text("This is the main content area.").build()

class NavigationComponent(Component):
    async def go_to_home(self, event):
        await router.navigate(ClientRoutes.home.value)

    def render(self):
        return Builder("button").with_text("Go to Home").with_attribute("py-click", f"{self.instance_name}.go_to_home").build()

# Create Pages
header = Header()
footer = Footer()
main_content = MainContent()
navigation = NavigationComponent()

home_page = Page([header, main_content, footer])
navigation_page = Page([navigation, footer])

# Initialize Router
router = App()

# Add Routes
router.add_route(Route(
    title="Home",
    path=ClientRoutes.home.value,
    page=home_page
))

router.add_route(Route(
    title="Navigation",
    path=ClientRoutes.navigation.value,
    page=navigation_page
))

# Start the App
if __name__ == "__main__":
    import asyncio
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(router.handle_location())
```

### Explanation

1. **Components and Pages**: We define components and create two pages: `home_page` and `navigation_page`.
2. **Router Setup**: We initialize the router, add routes for both pages, and start the application.

## Best Practices

1. **Component Organization**: Organize your components into separate files or modules for better maintainability.
2. **Consistent Structure**: Follow a consistent structure for defining and adding pages to the router.
3. **Reusability**: Use reusable components wherever possible to keep your code DRY (Don't Repeat Yourself).

## Summary

In this guide, we've covered how to create and manage pages in Zenaura. We explored adding components to pages, setting up the router, and handling navigation. By following these principles, you can build a well-structured and navigable Zenaura application.
