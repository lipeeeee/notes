class Node:
    prev: object
    next: object
    val: int

    def __init__(self, prev, next, val):
        self.prev = prev
        self.next = next
        self.val = val
    
    def __repr__(self):
        return f"Node(val={self.val}, prev={self.prev.val if self.prev else 'None'}, next={self.next.val if self.next else 'None'})"

class MyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def get(self, index: int) -> int:
        if (index < 0): return -1

        i = 0
        cur = self.head
        while (i < index):
            cur = cur.next if cur else None
            i += 1
        return cur.val if cur else -1
 
    def addAtHead(self, val: int) -> None:
        new_node = Node(None, self.head, val)
        if (self.head): self.head.prev = new_node
        self.head = new_node

        if (not self.tail):
            self.tail = self.head

    def addAtTail(self, val: int) -> None:
        new_node = Node(self.tail, None, val)
        if (self.tail): self.tail.next = new_node
        self.tail = new_node

        if (not self.head):
            self.head = self.tail

    def addAtIndex(self, index: int, val: int) -> None:
        if (index < 0): return
        if (index == 0): return self.addAtHead(val)
        if (not self.head): return

        i = 1
        prev = self.head
        next = self.head.next

        while (i < index):
            prev = prev.next
            next = next.next if next else None
            i += 1
        new_node = Node(prev, next, val)
        
        if (prev): prev.next = new_node
        else: prev = self.tail

        if (next): next.prev = new_node
        else: self.tail = new_node

    def deleteAtIndex(self, index: int) -> None:
        if (index < 0): return
        if (index == 0):
            self.head = self.head.next if self.head else None
            return

        i = 1
        prev = self.head
        next = self.head.next
        while (i < index):
            prev = prev.next
            next = next.next if next else None
            i += 1
        next = next.next if next else None

        if (not prev): return    
        prev.next = next
        if (next): next.prev = prev
        else: self.tail = prev
