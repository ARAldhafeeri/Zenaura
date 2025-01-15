### Handling User Events in Zenaura (Revised)

In Zenaura, handling user events is a key aspect of creating interactive and dynamic applications. This guide will cover how Zenaura processes user events, updates the state, and re-renders components.

## Overview

The workflow in Zenaura for handling user events follows this sequence:

1. **User Event**: An event (e.g., click, input change) occurs in the browser.
2. **Mutate State**: The event triggers a mutator method in the component, which updates the component's state.
3. **Re-render Component**: Zenaura compares the new state with the previous state and generates a virtual DOM diff.
4. **Render Component on the Browser**: The diff is applied to update the actual DOM in the browser.

### Example of Handling User Events

```python
from zenaura.client.component import Component
from zenaura.client.tags import div, h1, button
from zenaura.client.mutator import mutator
from zenaura.client.dispatcher import dispatcher

class Counter(Component):
    def __init__(self, instance_name):
        super().__init__()
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
        return div(
            h1(f"Count: {count}"),
            button("+", id=f"{self.instance_name}.increase"),
            button("-", id=f"{self.instance_name}.decrease"),
        )

# Create an instance of the Counter component
counter1 = Counter("counter1")

# Bind events using the dispatcher
dispatcher.bind("counter1.increase", "click", counter1.increment)
dispatcher.bind("counter1.decrease", "click", counter1.decrement)
```

### Explanation of Changes

1. **Replacing `Builder` with `tags`:**

   - The `tags` library (`div`, `h1`, `button`, etc.) is used for a cleaner and more readable declarative syntax.
   - Each tag directly represents the HTML structure of the component.

2. **Event Binding with `dispatcher`:**

   - Events (`click` for incrementing and decrementing the counter) are bound to their respective methods (`increment` and `decrement`) using `dispatcher`.
   - The `dispatcher.bind` ensures that each button is linked to the correct instance and method.

3. **Maintaining the `@mutator` Decorator:**

   - The `@mutator` decorator ensures that Zenaura's state management and virtual DOM diffing work seamlessly to update the UI dynamically.

4. **Using Instance Names:**
   - The `instance_name` ensures unique IDs for buttons, enabling multiple instances of the `Counter` component to exist independently.

This updated example aligns with the recommended approach and uses the `tags` system for simplicity and clarity while retaining the core functionality.
