from .heap import Heap

class PriorityQueue:
    def __init__(self):
        # We should base the implementation off of a heap, since it is more efficient over a list. 
        # Make sure that you are inserting only tuples structured: (priority_weight (int), value (Any))
        self.queue = []
    
    def is_empty(self):
        """
        Check if the priority queue is empty.
        :return: True if the queue is empty, False otherwise.
        """
        pass

    def insert(self, item, priority):
        """
        Insert an item into the priority queue with a given priority.
        :param item: The item to be inserted.
        :param priority: The priority of the item.
        """
        pass

    def delete(self):
        """
        Remove and return the item with the highest priority.
        :return: The item with the highest priority.
        """
        pass

    def peek(self):
        """
        Return the item with the highest priority without removing it.
        :return: The item with the highest priority.
        """
        pass