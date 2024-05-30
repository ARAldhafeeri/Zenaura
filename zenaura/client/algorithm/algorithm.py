from .searcher import Searcher
from .updater import Updater

class DiffingAlgorithm(
    Searcher,
    Updater
):
    """
        The diffing algorithm in Zenaura virtual DOM.

        This class is responsible for comparing the old and new virtual DOM trees and generating a list of changes that need to be applied to the real DOM.

        The diffing algorithm is implemented in two steps:

        1. **Search:** The `Searcher` class traverses the old and new virtual DOM trees and identifies the nodes that have changed.
        2. **Update:** The `Updater` class applies the changes to the real DOM.

        The diffing algorithm is designed to be efficient and performant. It uses a number of techniques to minimize the number of changes that need to be applied to the real DOM.

        **Attributes:**

        * `Searcher`: An instance of the `Searcher` class.
        * `Updater`: An instance of the `Updater` class.

        **Methods:**

        * `diff(old_tree, new_tree)`: Compares the old and new virtual DOM trees and generates a list of changes that need to be applied to the real DOM.

        **Example:**

        ```python
        # Create an instance of the DiffingAlgorithm class.
        diffing_algorithm = DiffingAlgorithm()

        # Compare the old and new virtual DOM trees.
        changes = diffing_algorithm.diff(old_tree, new_tree)

        # Apply the changes to the real DOM.
        diffing_algorithm.update(changes)
        ```
    """