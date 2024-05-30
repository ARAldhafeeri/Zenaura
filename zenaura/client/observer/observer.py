from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Abstract base class for observers that listen to changes in subjects.

    Observers are notified when a subject's state changes, allowing them to react accordingly.
    This pattern promotes loose coupling between subjects and observers, making the system more flexible and maintainable.

    **Key Features:**

    - **Loose Coupling:** Observers are not directly dependent on the subject's implementation, 
      allowing for easier modifications and additions.
    - **Flexibility:** Observers can be easily added or removed without affecting the subject.
    - **Maintainability:** The separation of concerns makes the code easier to understand and maintain.

    **Usage:**

    1. Define concrete observer classes that inherit from `Observer`.
    2. Implement the `update` method in each concrete observer to specify the desired behavior when notified.
    3. Attach the observers to the subject using the subject's `attach` method.
    4. When the subject's state changes, it will call the `update` method of all attached observers.

    **Example:**

    ```python
    class Subject:
        def __init__(self):
            self._observers = []

        def attach(self, observer):
            self._observers.append(observer)

        def notify(self, value):
            for observer in self._observers:
                observer.update(value)

    class ConcreteObserver(Observer):
        def update(self, value):
            print(f"Observer received value: {value}")

    # Create a subject and an observer
    subject = Subject()
    observer = ConcreteObserver()

    # Attach the observer to the subject
    subject.attach(observer)

    # Notify the observer with a value
    subject.notify("Hello, world!")
    ```

    **Additional Notes:**

    - The `update` method can receive any type of data, depending on the subject's implementation.
    - Observers can choose to ignore notifications if they are not interested in the updated value.
    - The subject can manage multiple observers and notify them individually or in groups.
    """

    @abstractmethod
    def update(self, value):
        """
        Update method to be implemented by concrete observers.

        This method is called by the subject when its state changes. The observer can use the provided value
        to perform any necessary actions, such as updating its own state or triggering other events.

        Parameters:
        value (dict): The updated value from the subject.

        Returns:
        None
        """
        pass