from pathlib import Path
from fastapi import HTTPException
from app.services.profanity_filter import load_banned_words, censor_profanity
from app.services.spellchecker import load_wordlist, spellcheck_text




async def apply_filters(file_path: str, run_profanity: bool, run_spellcheck: bool, banned_words_path: str = "app/resources/bad_words.txt", wordlist_path: str = "app/resources/wordlist.txt"):
    """
    Used for applying filters to a text file.
    Profanity filter and spellchecker.
    """

    path = Path(file_path)

    if not path.exists():
        raise HTTPException(status_code=500, detail="Text file not found for filtering")
    
    text = path.read_text(encoding="utf-8", errors="replace")

    if run_profanity:
        banned_words = load_banned_words(banned_words_path)
        text = censor_profanity(text, banned_words)

    if run_spellcheck:
        dictionary = load_wordlist(wordlist_path)
        text, _ = spellcheck_text(text, dictionary)

    path.write_text(text, encoding="utf-8")

    print(f"Filters will be applied to: {file_path}")
