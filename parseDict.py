"""Extract key value pairs in Python 3 using shlex and regex."""
import re
import shlpipex


def regex_kv_pairs(text, item_sep=r"\s", value_sep="="):
    """
    Parse key-value pairs from a shell-like text with regex.
    This approach is ~ 25 times faster than the shlex approach.
    Returns a dict with the keys and values from the text input
    """

    split_regex = r"""
        (?P<key>[\w\-]+)=       # Key consists of only alphanumerics and '-' character
        (?P<quote>["']?)        # Optional quote character.
        (?P<value>[\S\s]*?)     # Value is a non greedy match
        (?P=quote)              # Closing quote equals the first.
        ($|\s)                  # Entry ends with comma or end of string
    """.replace("=", value_sep).replace(r"|\s)", f"|{item_sep})")
    regex = re.compile(split_regex, re.VERBOSE)

    return {match.group("key"): match.group("value") for match in regex.finditer(text)}


def parse_kv_pairs(text, item_sep=" ", value_sep="="):
    """
    Parse key-value pairs from a shell-like text with shlex.
    This approach has behavior very similar to the standard shell parsing.
    Returns a dict with the keys and values from the text input
    """
    # initialize a lexer, in POSIX mode (to properly handle escaping)
    lexer = shlex.shlex(text, posix=True)
    # set ' ' as whitespace for the lexer
    # (the lexer will use this character to separate words)
    lexer.whitespace = item_sep
    # include '=' as a word character
    # (this is done so that the lexer returns a list of key-value pairs)
    # (if your option key or value contains any unquoted special character,
    #  you will need to add it here)
    lexer.wordchars += value_sep
    lexer.wordchars += ".-_()/:+*^&%$#@!?|{}"
    # then we separate option keys and values to build the resulting dictionary
    # (maxsplit is required to make sure that '=' in value will not be a problem)
    return dict(word.split(value_sep, maxsplit=1) for word in lexer)
