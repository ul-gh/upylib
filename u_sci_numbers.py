def sane_str_to_f(s):
    """Returns float from string input, agnostic to language-specific
    decimal point format and with possible scientific number notation.
    
    Thousands separator not allowed.

    For invalid or empty input string, a float NaN value is returned.
    """
    try:
        f = float(s.replace(",", "."))
    except ValueError:
        return float("NaN")
    return f
