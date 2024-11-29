class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def append_to_front(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, value):
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

        
    def find(self, value):
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None
    
    def print_list(self):
        current = self.head
        while current:
            print(current.value, end=" -> ")
            current = current.next
        print("None")

