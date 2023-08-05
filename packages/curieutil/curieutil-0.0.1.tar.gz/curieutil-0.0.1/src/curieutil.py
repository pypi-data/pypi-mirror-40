from src.trie import Trie
from bidict import bidict


class CurieUtil:

    def __init__(self, mapping):
        self.trie = Trie()
        self.curieMap = mapping

        for val in mapping.values():
            self.trie.insert(val)

    def getPrefixes(self):
        return self.curieMap.keys()

    def getExpansion(self, curiePrefix):
        return self.curieMap[curiePrefix]

    def getCurie(self, iri):
        prefix = self.trie.getMatchingPrefix(iri)
        if not prefix or prefix == "":
            return None
        else:
            curiePrefix = self.curieMap.inv[prefix]
            return curiePrefix + ":" + iri[len(prefix):len(iri)]

    def getIri(self, curie):
        if not curie:
            return None
        split = curie.split(":")
        if len(split) == 0:
            return None

        prefix = split[0]
        if prefix in self.curieMap.keys():
            return self.curieMap[prefix] + curie[curie.index(":") + 1:]

        return None

    def getCurieMap(self):
        return self.curieMap

    @staticmethod
    def parseContext(jsonObject):
        jsonContext = jsonObject["@context"]
        map = bidict()
        for k, v in jsonContext.items():
            map[k] = v
        return map