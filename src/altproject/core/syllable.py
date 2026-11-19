from typing import ClassVar

class SyllableParseError(Exception):
    def __init__(self, reason: str, word: str | None = None, idx: int | None = None):
        self.reason = reason
        self.word = word
        self.idx = idx

        message = reason
        if word is not None and idx is not None:
            message = f"Failed to syllabify {word} at index {idx}: {reason}"
        super().__init__(message)

# Word syllabifier
class Syllabifier:
    IRREGULAR_WORDS: ClassVar[dict[str, list[str]]] = {
        "mga": ["ma", "nga"],
    }

    def __init__(self):
        self.patinig = {
            "a", "e", "i", "o", "u",
        }
        self.katinig = {
            "b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "ng", "ñ", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
        }
        self.cluster = {
            "bl", "br", "dr", "dy", "fl", "fr", "gl", "gr", "kl", "kr", "kw", "pl", "pr", "pw", "py", "sw", "sy", "tr", "ts", "tw", "ty",
        }
        self._word = None
        self._grapheme = None
        self._idx = -1

    def syllabify_word(self, word: str) -> list[str]:
        if Syllabifier.IRREGULAR_WORDS.get(word):
            return Syllabifier.IRREGULAR_WORDS[word]

        self._word = word
        self._grapheme = self._to_grapheme(word)
        self._idx = -1
        return self._parse_word()

    def _to_grapheme(self, word: str) -> str:
        graphemes = []
        i = 0
        n = len(word)
        while i < n:
            if i + 1 < n and word[i] == "n" and word[i + 1] == "g":
                graphemes.append("ng")
                i += 2
                continue
            graphemes.append(word[i])
            i += 1
        return graphemes

    def _peek(self, k=1) -> str | None:
        if (self._idx + k) >= len(self._grapheme):
            return None

        return self._grapheme[self._idx + k]

    def _next(self) -> str | None:
        self._idx += 1

        if self._idx >= len(self._grapheme):
            return None

        return self._grapheme[self._idx]

    def _is_patinig(self, c: str) -> bool:
        return (c in self.patinig)

    def _is_katinig(self, c: str) -> bool:
        return (c in self.katinig)

    def _is_cluster(self, c1: str, c2: str) -> bool:
        if c1 is None or c2 is None:
            return False

        return ((c1 + c2) in self.cluster)

    def _expect(self, predicate: bool, reason: str):
        if predicate:
            return
        raise SyllableParseError(reason, word = self._word, idx = self._idx)

    def _parse_word(self):
        # S -> Word
        # Word -> Syllable Word | Syllable
        # Syllable -> Onset Nucleus Coda
        # Onset -> ε | K | Cluster
        # Nucleus -> P
        # Coda -> ε | K | K K | K K K
        # Cluster -> bl | br | dr | dy | fl | fr | gl | gr | kl | kr | kw | pl | pr | pw | py | sw | sy | tr | ts | tw | ty
        # P -> a | e | i | o | u
        # K -> b | c | d | f | g | h | j | k | l | m | n | ng | ñ | p | q | r | s | t | v | w | x | y | z
        syllables = []

        while self._peek() is not None:
            syllable = self._parse_syllable()
            syllables.append(syllable)

        return syllables

    def _parse_syllable(self):
        onset = self._parse_onset()
        nucleus = self._parse_nucleus()
        coda = self._parse_coda(onset)

        return onset + nucleus + coda

    def _parse_onset(self) -> str:
        c1 = self._peek(1)
        c2 = self._peek(2)
        self._expect(c1 is not None or c2 is not None, "Expected onset to be not None")

        # Empty
        if self._is_patinig(c1):
            return ""
        if self._is_cluster(c1, c2):
            # Assume cluster
            self._next()
            self._next()
            return c1 + c2
        self._next()
        return c1

    def _parse_nucleus(self):
        # 1st rule
        c = self._next()
        self._expect(self._is_patinig(c), "Expected nucleus to be patinig")
        return c

    def _parse_coda(self, onset: str):
        c1 = self._peek(1)

        # Empty
        if not self._is_katinig(c1):
            return ""

        c2 = self._peek(2)
        c3 = self._peek(3)

        # KP should be for the next onset
        if self._is_patinig(c2):
            return ""

        # Handle reduplication rule
        if onset == c1 and self._is_cluster(c1, c2) and self._is_patinig(c3):
            return ""

        # 2nd rule
        if self._is_katinig(c2) and self._is_patinig(c3):
            self._next()
            return c1

        c4 = self._peek(4)

        # 3rd rule
        if self._is_katinig(c2) and self._is_katinig(c3) and self._is_patinig(c4):
            # 4th rule
            if c1 == "m" or c1 == "n":
                rule_clusters = { "bl", "br", "dr", "pl", "tr" }
                if (c2 + c3) in rule_clusters:
                    self._next()
                    return c1
            if self._is_cluster(c2, c3):
                self._next()
                return c1
            self._next()
            self._next()
            return c1 + c2

        c5 = self._peek(5)

        # 5th rule
        if (self._is_katinig(c2) and self._is_katinig(c3) and
            self._is_katinig(c4) and self._is_patinig(c5)):
            self._next()
            self._next()
            return c1 + c2

        c2 = c2 or ""
        c3 = c3 or ""

        self._next()
        self._next()
        self._next()

        return c1 + c2 + c3
