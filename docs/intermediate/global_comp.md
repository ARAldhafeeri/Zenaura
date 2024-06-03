## Handling Global Components with Higher Order Components

Global components are components used in multiple places within an application. Examples include navigation bars, footers, or modals that appear consistently across various pages. To efficiently manage these components and adhere to the DRY (Don't Repeat Yourself) principle, you can utilize Higher Order Components (HOCs).

## Why Use Global Components?

- **Maintainability**: Enhances the codebase's maintainability and comprehensibility by centralizing component logic.
- **Evolvability**: Facilitates easier updates and changes. For instance, modifying a nav bar component will automatically reflect the changes across all the pages where it is used.

## Step 1: Create a Global Component

Design your global component. This can range from a simple navigation bar to a complex global modal that appears with different content throughout the application. For the simplicity of this tutorial, we'll create a nav bar component.

### Example: Creating a NavBar Component
In `presentational.py`

```python
from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Node, Attribute

def Paragraph(text, class_name=None):
    builder = Builder('p').with_text(text)
    if class_name:
        builder = builder.with_attribute('class', class_name)
    return builder.build()

def Header1(text):
    return Builder('h1').with_text(text).build()

def Div(class_name, children):
    div = Builder('div').with_attribute('class', class_name).build()
    div.children = children
    return div

def NavItemText(href, text):
    return Builder('a').with_attribute('href', href).with_text(text).build()

```
in `main.py` we create a `NavBar` component:

```python
from zenaura.client import Component, Reuseable
from public.presentational import Div, NavItemText, Header1, Paragraph
from zenaura.client.app import App, Route
from zenaura.client.page import Page

@Reuseable
class NavBar(Component):
    def render(self):
        return Div("navbar",[
            NavItemText("Home", "/"),
            NavItemText("About", "/about"),
            NavItemText("Contact", "/contact")
        ])
```

## Step 2: Create a Higher Order Component (HOC)

Higher Order Components are functions that take a component and return a new component with additional properties or behavior. We'll create an HOC that wraps a given page component with our `NavBar` component.

### Example: Creating an HOC

Create a new file `main.py` and define the HOC:

```python
# previous code 
def with_navbar(page_children):
    return [
        NavBar(),
        *page_children
    ]
```
Note: here we are passing the global component, and the rest of the page children.

## Step 3: Apply the HOC to Your Page Components

Now, you can apply the `with_navbar` HOC to your page components to include the `NavBar` globally.

### Example: Applying the HOC

Let's say you have a `HomePage`, `AboutPage`, and `ContactPage` component defined in `main.py`:

```python


class HomePage(Component):
    def render(self):
        return Div("homepage", [
            Header1("Home Page"), 
            Paragraph("This is the home page")
        ])

class AboutPage(Component):
    def render(self):
        return Div("aboutpage", [
            Header1("About Page"), 
            Paragraph("This is the about page")
        ])

class ContactPage(Component):
    def render(self):
        return Div( "contactpage", [
            Header1("Contact Page"), 
            Paragraph("This is the contact page")
        ])

```

You can apply the `with_navbar` HOC to this component as follows:

``` python
router = App()
router.add_route(
    Route(
        "Home", 
        "/",
        Page(
            with_navbar([HomePage()])
       ) 
    )
)

router.add_route(
    Route(
        "About", 
        "/about",
        Page(
            with_navbar([AboutPage()])
        ) 
    )
)

router.add_route(
    Route(
        "Contact", 
        "/contact",
        Page(
            with_navbar([ContactPage()])
        ) 
    )
)

```

Full `main.py`:

```python 
from zenaura.client.component import Component, Reuseable
from public.presentational import Div, NavItemText, Header1, Paragraph
from zenaura.client.app import App, Route
from zenaura.client.page import Page
import asyncio
@Reuseable
class NavBar(Component):
    def render(self):
        return Div("navbar",[
            NavItemText("Home", "/"),
            NavItemText("About", "/about"),
            NavItemText("Contact", "/contact")
        ])
    

def with_navbar(page_children):
    return [
        NavBar(),
        *page_children
    ]

class HomePage(Component):
    def render(self):
        return Div("homepage", [
            Header1("Home Page"), 
            Paragraph("This is the home page")
        ])

class AboutPage(Component):
    def render(self):
        return Div("aboutpage", [
            Header1("About Page"), 
            Paragraph("This is the about page")
        ])

class ContactPage(Component):
    def render(self):
        return Div( "contactpage", [
            Header1("Contact Page"), 
            Paragraph("This is the contact page")
        ])

router = App()
router.add_route(
    Route(
        "Home", 
        "/",
        Page(
            with_navbar([HomePage()])
       ) 
    )
)

router.add_route(
    Route(
        "About", 
        "/about",
        Page(
            with_navbar([AboutPage()])
        ) 
    )
)

router.add_route(
    Route(
        "Contact", 
        "/contact",
        Page(
            with_navbar([ContactPage()])
        ) 
    )
)

# Run the application
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(router.handle_location())

```
Basically, we return the page children with the global component, as a Page in zenaura expect a list of components. This way, whenever we need the navbar with a specific page, we pass with_navbar HOC to the page component, with the page children as list.

## Conclusion

By creating global components and using Higher Order Components (HOCs), you can efficiently manage and reuse common UI elements across your application. This approach not only improves maintainability but also ensures a consistent user experience across different pages.

Explore further by creating more complex global components and integrating them using HOCs to enhance your application's architecture and usability.