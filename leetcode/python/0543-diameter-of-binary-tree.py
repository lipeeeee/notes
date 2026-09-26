# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        def diam(root):
            if not root:
                return 0
                  
            def length(root):
                if not root:
                    return 0
                
                return 1 + max(length(root.left), length(root.right))

            return length(root.right) + length(root.left)
        
        max_ = diam(root)
        def max_diam(root):
            if not root:
                return
        
            nonlocal max_
            max_ = max(diam(root.left), max_)
            max_ = max(diam(root.right), max_)
            max_diam(root.right)
            max_diam(root.left)
        max_diam(root)
        return max_
