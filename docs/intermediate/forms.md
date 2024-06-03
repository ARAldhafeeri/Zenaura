# Handling Forms in Zenaura

Handling forms efficiently in Zenaura involves managing form states and handlers in a structured way. This guide will walk you through creating and handling a form using a pattern that mimics dependency injection to keep your code clean and maintainable.

## Step 1: Define Needed presentaional components 

First, create needed presentational components such as `Label`, `Input`, and `Button`, `TextArea`, and `Form`.

In `presentational.py`

```python
from zenaura.client.tags.builder import Builder

def Div(class_name, children):
    div = Builder('div').with_attribute('class', class_name).build()
    div.children = children
    return div

def Label(text):
    return Builder('label').with_text(text).build()

def Input(type, name, oninput):
    return Builder('input').with_attributes(
        type=type,
        name=name,
    ).with_attribute(
        "py-change", oninput
    ).build()

def TextArea(name, oninput):
    return Builder('textarea').with_attributes(
        name=name,
    ).with_attribute(
        "py-change", oninput
    ).build()

def Button(type, text):
    return Builder('button').with_attributes(
        type=type
    ).with_text(text).build()

def UserForm(onsubmit, handle_input):
    return Builder('form').with_attribute(
        "py-submit", onsubmit
    ).with_children(
        Div('form-group', [
            Label("Name:"),
            Input("text", "name", handle_input),
            Label("Email:"),
            Input("email", "email", handle_input),

            Label("Message:"),
            TextArea("message", handle_input),
            Button("submit", "Submit")
        ])
    ).build()
```

## Step 2: We will create our Form component 

The form component will handle 3 fields, name, email, message, and submit button.

in `components.py`

```python
from zenaura.client.component import Component
from public.presentational import UserForm

class UserFormComponent(Component):
    def __init__(self, instance_name):
        super().__init__()
        self.instance_name = instance_name
        self.state = {

                "name": "",

                "email": "",

                "message": ""

            }

    def update_state(self, field, value):

        self.state[field] = value
        
    def submit_form(self):

        print("Form submitted with:", self.state)
    def handle_input(self, event):
        field = event.target.name
        value = event.target.value
        self.update_state(field, value)
        print(self.state)


    def handle_submit(self, event):
        event.preventDefault()
        self.submit_form()

    def render(self):
        return UserForm(f"{self.instance_name}.handle_submit",f"{self.instance_name}.handle_input")
```

## Step 3: Link the form to a page

finally we link the form to a page in `main.py`

### Application Component

```python
from zenaura.client.app import Route, App
from zenaura.client.page import Page
from public.routes import ClientRoutes
from public.components import UserFormComponent
import asyncio

starter = UserFormComponent("starter")

# App and routing
router = App()
home_page = Page([starter])

router.add_route(Route(
    title="Developer-Focused | Zenaura",
    path=ClientRoutes.home.value,
    page=home_page
))

# Run the application
event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(router.handle_location())

```

## Step 4: build and run the application 

```Python 
zenaura build
```
```Python 
zenaura run
```

Note in the console when we type in the input field, the state is updated and printed out, when we submit we get the following message in the console of the browser 

```
Form submitted with: {'name': 'sdf', 'email': 'sdf@gmail.com', 'message': 'alksdfhe'}
```

## Summary

In this guide, we've demonstrated how to handle forms in Zenaura using a pattern that mimics dependency injection. By separating the form handling logic into a dedicated `FormHandler` class and passing it as a dependency to the form component, we've achieved a clean and maintainable structure.

### Key Points:
- **FormHandlers**: Manages form state and submission logic, it can live within the form component or seperated class.
- **Form Component**: Handles user input and form submission, utilizing the `FormHandler`.
- **Application Component**: Integrates the form into the application and passes the handler as a dependency.
- **Main Entry Point**: Renders the application.

This pattern keeps your codebase modular and promotes separation of concerns, making it easier to manage and extend.


The example is available in the examples repository under Handling_forms directory.
