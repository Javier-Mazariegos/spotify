class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty1(self):
        if self.head == None:
            return True
        return False

    def enqueue(self,n):
        if self.is_empty1():
            self.head = n
            self.tail = n
        else:
            self.tail.next = n
            n.next = None
            self.tail = n
    
    def dequeue(self):
        if self.is_empty1():
            return("Queue Underflow")
        else:
            x = self.head
            self.head = self.head.next
            return x
