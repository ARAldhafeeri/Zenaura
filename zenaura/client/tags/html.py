from abc import ABC, abstractmethod

class HTMLElement(ABC):
    """
    Abstract class for HTMLElement.
    """
    @abstractmethod
    def appendChild(self, child: "HTMLElement") -> None:
        """
        Appends a child element to the parent element.
        """
        pass

    @abstractmethod
    def removeChild(self, child: "HTMLElement") -> None:
        """
        Removes a child element from the parent element.
        """
        pass
