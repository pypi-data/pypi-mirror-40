from typing import (  # noqa: F401
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from darglint.token import (
    TokenType,
)
from darglint.node import (  # noqa: F401
    NodeType,
    Node,
)
from darglint.token import (  # noqa: F401
    Token,
)


NON_TERMINALS = {
    NodeType.SECTION_HEAD: [
        (NodeType.KEYWORD, NodeType.COLON),
        (NodeType.KEYWORD, NodeType.NULL),
    ],
}


TERMINALS = {
    NodeType.KEYWORD: [
        (TokenType.WORD, 'Args'),
        (TokenType.WORD, 'Returns'),
    ],
    NodeType.COLON: [
        (TokenType.COLON, ':'),
    ],
}


NODES = list(set(NON_TERMINALS.keys()) | set(TERMINALS.keys()))


class Parser(object):

    def __init__(self):
        self.terminal_lookup = dict()
        for node_type, pairs in TERMINALS.items():
            for pair in pairs:
                if pair not in self.terminal_lookup:
                    self.terminal_lookup[pair] = list()
                self.terminal_lookup[pair].append(node_type)

        self.nonterminal_lookup = dict()
        for node_type, pairs in NON_TERMINALS.items():
            for pair in pairs:
                if pair not in self.nonterminal_lookup:
                    self.nonterminal_lookup[pair] = list()
                self.nonterminal_lookup[pair].append(node_type)

        self.node_indices = {
            node: i
            for i, node in enumerate(NODES)
        }  # type: Dict[Node, int]

    def cyk(self, I):
        # type: (List[Token]) -> Optional[Node]
        """Perform the Cocke-Younger-Kasami Algorithm on the Tokens.

        Args:
            I: A list of tokens.

        Returns:
            The node which represents the production.

        """
        n = len(I)
        r = len(NODES)
        P = [[[None for _ in range(r)] for _ in range(n)] for _ in range(n)]
        for i, token in enumerate(I):
            needle = (token.token_type, token.value)
            for node in self.terminal_lookup.get(needle, []):
                P[0][i][self.node_indices[node]] = node
        for l in range(1, n):
            for s in range(n - l):
                for p in range(l - 2):
                    for production, rule in self.nonterminal_lookup.items():
                        a = self.node_indices[production]
                        b = self.node_indices[rule[0]]
                        c = self.node_indices[rule[1]]
                        if P[p][s][b] and P[l - p][s + p][c]:
                            P[l][s][a] = production
        return P[n - 1][0][0]

    def parse(self, tokens):
        # type: (List[Token]) -> Optional[Node]
        return self.cyk(tokens)
