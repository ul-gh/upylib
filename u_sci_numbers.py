def sane_str_to_f(s, default=None):
    """Returns float from string input, agnostic to language-specific
    decimal point format and with possible scientific number notation.
    
    Thousands separator not allowed.

    For invalid or empty input string, the default of None is returned.
    """
    try:
        f = float(s.replace(",", "."))
    except ValueError:
        return default
    return f
