from .heap import Heap

class PriorityQueue:
    """
    A priority queue is a data structure that stores elements with associated priorities.
    The elements are ordered by their priority, with the highest priority elements being 
    removed first.

    Attributes:
        queue (Heap): The internal heap used to store the elements.
    """

    def __init__(self):
        """
        Initializes a new instance of the PriorityQueue class.

        The priority queue stores elements as tuples in the form (priority, value), 
        where priority is an integer and value can be any object.
        """
        self._queue = Heap()
    
    def is_empty(self):
        """
        Checks if the priority queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return self._queue.is_empty()

    def insert(self, item, priority):
        """
        Inserts an item into the priority queue with the given priority.

        Args:
            item (Any): The item to be inserted into the queue.
            priority (int): The priority of the item, where a lower value indicates higher priority.
        """
        self._queue.insert((priority, item))

    def pop(self):
        """
        Removes and returns the item with the highest priority.

        Returns:
            Any: The item with the highest priority, or None if the queue is empty.
        """
        top = self._queue.pop()
        if top is None:
            return None
        
        return top[1]

    def peek(self):
        """
        Returns the item with the highest priority without removing it.

        Returns:
            Any: The item with the highest priority, or None if the queue is empty.
        """
        top = self._queue.peek()
        if top is None:
            return None
        
        return top[1]
    
    def size(self):
        """
        Returns the number of elements in the priority queue.

        Returns:
            int: The number of elements in the queue.
        """
        return self._queue.size()
