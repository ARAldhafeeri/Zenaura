from collections import defaultdict

class VDomLookupTable:
    """
        1. zen_dom_table :
        - Optimizing general tree structure
        - each component unique componentId
        - each child of the component has ZENAURA_DOM_ATTRIBUTE
        this allows for:
        - searching for mounted component prev state : O(1)
        - deleting unmounted components : O(1)
        - inserting mounted components : O(1)
        now same time complexity applies on tree structure:
        - search O(n)
        - insert O(n)
        - delete O(n)
        - update O(n)
        aslo allows for effecient management of memory
        since in zenaura one page and each page is a dummy node
        of children components
        then once the page unmounted all the components are deleted

        2. zenaura prev_page_instance:
        - once page is mounted we store the prev_page_instance
        - zenaura mount single page at a time or " route path "
        - this allow for effecient memory management
        - once new page is mounted:
            - get the prev page instance
            - iterage over the prev page components
            - delete the prev page component from zen_dom_table

    """
    zen_dom_table = defaultdict(str)
    prev_page_instance = None
    zen_pre_compiled = defaultdict(str)
