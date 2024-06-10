# Zenaura Data Binding Model Guide

Data binding is a powerful technique that allows seamless synchronization between the user interface and the underlying data model. In Zenaura, data binding facilitates automatic updates to the UI when the state changes, enabling a reactive and efficient user experience. This guide will walk you through the fundamentals of data binding in Zenaura components.

## Understanding Data Binding in Components

Data binding in Zenaura involves creating a connection between the component's state and the UI elements, ensuring that changes in the state are reflected in the UI and vice versa. This helps maintain a consistent and interactive user interface.

The way zenaura implement synchronization between the user interface and the underlying data model is through mutations. Mutations are event handlers decorated with mutator. Use mutator over an event handler if and only if we want the component to re-render. The data can still be synced if we set the state within event handler, without re-rendering the component.

### Example of a Simple Data Binding Component

Let's create a simple form component to demonstrate how data binding works in Zenaura.

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator

class SimpleForm(Component):
    def __init__(self):
        super().__init__()
        self.set_state({"inputValue": ""})

    # note here we did not pass re-render
    # we just want to grap the user input value
    async def update_input(self, event):
        new_value = event.target.value
        self.set_state({"inputValue": new_value})

    def render(self):
        input_value = self.get_state()["inputValue"]
        return Builder("div").with_children([
            Builder("input")
                .with_attribute("value", input_value)
                .with_attribute("py-change", f"{self.instance_name}.update_input")
                .build(),
            Builder("p")
                .with_text(f"Current input: {input_value}")
                .build()
        ]).build()
```

### Explanation

1. **Initialization**: The `SimpleForm` component initializes its state with an `inputValue` key, set to an empty string.
2. **Mutator**: The `update_input` method updates the `inputValue` state based on the user's input.
3. **Rendering**: The `render` method constructs the UI using the `Builder` interface. It creates an input field bound to `inputValue` and a paragraph element to display the current input value.

## Two-Way Data Binding

Two-way data binding ensures that changes in the UI update the component's state and that changes in the state update the UI. This is essential for creating interactive forms and inputs.

Make sure to use text, node via builder `.with_text` zenaura will sanitize the data for you, but extra sanitization is never wrong. Zenaura as well will sanitize attributes, same extra sanitization is good. Better to be careful than sorry.

### Example of Two-Way Data Binding

Here's an example of a component demonstrating two-way data binding:

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator

class TwoWayBinding(Component):
    def __init__(self):
        super().__init__()
        self.set_state({"text": "Hello, Zenaura!"})

    @mutator
    async def update_text(self, event):
        new_text = event.target.value
        self.set_state({"text": new_text})

    def render(self):
        text = self.get_state()["text"]
        return Builder("div").with_children([
            Builder("input")
                .with_attribute("value", text)
                .with_attribute("py-change", f"{self.instance_name}.update_text")
                .build(),
            Builder("p")
                .with_text(f"Typed text: {text}")
                .build()
        ]).build()
```

### Explanation

1. **Initialization**: The `TwoWayBinding` component initializes its state with a `text` key.
2. **Mutator**: The `update_text` method updates the `text` state based on the user's input.
3. **Rendering**: The `render` method creates an input field bound to `text` and a paragraph element to display the current text.

## Best Practices for Data Binding

1. **Keep State Consistent**: Ensure that the state accurately reflects the UI and vice versa. This helps maintain a reliable and predictable user experience.
2. **Use Mutators for State Changes**: use `@mutator`-decorated methods to modify the state. This ensures that state changes are tracked and the UI is updated correctly.
3. **Initialize State in the Constructor**: Set initial state values in the `__init__` method to ensure the component starts with a known state.
4. **Use Clear Naming Conventions**: Use descriptive names for state keys and mutator methods to make the code more readable and maintainable.

## Summary

In this guide, we've covered the basics of data binding in Zenaura components. We created examples of components with one-way and two-way data binding and discussed best practices for managing state and data binding. Following these principles will help you build dynamic and interactive UIs with Zenaura.