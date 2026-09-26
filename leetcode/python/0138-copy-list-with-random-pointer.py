"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        newNode = None
        dummy = None
        while head:
            newNode = copy.deepcopy(head)
            head = head.next
            if not dummy:
                dummy = Node(0)
                dummy.next = newNode 
        
        return dummy.next if dummy else None
