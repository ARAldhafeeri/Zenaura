class Attribute:
    def __init__(self, key, value):
        """
        Initializes an Attribute object with the given key and value.

        Args:
        key: The key of the attribute.
        value: The value of the attribute.
        """
        self.key = key
        self.value = value

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value
        }