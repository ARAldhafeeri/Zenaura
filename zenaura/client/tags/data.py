class Data:
    """
        Data structure for specifying the
         child within a node is inner text
        inside html elements used by virutal
        dom and compiler classes.
    """
    def __init__(self, content):
        """
            initlize the data structure
            args: content, turn it into
            str for compiler to sanitize
        """
        self.content = str(content)