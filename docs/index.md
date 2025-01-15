### Introduction
Zenaura is a Python-based framework designed for building web applications with simplicity, developer experience, and event-driven design.

### Architecture Guidelines
- Modular components for scalability.
- Event-driven architecture via `dispatcher.bind`.
- Python-first approach, enabling PyScript and Pyodide integration.

### Why Zenaura
- Simplified async programming.
- Intuitive routing and state management.
- Easy integration with Python and JS packages.

### Rules
#### Do's
1. Use `dispatcher.bind` and `dispatcher.dispatch` for event management:
   ```python
   dispatcher.bind("button-id", "click", callback_function)
   ```
2. Ensure `render` in components has a single parent and one child level:
   ```python
   def render(self):
       return div(
           h1("Parent"),
           div("Child 1"),
           div("Child 2")
       )
   ```
   Use functional components for nested children:
   ```python
   def child1(prop1, prop2):
       return div(
           p(prop1),
           p(prop2)
       )
   ```
3. Follow the hierarchy: `HTML tags -> Functional Components -> Class Components -> Pages -> Layout`.
   - For multiple layouts, use:
     - Microfrontend architecture.
     - Conditional rendering (discussed in Layout section).
4. Use `subject` and `observer` for shared states:
   ```python
   from zenaura.client.observer import subject
   state = subject(shared_data)
   ```

#### Don'ts
1. **Don’t** use inline event handlers like `on_click`.
2. **Don’t** deeply nest child elements in `render`.
3. **Don’t** use `builder` calls for UI construction.
4. **Don’t** hard-code shared states or use global variables.

---

## Quick Overview

### Basics
#### HTML Tags
Simplified tag usage:
```python
from zenaura.ui import div, h1, button
from zenaura.client.component import Component

class MyComponent(Component):
    def render(self):
        return div(
            h1("Welcome to Zenaura"),
            button("Click Me", id="my-button"),
        )
```
#### Special Attributes
Attributes conflicting with Python keywords use `_` suffix:
```python
div("Hello World", class_="greeting")
input_(id="my_input")
```

#### Components
Define reusable components:
```python
from zenaura.client.component import Component, Reuseable

@Reuseable
class WelcomeComponent(Component):
    def render(self):
        return div("Welcome to Zenaura", class_="welcome")
```
Zenaura prompts for `@Reuseable` if missing.

#### State Management
Integrated event-driven patterns:
```python
class Counter(Component):
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
```

#### Dispatcher
Bind events with `dispatcher.bind`:
```python
from zenaura.client.dispatcher import dispatcher

dispatcher.bind("my-button", "click", counter.increment)
```
Dispatch events with `dispatcher.dispatch`.

### Beyond Basics
#### Router
Simplified routing:
```python
from zenaura.client.app import App
from zenaura.client.page import Page

app = App()
home_page = Page([WelcomeComponent()])
app.add_route("/", home_page)
app.run()
```

#### Pages
Encapsulate components:
```python
from zenaura.client.page import Page

home_page = Page([WelcomeComponent()])
```

#### Layout
Define app layout:
```python
from zenaura.client.layout import Layout
from zenaura.client.app import App

app = App()

my_app_layout = Layout(
    top=[NavigationAuthNotAuth],
    routes=app.routes,
    bottom=[FooterAuthNotAuth]
)
```

#### Global State
Share state between components:
```python
from zenaura.client.observer import Subject

counter_subject = Subject()
counter_subject.state = {"counter1": 0}

class CounterObserver(Observer):
    pass

class Counter1(Component, CounterObserver):
    async def increment(self, event):
        counter_subject.state["counter1"] += 1
        counter_subject.notify()

    def update(self, value):
        # Logic for state update
```

#### Forms
Handle forms:
```python
def render_form():
    return form(
        input_(type="text", id="name"),
        button("Submit", id="submit-button")
    )
```

### Advanced Concepts
#### Virtual DOM
Minimizes re-rendering by efficiently patching changes.

#### Component Lifecycle
- `attached`: Runs after mounting.
- `on_mutation`: Runs before DOM updates.
- `on_settled`: Runs after DOM updates.

#### API Integration
Fetch data with async handlers:
```python
from zenaura.client.mutator import mutator

@mutator
async def fetch_data():
    data = await fetch("/api/data")
    return data
```

#### PyScript and Pyodide
- PyScript: Run Python in the browser.
- Pyodide: Python interpreter in WebAssembly.

#### Deployment
- Configure `config.json`.
- Host static files on a CDN/server.

#### External JS or CSS
Add scripts to `build.py`:
```python
from zenaura.server import ZenauraServer
ZenauraServer.hydrate_app(app, scripts=[
    """
    <script>
        const ws = new WebSocket("ws://localhost:5000/refresh");
        ws.onmessage = () => location.reload();
    </script>
    """
])
```
Import JS dynamically:
```python
from zenaura.web.utils import to_js

def use_js_function():
    from js import my_js_function
    my_js_function(to_js({"data": 1}))
```

#### External Python Packages
List dependencies in `config.json`:
```json
"packages": ["numpy", "pandas"]
```



### Zenaura CLI

Zenaura cli is a tool to use, to quickly intialize, build, and run application

- `zenaura init` will initialize basic zenaura application.
- `zenaura build` will build the zenaura application, and run everytime you change a file in zenaura public folder.
- `zenaura run` run the application on port 5000, you can change the port from index.py

### Zenaura UI

Multiple ready to use UI components.

```Python
from zenaura.ui import Button, BreadCrumbs
```

### Zenaura Charts

Multiple ready to use charts, built on top of chartjs

```
from zenaura.ui.charts import ChartThis, Canvas

config = {} # chartjs config as python dict
async def chart_logic(self):
   ChartThis(config, self.chart_name)

def my_chart():
   return Canvas("bar_chart")
```
