# Handling User Events in Zenaura

In Zenaura, handling user events is a key aspect of creating interactive and dynamic applications. This guide will cover how Zenaura processes user events, updates the state, and re-renders components.

## Overview

The workflow in Zenaura for handling user events follows this sequence:

1. **User Event**: An event (e.g., click, input change) occurs in the browser.
2. **Mutate State**: The event triggers a mutator method in the component, which updates the component's state.
3. **Re-render Component**: Zenaura compares the new state with the previous state and generates a virtual DOM diff.
4. **Render Component on the Browser**: The diff is applied to update the actual DOM in the browser.

### Example of Handling User Events

Let's illustrate this with an example. We will create a simple counter component that increments and decrements a count value based on button clicks.

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator
from zenaura.client.tags import Node, Attribute
from zenaura.client.
class Counter(Component):
    def __init__(self):
        super().__init__(instance_name)
        self.set_state({"count": 0})
        self.instance_name = instance_name

    @mutator
    async def increment(self, event):
        self.set_state({"count": self.get_state()["count"] + 1})

    @mutator
    async def decrement(self, event):
        self.set_state({"count": self.get_state()["count"] - 1})

    def render(self):
        count = self.get_state()["count"]
        return Builder("div").with_children([
            Builder("h1").with_text(f"Count: {count}").build(),
            Builder("button").with_text("+").with_attribute("id", f"{self.instance_name}.increase").build(),
            Builder("button").with_text("-").with_attribute("id", f"{self.instance_name}.decrease").build()
        ]).build()

counter1 = Counter("counter1")
# dispatcher.bind("element_id", "event_name",  component.callback)
dispatcher.bind("counter1.increase", "click",  simple_form.increment)
dispatcher.bind("counter1.decrease", "click",  simple_form.decrement)
```

### Explanation

1. **User Event**: When the user clicks the "+" or "-" button, a `click` event is triggered.
2. **Mutate State**: The event handler (`increment` or `decrement` method) is called. These methods are decorated with `@mutator`, indicating that they will change the component's state.
3. **Re-render Component**: After the state is updated, Zenaura automatically triggers a re-render of the component. The `render` method is called again with the updated state and the updates are shown on the browser.
