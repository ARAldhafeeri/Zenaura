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

class Counter(Component):
    def __init__(self):
        super().__init__()
        self.set_state({"count": 0})

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
            Builder("button").with_text("+").with_attribute("py-click", f"{self.instance_name}.increment").build(),
            Builder("button").with_text("-").with_attribute("py-click", f"{self.instance_name}.decrement").build()
        ]).build()

counter = Counter()
```

### Explanation

1. **User Event**: When the user clicks the "+" or "-" button, a `click` event is triggered.
2. **Mutate State**: The event handler (`increment` or `decrement` method) is called. These methods are decorated with `@mutator`, indicating that they will change the component's state.
3. **Re-render Component**: After the state is updated, Zenaura automatically triggers a re-render of the component. The `render` method is called again with the updated state.
4. **Render Component on the Browser**: Zenaura performs a virtual DOM diff between the previous and new states. Only the changed parts of the DOM are updated in the browser, ensuring efficient rendering.

## Detailed Steps

### 1. User Event

User events are linked to component methods using the `py-click`, `py-change`, and other attributes in the `Builder` interface. For example:

```python
Builder("button").with_text("+").with_attribute("py-click", f"{self.instance_name}.increment").build()
```

The `py-click` attribute specifies that the `increment` method of the component instance should be called when the button is clicked.

### 2. Mutate State

Mutator methods are defined with the `@mutator` decorator. These methods update the component's state and ensure that the changes are tracked:

```python
@mutator
async def increment(self, event):
    self.set_state({"count": self.get_state()["count"] + 1})
```

The `set_state` method updates the state and triggers a re-render.

### 3. Re-render Component

When the state is updated, Zenaura automatically calls the `render` method of the component to generate the new virtual DOM:

```python
def render(self):
    count = self.get_state()["count"]
    return Builder("div").with_children([
        Builder("h1").with_text(f"Count: {count}").build(),
        Builder("button").with_text("+").with_attribute("py-click", f"{self.instance_name}.increment").build(),
        Builder("button").with_text("-").with_attribute("py-click", f"{self.instance_name}.decrement").build()
    ]).build()
```

### 4. Render Component on the Browser

Zenaura compares the previous virtual DOM with the new virtual DOM and applies only the differences to the actual DOM. This diffing algorithm ensures efficient updates and minimizes reflows and repaints in the browser.

## Best Practices

1. **Use Mutators for State Changes**: Always use `@mutator`-decorated methods to handle state changes. This ensures the state changes are tracked and the component is re-rendered correctly.
2. **Keep Event Handlers Simple**: Event handlers should focus on updating the state. Avoid complex logic in event handlers; instead, delegate it to other methods or services.
3. **Optimize Rendering**: Ensure that your `render` method is efficient. Avoid unnecessary computations or side effects in the `render` method.

## Summary

In this guide, we've covered how Zenaura handles user events and updates the component state. The sequence of user events leading to state mutations, virtual DOM diffing, and efficient rendering ensures that Zenaura applications are both interactive and performant. By following these principles, you can build dynamic and responsive user interfaces with Zenaura.
