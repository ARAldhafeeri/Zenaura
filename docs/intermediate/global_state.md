## Managing Global State with the Observer Pattern

In this guide, we'll implement a global state management system using the Observer pattern. We'll create four counters, and when Counter 1 reaches 5, all counters will reset. This example will demonstrate how to use subjects and observers to manage global state in a Zenaura application.

## Step 1: Define the Observer and Subject

First, we need to import our `Observer` abstract base class and our `Subject` class that will manage the observers. Also we will define some presentational components that helps us build the counters. 

### Observer

importing the `Observer`, `Subject`.
```python
from zenaura.client.observer import Observer, Subject
```
The counter controlled presentational components in `presentational.py`:

```Python
from zenaura.client.tags.builder import Builder
from zenaura.client.tags.node import Node, Attribute

def Paragraph(text, class_name=None):
    builder = Builder('p').with_text(text)
    if class_name:
        builder = builder.with_attribute('class', class_name)
    return builder.build()

def Header1(text):
    return Builder('h1').with_text(text).build()

def Div(class_name, children):
    div = Builder('div').with_attribute('class', class_name).build()
    div.children = children
    return div

def CounterPresntaional(increaseBtn, decreaseBtn, headertext, count) -> Node:

    header = Builder('h1') \
    .with_child(
        headertext
    ).build()

    ctrl = Builder("div") \
        .with_child(
            increaseBtn
        ).with_child(
            decreaseBtn
        ).build()

    return Builder("div") \
        .with_attribute("id", "large-header") \
        .with_child(
            header 
        ).with_child(
            ctrl
    ).build()

def Button(class_name, text, onclick_handler=None, name=None):
    return Builder("button") \
        .with_attributes(
            class_=class_name,
            py_click=onclick_handler,
            name=name
        ) \
        .with_child(
            text
        ).build()

```

## Step 2: Define Concrete Observers

Next, we define concrete observer classes that will react to state changes. Each counter will be an observer.

### CounterObserver

```python
from zenaura.client import Component

class CounterObserver(Component, Observer):
    def __init__(self, subject, counter_name):
        super().__init__()
        self.subject = subject
        self.counter_name = counter_name
        self.subject.attach(self)
        self.state = {self.counter_name: 0}

    def increment(self):
        new_state = self.subject._state
        new_state[self.counter_name] += 1
        if new_state["counter1"] == 5:
            new_state = {k: 0 for k in new_state}  # Reset all counters
        self.subject.set_state(new_state)

    def update(self, value):
        self.state = value
        self.render()

    def render(self):
        return html.div(
            html.h3({}, f"{self.counter_name.capitalize()}: {self.state[self.counter_name]}"),
            html.button({"onclick": self.increment}, "Increment")
        )
```

## Step 3: Create and Attach Counters to the Subject

Now, we'll create the counters and attach them to the subject.

### Main Application

```python
from zenaura.client import html, run_app

# Create the subject
subject = Subject()

# Create counter components
counter1 = CounterObserver(subject, "counter1")
counter2 = CounterObserver(subject, "counter2")
counter3 = CounterObserver(subject, "counter3")
counter4 = CounterObserver(subject, "counter4")

# Define the main app component
class App(Component):
    def render(self):
        return html.div(
            counter1,
            counter2,
            counter3,
            counter4
        )

# Run the app
run_app(App)
```

## Conclusion

By implementing the Observer pattern, we can efficiently manage global state and ensure that all parts of the application react to changes. In this example, we created four counters, and when Counter 1 reaches 5, all counters reset. This approach ensures maintainability, flexibility, and separation of concerns in your Zenaura applications.