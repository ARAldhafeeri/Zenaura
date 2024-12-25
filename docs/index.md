# Welcome to Zenaura Docs

Zenaura is a cutting-edge Python library that empowers developers to build high-performance, stateful Single Page Applications (SPAs) with ease. Built on Pydide and PyScript, Zenaura leverages a virtual DOM to optimize responsiveness and interactivity in web UIs.

---

## **Introduction**

### Brief Intro to Core Concepts

Zenaura simplifies modern web development by:

- Combining Python with a virtual DOM for dynamic updates.
- Allowing seamless integration of stateful SPAs.
- Providing an intuitive API for effortless development.

---

## **Architecture**

Zenaura’s architecture revolves around:

- **Components**: Modular, reusable building blocks.
- **Pages**: Collections of components forming the UI.
- **Router**: Handles SPA navigation without page reloads.
- **State Management**: Simplifies handling dynamic data.
- **Virtual DOM**: Ensures efficient UI rendering.
- **Global States**: Manage state between different components.
- **Dispatcher**: Link event listeners from document, window or html tag by id to a handler.

---

## **Why Zenaura?**

1. **Pythonic Development**: Use Python to build web apps less congitive load, write everything in Python.
2. **High Performance**: Optimized rendering with a virtual DOM.
3. **Stateful SPAs**: Create seamless, dynamic user experiences.
4. **Simplicity and Flexibility**: Easy-to-learn API for projects of any size.
5. **Ecosystem Integration**: Integrate powerful Python ecosystem with Javascript ecosystem.
6. **Active Development**: Regular updates and community support.

---

## **Guidelines**

### **Best Practices for Zenaura Development**

1. **Prioritize Modular and Reusable Components**

   - Keep components flat and avoid excessive nesting.
   - Refactor nested HTML tags into presentational functional components and pass required props from parent components.

2. **Global State Management**

   - Use **Subjects** and **Observers** to efficiently manage global state across the application.

3. **Optimize Redundant UI Elements**

   - Leverage functional components for repeatable or static UI elements to simplify the codebase.

4. **Single Layout for Global Components**

   - Centralize global components within a single layout, avoiding duplication across multiple pages.

5. **Separate Business Logic from UI**

   - Isolate business logic by using **dispatcher**, keeping UI components focused solely on rendering.

6. **Maintain a Clear Project Structure**

   - Organize your application as follows:  
     **Routes → Layout → Pages → Class Components → Functional Components**

7. **Implement Dependency Injection**
   - Use dependency injection to design reusable and flexible components.

---

## **Rules**

- Use `@mutator` and `@mutates` appropriately for async and regular callbacks to rerender the component once the handler is invoked via event listner.
- Bind events using the `dispatcher.bind` for clean, event-driven code.
- dispatch events using `dispatcher.dispatch`
- Follow Zenaura’s recommended project structure for clarity and maintainability.
- Utilize the virtual DOM efficiently to avoid unnecessary rendering.
- Don't include many files in config.json, just include **init**.py and import everything you need to use there.

---

## **Next Steps**

- **Quick Start**: Create your first application in minutes.
- **Fundamentals**: Master Zenaura's building blocks like components, pages, and state.
- **Beyond the Basics**: Explore advanced topics like event handling and server-side rendering.
- **Examples**: Learn by building projects ranging from simple UIs to admin dashboards.
- **API Reference**: Dive into the comprehensive documentation for detailed insights.

Welcome to Zenaura—where Python meets the web. Let’s build something amazing together! 🚀
