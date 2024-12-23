from typing import List, Dict
from collections import defaultdict
import re
from re import Match

def strip_comments(query_str: str) -> str:
    output: str = ""
    for line in query_str.split('\n'):
        comment_indxs: List[int] = [match.start() for match in re.finditer("#", line)]
        inside_iri_lookup: Dict[int, bool] = defaultdict(bool)
        # iriref_indxs: List[Tuple[int, int]] = \
        for match in re.finditer("<[^<>\"{}|^`\\]\\s]*>", line):
            update_truth_lookup(inside_iri_lookup, match)
        line_terminus: int = len(line)
        for indx in comment_indxs:
            if not inside_iri_lookup[indx]:
                line_terminus = indx
                break
        valid_part: str = line[:line_terminus].rstrip()
        valid_part += "\n" if len(valid_part) != 0 else ""
        output += valid_part
    return output

def update_truth_lookup(inside_iri_lookup: Dict[int, bool], match: Match) -> None:
    for i in range(match.start(), match.end()):
        inside_iri_lookup[i] = True

def standardize_whitespace(input: str) -> str:
    return re.sub("( |\n|\t)+", " ", input.strip())
