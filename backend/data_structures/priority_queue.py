from .heap import Heap

class PriorityQueue:
    """
    A priority queue is a data structure that stores elements with priorities.
    """

    def __init__(self):
        """
        Initializes a new instance of the PriorityQueue class.
        """
        self.queue = Heap()
    
    def is_empty(self):
        """
        Check if the priority queue is empty.
        
        Returns:
            True if the queue is empty, False otherwise
        """

        return self.queue.is_empty()

    def insert(self, item, priority):
        """
        Insert an item into the priority queue with a given priority.
        
        Args:
            item: The item to be inserted
            priority: The priority of the item
        """

        self.queue.insert((priority, item))

    def pop(self):
        """
        Remove and return the item with the highest priority.
        
        Returns:
            The item with the highest priority, or None if the queue is empty
        """

        top = self.queue.pop()
        if top == None:
            return None
        
        return top.get(1)

    def peek(self):
        """
        Return the item with the highest priority without removing it.
        
        Returns:
            The item with the highest priority, or None if the queue is empty
        """

        top = self.queue.peek()
        if top == None:
            return None
        
        return top.get(1)
    
    def size(self):
        """
        Return the number of elements in the priority queue.
        
        Returns:
            The number of elements in the priority queue
        """

        return self.queue.size()
    

