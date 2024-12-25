# **Zenaura Components: Functional and Class Components**

Zenaura allows you to build modular UIs by combining **functional components** with **class components**. Understanding when to use each and how to structure them effectively is key to building maintainable applications.

**class components** : Are stateful components with business logic in them.
**functional components**: Are stateless ui elements they get their state via props " function arguments "

---

## **Using Functional Components Within Class Components**

Class components are ideal for managing state and complex logic, while functional components are best for reusable and presentational UI. You can use functional components inside class components to keep your code modular and clean.

### Example:

```python
from zenaura.client.component import Component
from zenaura.ui import div, h1, img

# Functional Component
def Header(title):
    return h1(title, class_="header")

# Class Component
class ZenauraStarter(Component):
    def render(self):
        return div(
            div(
                img(src="./public/logo.png", width=255, height=255, alt="starterLogo"),
                Header("The Python Framework For"),
                Header("Building Modern Web User Interfaces"),
            ),
            class_="zenaura"
        )
```

### Why Use Functional Components in Class Components?

1. **Separation of Concerns**  
   Functional components handle UI presentation, leaving logic to the class component.

2. **Reusability**  
   Functional components can be reused across multiple class components.

3. **Simplified Code**  
   Breaking down large class components into smaller functional components makes your code easier to read and maintain.

---

## **Reusable Components vs. Non-Reusable Components**

### **Non-Reusable Class Components**
By default, Zenaura class components are **limited** and cannot be reused unless explicitly marked as reusable. These components are tied to specific instances and use cases.

#### Example:
```python
from zenaura.client.component import Component

class LimitedComponent(Component):
    def render(self):
        return div("This is a limited component", class_="limited")
```

**Usage:**
```python
limited1 = LimitedComponent()
limited2 = LimitedComponent()  # Error: Non-reusable components cannot be instantiated multiple times
```

### **Reusable Class Components**
Marking a class component as reusable allows it to be instantiated multiple times within the same project. Use the `@Reuseable` decorator to enable this.

#### Example:
```python
from zenaura.client.component import Component, Reuseable

@Reuseable
class ReusableComponent(Component):
    def render(self):
        return div("This is a reusable component", class_="reusable")
```

**Usage:**
```python
reusable1 = ReusableComponent()  # No error
reusable2 = ReusableComponent()  # No error
```

---

### **When to Use Non-Reusable Components**
- For components tightly coupled to specific logic or state.
- For one-off components not meant to be instantiated multiple times.

### **When to Use Reusable Components**
- For UI elements used across different parts of the application (e.g., buttons, cards, modals).
- When you need consistency across instances with shared logic but independent states.

---

## **Combining Functional and Reusable Components**

You can nest reusable and functional components inside a class component to create highly modular and flexible UIs.

#### Example:
```python
from zenaura.client.component import Component, Reuseable
from zenaura.ui import div, h1

# Functional Component
def Card(content):
    return div(content, class_="card")

# Reusable Class Component
@Reuseable
class ReusableCardList(Component):
    def render(self):
        return div(
            Card("Card 1 Content"),
            Card("Card 2 Content"),
            class_="card-list"
        )
```

---

## **Best Practices**

1. **Functional Inside Class**: Use functional components within class components for reusable, presentation-focused UI.
2. **Reusable Components**: Mark components as reusable when they need to be instantiated multiple times.
3. **Non-Reusable Components**: Use non-reusable components for one-off, tightly scoped logic.
4. **Modularity**: Break large components into smaller functional components for better maintainability.

By understanding the distinction between reusable and non-reusable components and leveraging functional components effectively, you can build scalable, maintainable, and efficient Zenaura applications. 🚀