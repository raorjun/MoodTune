class Heap:
    """
    Basic min heap data structure implementation.
    """

    def __init__(self):
        """
        Initializes a new instance of the Heap class.
        """
        self._data = []

    def insert(self, value):
        """
        Inserts a new value into the heap.

        Args:
            value: The value to be inserted
        """
        self._data.append(value)
        self._heapify_up(self.size() - 1)
        return True

    def pop(self):
        """
        Extracts the minimum value from the heap.

        Returns:
            The minimum value, or None if the heap is empty
        """
        
        if self.is_empty():
            return None
        
        rtn = self._data[0]
        self._data[0] = self._data[self.size() - 1]
        self._heapify_down(0)
        return rtn

    def peek(self):
        """
        Returns the minimum value from the heap without removing it.

        Returns:
            The minimum value, or None if the heap is empty
        """
        
        if self.is_empty():
            return None
        
        return self._data[0]

    def size(self):
        """
        Returns the number of elements in the heap.

        Returns:
            The number of elements in the heap
        """
        return len(self._data)
    
    def is_empty(self):
        """
        Returns a boolean value indicating whether the heap is empty.

            Returns:
            True if the heap is empty, False otherwise
        """
        return self.size() == 0

    def _heapify_up(self, index):
        """
        Maintains the heap property by moving a node up the tree.

        Args:
            index: The index of the node to move up
        """
        
        if index == 0:
            return
        
        parent = (index - 1) / 2
        compare = self._compare( self._data[parent], self._data[index])
        if compare == 1:
            tmp = self._data[parent]
            self._data[parent] = self._data[index]
            self._data[index] = tmp
            self._heapify_up(parent)

    def _heapify_down(self, index):
        """
        Maintains the heap property by moving a node down the tree.

        Args:
            index: The index of the node to move down
        """
        
        if index >= self.size():
            return
        
        children = [2 * index + 1, 2 * index + 2]
        min = index
        for child in children:
            if child < self.size():
                comp = self._compare(self._data[min], self._data[child])
                if comp == 1:
                    min = child

    def _compare(self, item1, item2):
        """
        Compares two items in the heap.

        Args:
            item1: The first item
            item2: The second item
        
        Returns:
            1 if item1 is greater than item2, -1 if item1 is less than item2, and 0 otherwise
        """

        if item1.get(0) < item2.get(0):
            return -1
        elif item1.get(0) > item2.get(0):
            return 1
        
        return 0
