from collections import defaultdict

class LookupTable:
    zen_dom_table = defaultdict(str)
    prev_component_id = None
    prev_component_instance = None
    mounted_component_id = None   