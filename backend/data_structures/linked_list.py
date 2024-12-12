class Node:
    """
    A generic node class for a linked list

    Attributes:
        value: The value of the node
        next: The next node in the linked list
    """

    def __init__(self, value):
        """
        Initializes a node with a given value

        Args:
            value: The value for the node
        """

        self.value = value
        self.next = None


class LinkedList:
    """
    A generic linked list class

    Attributes:
        head: The first node in the linked list
    """


    def __init__(self):
        """
        Initializes an empty linked list
        """

        self.head = None
    
    def append(self, value):
        """
        Appends a new node with a given value to the end of the linked list

        Args:
            value: The value for the new node
        """

        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def append_to_front(self, value):
        """
        Appends a new node with a given value to the front of the linked list

        Args:
            value: The value for the new node
        """

        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, value):
        """
        Deletes the first instance of a node with a given value from the linked list

        Args:
            value: The value of the node to delete
        """

        if self.head is None:
            return
        
        if self.head.value == value:
            self.head = self.head.next
            return
        
        current = self.head

        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                return
            
            current = current.next
    
    def pop(self):
        """
        Removes and returns the first node (head) of the linked list
        """
        if self.head is None:
            return None 
        
        popped_value = self.head.value
        self.head = self.head.next 
        return popped_value
        
    def find(self, value):
        """
        Returns the first node with a given value

        Args:
            value: The value of the node to find

        Returns:
            The first node with the given value, or None if the value is not found
        """

        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
    
    def print_list(self):
        """
        Prints the linked list
        """

        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

