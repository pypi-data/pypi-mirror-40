# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
from typing import List


class Module:

    def __init__(
            self,
            sources: List['Module'],
            distinguishing: List[str],  # fields that uniquely identify a file/object
    ):
        self._children = []
        self.sources = sources
