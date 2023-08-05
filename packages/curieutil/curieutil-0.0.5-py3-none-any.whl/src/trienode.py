class TrieNode:

    def __init__(self, ch):
        self.value = ch
        self.children = { }
        self.leaf = False

    def getChildren(self):
        return self.children

    def getValue(self):
        return self.value

    def setIsLeaf(self, val):
        self.leaf = val

    def isLeaf(self):
        return self.leaf
