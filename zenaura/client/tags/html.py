from abc import ABC, abstractmethod

class HTMLElement(ABC):
    """
    Abstract base class representing an HTML element.

    This class defines the common interface for all HTML elements,
    providing methods for manipulating child elements.

    Attributes:
        None

    Methods:
        appendChild(child: HTMLElement) -> None:
            Appends a child element to the current element.
        removeChild(child: HTMLElement) -> None:
            Removes a child element from the current element.
    """

    @abstractmethod
    def appendChild(self, child: "HTMLElement") -> None:
        """
        Appends a child element to the current element.

        Args:
            child: The child element to be appended.

        Raises:
            TypeError: If the provided child is not an instance of `HTMLElement`.
        """
        pass

    @abstractmethod
    def removeChild(self, child: "HTMLElement") -> None:
        """
        Removes a child element from the current element.

        Args:
            child: The child element to be removed.

        Raises:
            TypeError: If the provided child is not an instance of `HTMLElement`.
            ValueError: If the provided child is not a child of the current element.
        """
        pass
