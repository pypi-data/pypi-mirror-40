from operator import attrgetter
from typing import Iterable, Sequence

from spectra_lexer.keys import StenoKeys
from spectra_lexer.rules import RuleMap


class LexerResult(RuleMap):
    """ List-based rulemap builder used during lexer matching. """

    keys: StenoKeys  # Full key string
    letters: str     # Full English text of the word.

    def __init__(self, keys="", letters="", src:Iterable=()):
        super().__init__(src)
        self.keys = keys
        self.letters = letters

    def copy(self):
        return LexerResult(self.keys, self.letters, self)

    def _keys_unmatched(self, agetter=attrgetter("rule.keys")) -> int:
        """ Get the number of keys *not* matched by mapped rules. """
        return sum(map(len, map(agetter, self))) - len(self.keys)

    def _letters_matched(self, agetter=attrgetter("rule.letters")) -> int:
        """ Get the number of characters matched by mapped rules. """
        return sum(map(len, map(agetter, self)))

    def _word_coverage(self) -> int:
        """ Return the number of characters between the start of the first child rule and the end of the last. """
        if self:
            start_item = self[0]
            end_item = self[-1]
            return end_item.start + end_item.length - start_item.start
        return 0

    def rank(self) -> Sequence[int]:
        """
        Determine the "value" of a lexer-generated rulemap.
        A larger value should reflect a more accurate mapping.
        Rank value is determined by a tuple of these values, in order:
            - least keys unmatched
            - most letters matched
            - fewest child rules
            - end-to-end word coverage
        """
        return (self._keys_unmatched(),
                self._letters_matched(),
                -len(self),
                self._word_coverage())

    def letters_matched_ratio(self) -> float:
        """ Find total characters matched divided by total characters possible to match (i.e. not spaces). """
        matched = self._letters_matched()
        matchable = sum([c != ' ' for c in self.letters])
        # All whitespace rules shouldn't happen, but let's not ruin someone's day by dividing by zero.
        return matched / matchable if matchable else 0
