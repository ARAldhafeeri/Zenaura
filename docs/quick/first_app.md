# Creating Your First Zenaura App

In this example, we will walk through creating your first Zenaura application and cover basic concepts.

The Zenaura library includes a simple CLI tool to streamline development.

---

## **CLI Commands**

The following commands are available via the CLI:

- `init`: Creates a basic Zenaura application with pre-configured files.
- `build`: Builds the Zenaura application.
- `run`: Runs the development server.

---

### **Initializing a Basic Zenaura Application**

```bash
zenaura init
```

This command generates a basic Zenaura application with essential files, enabling you to get started quickly.

### **Auto-Generated Files**

The `init` command creates the following structure:

- `build.py`: Script for building the Zenaura application.
- `index.py`: Entry point for a simple Zenaura server.
- `public/main.py`: Main file for importing components, creating pages, and configuring the client router.
- `public/main.css`: Primary CSS file for styling.
- `public/config.json`: PyScript Pyodide configuration file.
- `__init__.py`: Contains code intended to run in the browser.

---

### **Building the Application**

```bash
zenaura build
```

This command generates the `index.html` file for your application.

---

### **Running the Development Server**

```bash
zenaura run
```

Runs the server on `localhost:5000`. Open the URL in your browser to see the rendered HTML.

---

## **Example: Your First Zenaura App**

Below is an example of a basic Zenaura application using the new `zenaura.ui` tags for creating components and pages.

#### **Define the Component**

```python
from zenaura.client.component import Component
from zenaura.ui import div, h1, h2, img

class ZenauraStarter(Component):
    def render(self):
        return div(
            div(
                img(src="./public/logo.png", width=255, height=255, alt="starterLogo"),
                h1("The Python Framework For"),
                h2("Building Modern Web User Interface"),
            ),
            class_="zenaura"
        )
```

#### **Configure the App and Routing**

```python
from zenaura.client.app import Route, App
from zenaura.client.page import Page

starter = ZenauraStarter()

# App and routing
app = App()
home_page = Page([starter])

app.add_route(Route(
    title="Developer-Focused | Zenaura",
    path="/",
    page=home_page
))

app.run()
```

---

### **Rendered HTML Output**

```html
<div class="zenaura">
  <div>
    <img src="./public/logo.png" width="255" height="255" alt="starterLogo" />
    <h1>The Python Framework For</h1>
    <h2>Building Modern Web User Interface</h2>
  </div>
</div>
```

The application is live with hot-reloading enabled, ensuring that any code changes automatically refresh the page.

---

### **Adding New Components**

To extend the application, you can define additional components and add them to your pages.

#### **Define a New Component**

```python
from zenaura.client.component import Component
from zenaura.ui import h1

class SimpleHeader(Component):
    def render(self):
        return h1("Welcome to Zenaura!")
```

#### **Add the Component to the Page**

```python
header = SimpleHeader()
home_page = Page([starter, header])  # Add new component to the page
```

#### **Rendered HTML Output**

```html
<div class="zenaura">
  <div>
    <img src="./public/logo.png" width="255" height="255" alt="starterLogo" />
    <h1>The Python Framework For</h1>
    <h2>Building Modern Web User Interface</h2>
  </div>
</div>
<h1>Welcome to Zenaura!</h1>
```
