
class Tokenizer:
    @staticmethod
    def from_filipino(source: str) -> list[str]:
        return source.strip().lower().split(" ")
