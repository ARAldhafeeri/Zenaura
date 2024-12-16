# Zenaura Components

Zenaura components allow Python developers to create the building blocks for their applications. These components are categorized into three types:

1. **Stateful Limited Class Components (limited, not reusable)**
2. **Stateful Reusable Class Components (reusable)**
3. **Stateless Presentational Functional Components**

## Understanding the Node Data Structure

The `Node` data structure is the fundamental building block in the Zenaura library. It enables the virtual DOM to compare the previous and current state of a component, diff the changes, and update the real DOM efficiently. Every component must return a `Node` data structure via the `render` method in class components or via a return statement in functional components.

Here's an example of creating a `Node`:

```python
from zenaura.client.tags import Node, Attribute

node = Node(
    "div",
    children=[
        Node(
            'h1',
            children=[
                Node(text='hello')
            ]
        )
    ],
    attributes=[
        Attribute("class", "test")
    ]
)
```

This will render the following HTML:

```html
<div class="test">
  <h1>hello</h1>
</div>
```

While the `Node` data structure is powerful, it can be cumbersome for building UI components, which is where the Builder Interface comes in.

## The Builder Interface

The Builder Interface abstracts away the complexities of the `Node` data structure, allowing developers to write more maintainable, readable, and declarative UI building blocks.

Example using the Builder Interface:

```python
from zenaura.client.tags.builder import Builder

h1 = Builder('h1').with_text("test").build()
div = Builder("div").with_child(h1).with_attribute("class", "test").build()
```

This will render the following HTML:

```html
<div class="test">
  <h1>test</h1>
</div>
```

The Builder Interface enhances readability and maintainability. To further simplify, you can use functional components.

## Stateless Presentational Functional Components

Stateless presentational components allow you to break down large stateful components into smaller, reusable pieces. They are simple Python functions that return a `Node` data structure.

Example:

```python
from zenaura.client.tags.builder import Builder

def Div(class_name, children):
    div = Builder('div').with_attribute('class', class_name).build()
    div.children = children
    return div

def Header1(text):
    return Builder('h1').with_text(text).build()

div = Div('test', [Header1('test')])
```

This will render the following HTML:

```html
<div class="test">
  <h1>test</h1>
</div>
```

Using the Builder Interface with functional components helps in building robust and reusable components for any Zenaura project.

## Stateful Limited Class Components (Limited, Not Reusable)

These are the default class components in the Zenaura library. They can maintain state and wrap functional components to create fully-featured UIs. However, they are limited and cannot be reused within the same project unless specified with the `@Reusable` decorator.

Example:

```python
from zenaura.client.component import Component
from public.presentational import *

class ZenauraStarter(Component):
    def __init__(self, di):
        super().__init__()
        self.di = di
        self.state = None

    def render(self):
        return Div("zenaura", [
           Div("", [
            Image("./public/logo.png", "zenaura", "255", "255", "starterLogo"),
            Header1("The Python Library For, Hello world!"),
            Header1("Building Modern Web User Interfaces")
           ])
        ])

zen = ZenauraStarter()  # No error
zen2 = ZenauraStarter()  # Error: Zenaura components are limited by design
```

## Stateful Reusable Class Components (Reusable)

These components are designed to be reusable across your codebase. They manage their state independently and can be used multiple times within the same project.

Example:

```python
from zenaura.client.component import Component, Reuseable
from public.presentational import *

@Reuseable
class ZenauraStarter(Component):
    def render(self):
        return Div("zenaura", [
           Div("", [
            Image("./public/logo.png", "zenaura", "255", "255", "starterLogo"),
            Header1("The Python Library For, Hello world!"),
            Header1("Building Modern Web User Interfaces")
           ])
        ])

zen = ZenauraStarter()  # No error
zen2 = ZenauraStarter()  # No error
```

## Nesting Component Logic

In the Zenaura library, there is a specific nesting order that must be followed:

- **Pages**
  - **Class Components**
    - **Functional Components**
- **Layout** : Layout is advanced topic which we will discuss later in the documentation, it allows you to add global components that appear on every page like navbar, modals, footers and so on.

This order ensures predictable and debuggable source code. Pages render the components as a stack from index 0 to n in the browser. Nested stateful class components can be confusing, so maintain the hierarchy to avoid errors.

## Summary

In this guide, we've covered the different types of components in Zenaura and how to use the Node data structure and Builder Interface to create maintainable and reusable UI components. Following these principles will help you build scalable and efficient applications with Zenaura.

In the next guide, we'll dive deep into dependency injection and component state management.
