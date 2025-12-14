def load_banned_words(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]
    
def censor_profanity(text: str, banned_words: list[str]) -> str:
    words = text.split()
    censored = []

    for word in words:
        clean = word.lower().strip(".,!?")
        if clean in banned_words:
            censored.append("*" * len(word))
        else:
            censored.append(word)

    return " ".join(censored)