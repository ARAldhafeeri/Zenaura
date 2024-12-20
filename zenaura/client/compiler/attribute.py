from zenaura.client.tags import Attribute
from .sanitize import CompilerSanitizer
from typing import List 
import io 

sanitizer = CompilerSanitizer()

class AttributeProccessor():
    """
        Processes a list of `Attribute` objects and converts them into HTML-formatted attributes.

        Attributes:
            attrKeyWords (dict): Maps Python keywords to HTML attribute names.
                - "styles": Translates to "class".
                - "class_": Translates to "class" (avoids conflict with Python's `class` keyword).
                - "for_": Translates to "for".
                - "name_": Translates to "name".
                - "type_": Translates to "type".

            attrValueWords (dict): Maps Python boolean values to HTML-compliant strings.
                - "True": Translates to "true".
                - "False": Translates to "false".

        Methods:
            None
    """
    def __init__(self):
        self.attrKeyWords = {
            "styles": "class",
            "class_": "class",
            "for_": "for",
            "name_": "name",
            "type_": "type"
        }
        self.attrValueWords = {
            "True": "true",
            "False": "false"
        }
    def process_attributes(
                self, 
                attrs: List[Attribute]
                ) -> str:
        """
        Processes a list of `Attribute` objects, converting them to HTML-formatted attributes.

        Args:
            attrs (List[Attribute]): A list of `Attribute` objects representing the attributes to be processed.

        Returns:
            str: A string containing the HTML-formatted attributes, ready to be included in a tag.

        Raises:
            TypeError: If the input `attrs` is not a list.
            ValueError: If any element in `attrs` is not an `Attribute` object.
        """

        if not isinstance(attrs, list):
            raise TypeError("`attrs` must be a list of Attribute objects.")

        for attr in attrs:
            if not isinstance(attr, Attribute):
                raise ValueError("Each element in `attrs` must be an Attribute object.")

        s = io.StringIO()  # Create a string buffer for building the output

        for i, attr in enumerate(attrs):
            attrKey = attr.key
            attrValue = attr.value
            if attrKey in self.attrKeyWords.keys():
                attrKey = self.attrKeyWords[attrKey]  # Apply keyword mapping
            if str(attrValue) in self.attrValueWords.keys():
                attrValue = self.attrValueWords[str(attrValue)]

            # Add space only if it's not the first or last attribute
            if i == 0 or i == len(attrs) - 1:
                s.write(f' {attrKey}="{sanitizer.sanitize(attrValue)}"')
            else:
                s.write(f'{attrKey}="{sanitizer.sanitize(attrValue)}" ')

        res = s.getvalue()
        s.close()
        return res
