import difflib

def load_wordlist(path: str) -> set[str]:
    """
    Load dictionary words from file.
    """
    words = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if word:
                words.add(word)
    return words


def spellcheck_text(text: str, dictionary: set[str]):
    """
    Wrap misspelled words in * and return suggestions.
    """
    words = text.split()
    corrected = []
    suggestions = {}

    for word in words:
        clean = word.lower().strip(".,!?")
        if clean and clean not in dictionary:
            corrected.append(f"*{word}*")
            suggestions[word] = difflib.get_close_matches(clean, dictionary, n=3)
        else:
            corrected.append(word)

    return " ".join(corrected), suggestions