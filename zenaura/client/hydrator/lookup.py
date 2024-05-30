from collections import defaultdict

class VDomLookupTable:
    """
        VDomLookupTable:

        This class manages two lookup tables:

        1. **zen_dom_table**:
            - Optimizes general tree structure by storing each component's unique ID and its children with the `ZENAURA_DOM_ATTRIBUTE`.
            - Provides efficient operations:
                - Searching for mounted component's previous state: O(1)
                - Deleting unmounted components: O(1)
                - Inserting mounted components: O(1)
            - Applies the same time complexity to tree structure operations:
                - Search: O(n)
                - Insert: O(n)
                - Delete: O(n)
                - Update: O(n)
            - Enables efficient memory management by deleting all components when a page is unmounted.

        2. **zenaura_prev_page_instance**:
            - Stores the previously mounted page instance.
            - Leverages Zenaura's single-page mounting (per route path) for efficient memory management.
            - When a new page is mounted:
                - Retrieves the previous page instance.
                - Iterates over its components and deletes them from `zen_dom_table`.

    """
    zen_dom_table = defaultdict(str)
    prev_page_instance = None
    zen_pre_compiled = defaultdict(str)
