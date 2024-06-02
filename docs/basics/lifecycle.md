# Zenaura Lifecycle Guide

In Zenaura, lifecycle methods allow you to hook into various stages of a component's life in the zenaura virtual DOM. This guide will introduce the key lifecycle methods and how to use them effectively.

## Overview

Zenaura provides two main lifecycle classes:
1. **MountLifeCycles**: Handles actions when a component is first mounted to the DOM.
2. **RenderLifeCycle**: Manages actions before and after a component is updated and re-rendered in the DOM.

### Key Lifecycle Methods

- **attached**: Called after a component is mounted to the DOM.
- **on_mutation**: Called before a component is updated in the DOM.
- **on_settled**: Called after a component is updated and re-rendered in the DOM.

## MountLifeCycles

The `MountLifeCycles` class provides the `attached` method, which is invoked after a component is mounted to the DOM. This is useful for initializing state, setting up event listeners, making API calls, or performing animations.

### Usage

```python
from zenaura.client.component import Component
from zenaura.client.mutator import mutator

class MyComponent(Component):
    
    @mutator
    async def attached(self):
        # Initialize state
        self.state = {"count": 0}
        # Set up event listeners
        self.setup_event_listeners()
        # Make an API call
        await self.fetch_data()
        # Perform an animation
        self.perform_animation()
    
    def setup_event_listeners(self):
        pass
    
    async def fetch_data(self):
        pass
    
    def perform_animation(self):
        pass

    @

    def render(self):
        return Builder("div").with_text("Hello, World!").build()
```

### Explanation

1. **Initialization**: State initialization and other setup actions are performed in the `attached` method.
2. **Event Listeners and API Calls**: Set up event listeners and make any necessary API calls.
3. **Rendering**: Define the component's render method to return the desired HTML structure.
4. **mutator**: attached must be decorated with mutator , so once we trigger the ui or state mutation the component re-renders.

## RenderLifeCycle

The `RenderLifeCycle` class provides two methods: `on_mutation` and `on_settled`. These methods are invoked before and after a component is updated and re-rendered in the DOM.

### on_mutation

The `on_mutation` method is called before the component is updated. This is useful for updating state based on new props, setting up event listeners, making API calls, or performing animations.

### Usage

```python
from zenaura.client.component import Component

class MyComponent(Component):
    async def on_mutation(self):
        # Update state based on new props
        self.state["updated"] = True
        # Set up event listeners
        self.setup_event_listeners()
        # Make an API call
        await self.fetch_data()
        # Perform an animation
        self.perform_animation()
    
    def setup_event_listeners(self):
        pass
    
    async def fetch_data(self):
        pass
    
    def perform_animation(self):
        pass

    def render(self):
        return Builder("div").with_text("Hello, World!").build()
```

### Explanation
 Important note: Unlike mount lifecycle methods, render lifecycle methods should not be decorated with mutator decorator, they are already within the lifecycle of render, passing mutator will result in a recurision cycle. Render lifecycle methods are called when the component is rendering.

1. **Update State and Setup**: Perform necessary actions before the component is updated, such as updating state and setting up event listeners.

## on_settled

The `on_settled` method is called after the component is updated and re-rendered. This is useful for focusing on an input element, scrolling to a specific position, or triggering custom events.

### Usage

```python
from zenaura.client.component import Component

class MyComponent(Component):
    async def on_settled(self):
        # Focus on an input element
        self.focus_input()
        # Scroll to a specific position
        self.scroll_to_position()
        # Trigger custom events
        self.trigger_custom_event()
    
    def focus_input(self):
        pass
    
    def scroll_to_position(self):
        pass
    
    def trigger_custom_event(self):
        pass

    def render(self):
        return Builder("div").with_text("Hello, World!").build()
```

### Explanation

1. **Post-Update Actions**: Perform actions such as focusing on elements, scrolling, or triggering custom events after the component is re-rendered.

## Example: Complete Component Lifecycle

Here’s an example that integrates all lifecycle methods in a single component:

```python
from zenaura.client.component import Component
from zenaura.client.tags.builder import Builder
from zenaura.client.mutator import mutator

class FullLifecycleComponent(Component):
    @mutator
    async def attached(self):
        self.state = {"initialized": True}
        print("Component mounted and initialized.")
    
    async def on_mutation(self):
        self.state["updated"] = True
        print("Component state updated before rendering.")
    
    async def on_settled(self):
        print("Component re-rendered and settled.")
    
    def render(self):
        return Builder("div").with_text("Lifecycle Component").build()

# Create and mount the component
component = FullLifecycleComponent()
component.attached()
component.on_mutation()
component.on_settled()
```

### Explanation

1. **Mounting**: The `attached` method initializes the state when the component is mounted. We need mutator because we want to re-render the component, let zenaura virtual DOM diff, and update the real dom affected parts with the changes from attached method.
2. **Updating**: The `on_mutation` method updates the state before re-rendering.
3. **Settling**: The `on_settled` method logs a message after the component is re-rendered.

## Summary

Lifecycle methods in Zenaura provide hooks to perform actions at different stages of a component’s life. The `MountLifeCycles` and `RenderLifeCycle` classes offer methods to initialize state, set up event listeners, make API calls, perform animations, and more. By leveraging these lifecycle methods, you can create dynamic and interactive components with ease.
