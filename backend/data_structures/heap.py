class Heap:
    """
    A basic max-heap data structure that stores elements with a weight and value.
    The heap maintains the heap property such that the largest element is always at the root.

    Attributes:
        _data (list): The internal list used to store the heap elements as tuples of (weight, value).
    """

    def __init__(self):
        """
        Initializes a new instance of the Heap class.

        The heap stores elements as tuples in the form (weight, value), where weight is an integer 
        and value can be any object.
        """
        self._data = []

    def insert(self, value):
        """
        Inserts a new value into the heap.

        Args:
            value (tuple): The value to be inserted into the heap, expected to be a tuple (weight, value).
        
        Returns:
            bool: True after successfully inserting the value into the heap.
        """
        self._data.append(value)
        self._heapify_up(self.size() - 1)
        return True

    def pop(self):
        """
        Removes and returns the maximum value (root of the heap) from the heap.

        Returns:
            tuple or None: The maximum value as a tuple (weight, value), or None if the heap is empty.
        """
        if self.is_empty():
            return None
        
        rtn = self._data[0]
        self._data[0] = self._data[self.size() - 1]
        self._data.pop() 
        self._heapify_down(0)
        return rtn

    def peek(self):
        """
        Returns the maximum value (root of the heap) without removing it.

        Returns:
            tuple or None: The maximum value as a tuple (weight, value), or None if the heap is empty.
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
        Checks if the heap is empty.

        Returns:
            bool: True if the heap is empty, False otherwise.
        """
        return self.size() == 0

    def _heapify_up(self, index):
        """
        Maintains the heap property by moving a node up the tree.

        Args:
            index (int): The index of the node to be moved up the tree.
        """
        if index == 0:
            return
        
        parent = (index - 1) // 2
        compare = self._compare(self._data[parent], self._data[index])
        if compare == -1:
            # Swap the node with its parent and continue moving up the tree
            self._data[parent], self._data[index] = self._data[index], self._data[parent]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        """
        Maintains the heap property by moving a node down the tree.

        Args:
            index (int): The index of the node to be moved down the tree.
        """
        if index >= self.size():
            return
        
        children = [2 * index + 1, 2 * index + 2]
        largest = index
        
        for child in children:
            if child < self.size():
                comp = self._compare(self._data[largest], self._data[child])
                if comp == -1:
                    largest = child

        if largest != index:
            # Swap the node with the largest child and continue moving down the tree
            self._data[largest], self._data[index] = self._data[index], self._data[largest]
            self._heapify_down(largest)

    def _compare(self, item1, item2):
        """
        Compares two items in the heap.

        Args:
            item1 (tuple): The first item (weight, value) to be compared.
            item2 (tuple): The second item (weight, value) to be compared.

        Returns:
            int: 1 if item1's weight is less than item2's, 
                -1 if item1's weight is greater than item2's, 
                 0 if both weights are equal.
        """
        if item1[0] > item2[0]:
            return -1
        elif item1[0] < item2[0]:
            return 1
        
        return 0