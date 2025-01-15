# Handling Forms in Zenaura

Handling forms efficiently in Zenaura involves managing form states and handlers in a structured way. This guide will walk you through creating and handling a form using a pattern that mimics dependency injection to keep your code clean and maintainable.

## Step 1: Define Needed presentaional components

First, create needed presentational components such as `Label`, `Input`, and `Button`, `TextArea`, and `Form`.

In `presentational.py`

```python
from zenaura.ui import div, label, input_, textarea, button, form

def Div(class_name, children):
    return div(*children, class_=class_name)

def Label(text):
    return label(text)

def Input(type_, name):
    return input_(type_=type_, name_=name, id=change_event_id)

def TextArea(name):
    return textarea(name_=name, id=change_event_id)

def Button(text, submit_button_id):
    return button(
        text,
        id=submit_button_id
    )

def UserForm(change_event_id, submit_button_id):
    return form(
        Div('form-group', [
            Label("Name:"),
            Input("text", "name"),
            Label("Email:"),
            Input("email", "email"),
            Label("Message:"),
            TextArea("message"),
            Button("submit", submit_button_id)
        ]),
        id=change_event_id
    )

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
        return UserForm("form_field_change", "submit_user_form")
```

## Step 3: Link the form to a page

finally we link the form to a page in `main.py`

### Application Component

```python
from zenaura.client.app import Route, App
from zenaura.client.page import Page
from public.routes import ClientRoutes
from public.components import UserFormComponent

form = UserFormComponent("starter")

dispatcher.bind("submit_user_form", "click",  form.handle_submit)
dispatcher.bind("form_field_change", "input",  form.handle_input)
# App and routing
router = App()
home_page = Page([form])

router.add_route(Route(
    title="Developer-Focused | Zenaura",
    path="/",
    page=home_page
))

# Run the application
app.run()

```

When user enter data in any of the form fields, input event is triggered from the browser, zenaura will dispach the form input change event, and the handler will search for the target name and use it to update the state.

Note there is no mutation, if you want to add validation you might want to add @mutator on handle change, so you can display error message.

Same with click event, the dispacher bind the user click event to from.handle_submit.
