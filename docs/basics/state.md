# Zenaura Component State Management

State management is a crucial aspect of building dynamic and interactive user interfaces. In Zenaura, components can maintain and update their state to reflect changes in the application.

## Understanding State in Components

State in Zenaura components refers to the data that changes over time and drives the UI. Each stateful component can hold its own state, which can be updated in response to user interactions or other events.

### Example of a Stateful Component

Here's an example of a component managing multiple pieces of state:

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator

class UserProfile(Component):
    def __init__(self):
        super().__init__()
        self.set_state({
            "name": "John Doe",
            "age": 30
        })

    @mutator
    async def update_name(self, event):
        new_name = event.target.value
        self.set_state({"name": new_name})

    @mutator
    async def increment_age(self, event):
        current_age = self.get_state()["age"]
        self.set_state({"age": current_age + 1})

    def render(self):
        state = self.get_state()
        return Builder("div").with_children([
            Builder("h1").with_text(f"Name: {state['name']}").build(),
            Builder("input").with_attribute("value", state['name']).with_attribute("id", "user_profile_name").build(),
            Builder("h2").with_text(f"Age: {state['age']}").build(),
            Builder("button").with_text("Increase Age").with_attribute("id", "user_profile_age").build()
        ]).build()

user_profile = UserProfile()
dispatcher.bind("user_profile_name", "change",  user_profile.update_name)
dispatcher.bind("user_profile_age", "change",  user_profile.increment_age)
```

The dispacher binds change events to input fields, whenever data changes the state is updated, and @mutator will trigger zenaura vDOM to show updates to the user.
