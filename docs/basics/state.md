# Zenaura Component State Management

State management is a crucial aspect of building dynamic and interactive user interfaces. In Zenaura, components can maintain and update their state to reflect changes in the application. This guide will walk you through the basics of managing state within Zenaura components.

## Understanding State in Components

State in Zenaura components refers to the data that changes over time and drives the UI. Each stateful component can hold its own state, which can be updated in response to user interactions or other events.

### Example of a Simple Stateful Component

Let's create a simple counter component to illustrate how state works in Zenaura.

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator

class Counter(Component):
    def __init__(self):
        super().__init__()
        self.set_state({"count": 0})

    @mutator
    async def increment(self, event):
        current_count = self.get_state()["count"]
        self.set_state({"count": current_count + 1})

    @mutator
    async def decrement(self, event):
        current_count = self.get_state()["count"]
        self.set_state({"count": current_count - 1})

    def render(self):
        count = self.get_state()["count"]
        return Builder("div").with_children([
            Builder("h1").with_text(f"Count: {count}").build(),
            Builder("button").with_text("+").with_attribute("py-click", f"{self.instance_name}.increment").build(),
            Builder("button").with_text("-").with_attribute("py-click", f"{self.instance_name}.decrement").build()
        ]).build()
```

### Explanation

1. **Initialization**: The `Counter` component initializes its state with a `count` value of `0` in the `__init__` method.
2. **Mutators**: The `increment` and `decrement` methods are marked with the `@mutator` decorator, indicating that they can modify the component's state, mutate the component and trigger a zenaura dom re-render. These methods update the `count` value based on user interactions.
3. **Rendering**: The `render` method constructs the UI using the `Builder` interface. It creates an `h1` element to display the count and two buttons to increment and decrement the count.

Note when a user click on increment or decrement button the data follow will be as follow:
1. Pydide will call increment function.
2. increment function will run the code mutate the state.
3. mutator funciton will call the zenaura virtual dom to kick starts the diffing algorithm and patch update the real dom.
4. user see count increased by 1.

## Handling State Changes

State changes in Zenaura components are handled by mutator methods. These methods are asynchronous and use the `@mutator` decorator to indicate that they will modify the component's state.

The reason they are asynchronous because zenaura dom patch updates the real dom in non-blocking high performant way using scheduling and tasks, expressed as optimized dom minipulations patch updates.

### Example of a Stateful Component with Multiple States

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
        new_name = event.target.value  # Assume this value comes from an input field
        self.set_state({"name": new_name})

    @mutator
    async def increment_age(self, event):
        current_age = self.get_state()["age"]
        self.set_state({"age": current_age + 1})

    def render(self):
        state = self.get_state()
        return Builder("div").with_children([
            Builder("h1").with_text(f"Name: {state['name']}").build(),
            Builder("input").with_attribute("value", state['name']).with_attribute("py-change", f"{self.instance_name}.update_name").build(),
            Builder("h2").with_text(f"Age: {state['age']}").build(),
            Builder("button").with_text("Increase Age").with_attribute("py-click", f"{self.instance_name}.increment_age").build()
        ]).build()
```

### Explanation

1. **Initialization**: The `UserProfile` component initializes its state with `name` and `age`.
2. **Mutators**: The `update_name` method updates the `name` state based on user input, while the `increment_age` method increments the `age` state.
3. **Rendering**: The `render` method creates a UI that includes an `h1` element for the name, an input field for updating the name, an `h2` element for the age, and a button to increment the age.

## Best Practices for State Management

1. **Keep State Localized**: Manage state within the component that needs it. If multiple components need the same state, consider lifting the state up using a subject which is an intermediate concept we will cover in Beyond the basics guide. 
2. **Use Mutators for State Changes**: Always use `@mutator`-decorated methods to modify the state. This ensures that state changes are tracked and the UI is updated correctly.
3. **Initialize State in the Constructor**: Set initial state values in the `__init__` method to ensure the component starts with a known state.
4. for event handlers use py-* for py-script , for example if you are using JS function you will pass onclick="jsfunction", but for python we need the instance name, then py-<eventhandlername> e.g.: py-click, py-change, py-hover. 

## Summary

In this guide, we've covered the basics of managing state in Zenaura components. We created examples of stateful components and discussed how to handle state changes using mutators. Following these principles will help you build dynamic and interactive UIs with Zenaura.
