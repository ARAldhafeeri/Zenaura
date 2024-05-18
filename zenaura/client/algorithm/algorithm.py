from .searcher import Searcher
from .updater import Updater

class DiffingAlgorithm(
    Searcher,
    Updater
):
    """
        The diffing algorithm in zenaura virtual dom. 
    """