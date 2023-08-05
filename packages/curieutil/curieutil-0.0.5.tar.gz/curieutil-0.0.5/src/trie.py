from .trienode import TrieNode


class Trie:

    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word):
        length = len(word)
        crawl = self.root

        for level in range(0, length):
            child = crawl.getChildren()
            ch = word[level]

            if ch in child:
                crawl = child[ch]
            else:
                temp = TrieNode(ch)
                child[ch] = temp
                crawl = temp

        crawl.setIsLeaf(True)

    def getMatchingPrefix(self, prefix):
        result = ""

        length = len(prefix)

        crawl = self.root

        prevMatch = 0

        for level in range(0, length):
            ch = prefix[level]
            child = crawl.getChildren()

            if ch in child:
                result += ch
                crawl = child[ch]

                if crawl.isLeaf():
                    prevMatch = level + 1

            else:
                break

        if not crawl.isLeaf():
            return result[0:prevMatch]
        return result
