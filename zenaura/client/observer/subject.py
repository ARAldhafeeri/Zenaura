class Subject:
    """
    Create subjects for components to communicate on.

    A subject is an entity that maintains a state and notifies its observers when the state changes.
    Observers can be any object that implements the `Observer` interface.

    **Key Features:**

    - **State Management:** Subjects maintain their own state and provide access to it through the `state` property.
    - **Observer Management:** Subjects manage a list of attached observers and notify them when the state changes.
    - **Loose Coupling:** Subjects are not directly dependent on the implementation of their observers, 
      promoting flexibility and maintainability.

    **Usage:**

    1. Create a subject instance.
    2. Attach observers to the subject using the `attach` method.
    3. Modify the subject's state using the `state` property.
    4. The subject will automatically notify all attached observers when the state changes.

    **Example:**

    ```python
    class ConcreteSubject(Subject):
        def __init__(self, initial_state):
            super().__init__()
            self._state = initial_state

        def do_something(self):
            # Modify the subject's state
            self.state = {"key": "value"}

    # Create a subject and an observer
    subject = ConcreteSubject({"initial": "value"})
    observer = Observer()

    # Attach the observer to the subject
    subject.attach(observer)

    # Modify the subject's state
    subject.do_something()
    ```

    **Additional Notes:**

    - The `state` property can be any type of data, depending on the subject's implementation.
    - Observers can choose to ignore notifications if they are not interested in the updated state.
    - The subject can manage multiple observers and notify them individually or in groups.
    """

    def __init__(self):
        """
        Initialize a new Subject.

        Parameters:
        None

        Returns:
        None
        """
        self._observers = set()
        self._state = {}

    def attach(self, observer):
        """
        Attach an observer to the subject.

        Parameters:
        observer (Observer): The observer to attach.

        Returns:
        None
        """
        self._observers.add(observer)

    def detach(self, observer):
        """
        Detach an observer from the subject.

        Parameters:
        observer (Observer): The observer to detach.

        Returns:
        None
        """
        self._observers.discard(observer)

    def notify(self):
        """
        Notify all attached observers.

        Parameters:
        None

        Returns:
        None
        """
        for observer in self._observers:
            observer.update(self._state)

    @property
    def state(self):
        """
        Get the state of the subject.

        Parameters:
        None

        Returns:
        dict: The state of the subject.
        """
        return self._state

    @state.setter
    def state(self, new_value):
        """
        Set the state of the subject and notify observers.

        Parameters:
        new_value (dict): The new state of the subject.

        Returns:
        None
        """
        self._state = new_value
        self.notify()
