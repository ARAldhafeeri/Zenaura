## Layouts

Layouts in Zenaura allow you to define global components that exist within the root `div` for every route. Like other Zenaura components, their state is preserved. Layouts are a way to organize your Zenaura application, ensuring consistency and reusability of common UI elements.

The typical structure is:
```
Top Components -> App Routes -> Bottom Components
```

### Example Structure
```html
<div id="root">
    <nav></nav> <!-- Global top-of-page navigation component -->
    <div id="page1"></div>
    <div id="page2" hidden></div>
    <div id="page3" hidden></div>
    <div id="page4" hidden></div>
    <footer></footer> <!-- Global bottom-of-page footer component -->
</div>
```

## Example of Creating a Layout

### Step 1: Define Layout in `main.py`
```python
from zenaura.client.app import Route, App
from zenaura.client.page import Page
from zenaura.client.layout import Layout
from public.routes import ClientRoutes
from public.components.header import Header
from public.components.intro import IntroSection
from public.components.footer import Footer
from public.components.examples import Example

# Instantiate components
nav_bar_header = Header(router)
intro_section = IntroSection()
footer = Footer()
example = Example()

# Define pages
home_page = Page([intro_section])
example_page = Page([example])

# Define routes
router.add_route(Route(
    title="Developer-Focused | Zenaura",
    path=ClientRoutes.home.value,
    page=home_page
))

router.add_route(Route(
    title="Example",
    path=ClientRoutes.examples.value,
    page=example_page
))

# Create the app layout
my_app_layout = Layout(
    top=[nav_bar_header],    # Components to appear before the routes
    routes=app.routes,       # Application routes (pages)
    bottom=[footer]          # Components to appear after the routes
)

# optional : pass layout to router to trigger global components attached lifecycle method
router.layout = my_app_layout
```

### Step 2: Hydrate Layout in `build.py`
```python
from public.main import my_app_layout
from zenaura.client.server import ZenauraServer

ZenauraServer.hydrate_app_layout(my_app_layout, scripts=[
    '<link rel="stylesheet" href="public/gigavolt.min.css">',
    '<link rel="stylesheet" href="public/output.css">',
    '<script src="public/highlight.min.js"></script>',
    '<script src="public/python.min.js"></script>',
    '<script>hljs.highlightAll();</script>',
    """
    <script>
        const ws = new WebSocket("ws://localhost:5000/refresh");
        ws.onmessage = () => {
            console.log("Reloading...");
            location.reload();
        };
    </script>
    """
])
```

This setup ensures that the navigation bar (`nav_bar_header`) and footer (`footer`) components appear on every page of the application. You can add multiple components to the top or bottom sections as needed for your application layout.


## Conclusion

By using app layout for global component this insure maximum reuseability and yields more onrganized maintained codebase, even though one of the guides encourage the use of higher order components, however this approach is far more optimized. 
