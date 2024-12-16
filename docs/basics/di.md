# Simple Guide to Dependency Injection in Zenaura

Dependency injection (DI) allows you to inject external dependencies into your components, making your code more modular and easier to test.

## Why Use Dependency Injection?

- **Decoupling**: Makes your components independent of the specific implementations of their dependencies.
- **Testability**: Easier to mock dependencies during testing.
- **Flexibility**: Easily swap out dependencies without changing your component code.

## Basic Steps for Dependency Injection

### Step 1: Define Your Dependencies

First, create the dependencies that your components will need. These could be services, configurations, or any other objects.

```python
class ApiService:
    def fetch_data(self):
        return "data from API"

class Logger:
    def log(self, message):
        print(f"LOG: {message}")

# Create instances of your dependencies
dependencies = {
    "api_service": ApiService(),
    "logger": Logger()
}
```

### Inject Dependencies into Components

When creating a component, pass the dependencies to the component's constructor.

```python
from zenaura.client.component import Component

class MyComponent(Component):
    def __init__(self, di):
        super().__init__()
        self.api_service = di["api_service"]
        self.logger = di["logger"]

    def render(self):
        return Builder("div").with_text("My Component").build()

# Instantiate the component with dependencies
my_component = MyComponent(dependencies)
```

### Use Dependencies in Component Methods

Utilize the injected dependencies in your component's methods as needed.

```python
class DataFetcherComponent(Component):
    def __init__(self, di):
        super().__init__()
        self.api_service = di["api_service"]
        self.logger = di["logger"]

    async def fetch_and_log_data(self):
        data = self.api_service.fetch_data()
        self.logger.log(f"Data: {data}")

    def render(self):
        return Builder("div").with_text("Data Fetcher Component").build()

# Instantiate the component with dependencies
data_fetcher_component = DataFetcherComponent(dependencies)
```

### Step 4: Injecting Dependencies into Nested Components

If you have nested components, pass the dependencies down to the child components.

```python
class ParentComponent(Component):
    def __init__(self, di):
        super().__init__()
        self.di = di

    def render(self):
        child_component = ChildComponent(self.di)
        return Builder("div").with_child(child_component.render()).build()

def ChildComponent(dependency):
    self.logger.log("Child component rendered")
    return Builder("div").with_text("Child Component").build()

# Instantiate the parent component with dependencies
dependencies = ["1", "2"]
parent_component = ParentComponent(dependencies)
```
