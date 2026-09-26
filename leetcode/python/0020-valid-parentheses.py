class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        def isOpening(char):
            return char in ["(", "{", "["]
        
        def checkMatch(char1, char2):
            if char1 == "(":
                return char2 == ")"
            elif char1 == "[":
                return char2 == "]"
            elif char1 == "{":
                return char2 == "}"

        for char in s:
            if isOpening(char):
                stack.append(char)
            else:
                if len(stack) == 0:
                    return False
                if not checkMatch(stack.pop(), char):
                    return False        
        
        if len(stack) != 0:
            return False
        return True
