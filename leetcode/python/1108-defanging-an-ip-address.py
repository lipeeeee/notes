class Solution:
    def defangIPaddr(self, address: str) -> str:
        # wtf
        return address.replace(".", "[.]")
