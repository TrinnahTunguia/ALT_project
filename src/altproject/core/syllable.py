
# Word syllabifier
class Syllabifier:
    def syllabify_word(self, word: str) -> list[str]:
        self._parse_word(word)

    def _parse_word(self, word: str):
        # S -> Word
        # Word -> Syllable Word | Syllable
        # Syllable -> Cluster P | KP | P | Cluster PKK | Cluster PK | KPK | PKK | PK
        # Cluster -> bl | br | dr | dy | fl | fr | gl | gr | kl | kr | kw | pl | pr | pw | py | sw | sy | tr | ts | tw | ty
        # P -> a | e | i | o | u
        # K -> b | c | d | f | g | h | j | k | l | m | n | ng | ñ | p | q | r | s | t | v | w | x | y | z
        for c in word:
            self._parse_syllable(word)

    def _parse_syllable(self, syllable: str):
        pass

    def _parse_onset(self, char: str):
        pass
