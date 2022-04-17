from typing import Dict

from collections import defaultdict
from fuzzywuzzy import process

from core import conf


def compare_str(str1, variants) -> bool:
    _, ratio = process.extractOne(str1, variants)
    return ratio >= conf.COMMAND_MIN_MATCH_RATIO


def analyze_words(text: str) -> Dict[str, int]:
    tokens = [token.strip() for token in text.lower().split() if len(token) > 2]
    token_dict = defaultdict(int)
    analyzed_words = []
    for token in tokens:
        if token in analyzed_words:
            continue
        token_dict[token] += 1
        analyzed_words.append(token)
        extracted_tokens = process.extract(token, [t for t in tokens if not t == token])
        for extracted_token in extracted_tokens:
            if extracted_token[1] >= conf.SAME_WORD_MIN_MATCH_RATIO:
                analyzed_words.append(extracted_tokens[0])
    return token_dict


def update_stats(
    current_stats: Dict[str, int], additional_stats: Dict[str, int]
) -> Dict[str, int]:
    new_stats = current_stats.copy()
    for additional_word, additional_count in additional_stats.items():
        if additional_word in current_stats:
            new_stats[additional_word] = (
                current_stats[additional_word] + additional_count
            )
        else:
            new_stats[additional_word] = additional_count
    return new_stats
