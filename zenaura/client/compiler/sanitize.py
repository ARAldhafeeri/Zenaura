import html
import bleach

from zenaura.client.config import (
    allowed_tags,
    allowed_attributes,
)

class CompilerSanitizer:
    def sanitize(
                self, 
                user_input, 
                allowed_tags=allowed_tags, 
                allowed_attributes=allowed_attributes
            ):
        """
        Sanitizes user input to prevent various injection attacks.

        Args:
            user_input (str): The raw user input to sanitize.
            allowed_tags (list): A list of allowed HTML tags (e.g., ['p', 'br', 'strong']).
            allowed_attributes (dict): A dictionary mapping allowed tags to their allowed 
                                    attributes (e.g., {'img': ['src', 'alt']}).  

        Returns:
            str: The sanitized input.
        """
        user_input = str(user_input)
        
        safe_html = html.escape(user_input)  # Escape all HTML special characters initially
        safe_html = bleach.clean(
            safe_html, tags=allowed_tags, attributes=allowed_attributes
            ) 
      

        return safe_html 