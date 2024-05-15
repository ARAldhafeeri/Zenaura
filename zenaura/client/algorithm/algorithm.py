from .searcher import Searcher
from .comparer import Comparer
from .updater import Updater

class DiffingAlgorithm(
    Searcher,
    Comparer,
    Updater,
):
    """
        The diffing algorithm in zenaura virtual dom. 
        High level steps in order:

        1. search : 
            Compares the old and new component 
            trees to identify the differences.

        2. compare: 
            a step within search, 
            compares attributes of parent node, 
            data bended children.

        3. hyderate: 
            a step after search, 
            hyderates the differences stack, 
            remove any children that have parent changes.

        4. updater: 
            a step after hyderate, 
            updates the previous tree with the new tree.
            finally the return the optimized hyderated tree.
            virtual dom will iterate over the stack of differences
            and update the real dom accordingly.
    """