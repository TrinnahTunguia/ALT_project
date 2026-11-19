from altproject.core.tokenizer import Tokenizer
from altproject.core.syllable import Syllabifier

def main() -> None:
    syllabifier = Syllabifier()
    words = [
        "aklat",
        "sobre",
        "eksperto",
        "templo",
        "kontrol",
        "ekstra",
        "transkripsiyon",
        "nakikipagtrabaho",
        "pinagsusumikapan",
        "nakapagpapabagabag",
        "magpapakadalubhasa",
        "magtatransport",
        "piprituhin",
        "talagang",
    ]
    for word in words:
        syllables = syllabifier.syllabify_word(word)
        print(syllables)
