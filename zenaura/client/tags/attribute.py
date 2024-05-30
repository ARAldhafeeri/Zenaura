class Attribute:
    """
    Represents a key-value pair used for tagging entities.

    Attributes:
        key (str): The key of the attribute.
        value (str): The value of the attribute.

    Methods:
        to_dict(): Converts the attribute to a dictionary representation.
    """

    def __init__(self, key, value):
        """
        Initializes an Attribute object with the given key and value.

        Args:
            key (str): The key of the attribute.
            value (str): The value of the attribute.
        """
        self.key = key
        self.value = value

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the attribute.

        Returns:
            dict: A dictionary containing the key and value of the attribute.
        """
        return {
            "key": self.key,
            "value": self.value
        }
