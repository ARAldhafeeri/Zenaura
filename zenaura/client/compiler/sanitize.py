import html
import bleach

from zenaura.client.config import (
    allowed_tags,
    allowed_attributes,
)

class CompilerSanitizer:
    """
    This class provides methods for sanitizing user input to prevent various injection attacks.

    It uses the `bleach` library to remove potentially harmful HTML tags and attributes, 
    and the `html` library to escape special characters.

    Attributes:
        None
    """

    def sanitize(
        self, 
        user_input: str, 
    ) -> str:
        """
        Sanitizes user input to prevent various injection attacks.

        This method takes the raw user input as a string and returns a sanitized version of the input.

        Args:
            user_input (str): The raw user input to sanitize.
            allowed_tags (list, optional): A list of allowed HTML tags (e.g., ['p', 'br', 'strong']). 
                Defaults to `allowed_tags` from the `zenaura.client.config` module.
            allowed_attributes (dict, optional): A dictionary mapping allowed tags to their allowed 
                attributes (e.g., {'img': ['src', 'alt']}). Defaults to `allowed_attributes` from the 
                `zenaura.client.config` module.

        Returns:
            str: The sanitized input.
        """
        user_input = str(user_input)
        # Use bleach to remove potentially harmful HTML tags and attributes
        safe_html = bleach.clean(
            user_input, tags=allowed_tags, attributes=allowed_attributes
        )

        return safe_html