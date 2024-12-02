from re import Match
import re

def is_valid_iri(iri: str) -> bool:
    # Reg expression eval of string using '<' ([^<>"{}|^`\]-[#x00-#x20])* '>'
    match: Match = re.search("^<  >$", iri)
    if match:
        return True
    return False


def is_valid_prefix_name(pname: str) -> bool:
    match: Match = re.search("", pname)
    if match:
        return True
    return False
