from zenaura.client.tags import Attribute
from .sanitize import CompilerSanitizer
from typing import List 
import io 

sanitizer = CompilerSanitizer()
class AttributeProccessor(

):
    def process_attributes(
                self, 
                attrs: List[Attribute]
                ) -> str:
        """
            Processes a list of Attributes, converting them to
            HTML-formatted attributes.

            Args:
                attrs (List[Attribute]): A list of Zenui Attribute objects.
                attributes like onclick.

            Returns:
                str: A string containing the HTML-formatted attributes,
                 ready to be included in a tag.
        """

        s = io.StringIO()  # Create a string buffer for building the output

        for i, attr in enumerate(attrs):
            attrKey = attr.key
            attrValue = attr.value
            if attrKey in self.attrKeyWords.keys():
                attrKey = self.attrKeyWords[attrKey]  # Apply keyword mapping

            # Add space only if it's not the first or last attribute
            if i == 0 or i == len(attrs) - 1:
                s.write(f' {attrKey}="{sanitizer.sanitize(attrValue)}"')
            else:
                s.write(f'{attrKey}="{sanitizer.sanitize(attrValue)}" ')

        res = s.getvalue()
        s.close()
        return res