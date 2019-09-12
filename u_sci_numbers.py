import re

def validate_number(val):
    if type(val) is str:
        # Returns float from string input, taking the first occurrence of
        # any comma /or/ dot character as only valid thousands separator
        # and discards numbers following any non-number characters
        m = re.match(r"(\d+[,.]?)(\d*)(([eE][+-]?\d+)?)", val)
        if m is not None:
            s = m.group(1).replace(",", ".") + m.group(2) + m.group(3)
            return float(s)
        else:
            return float("NaN")
    elif type(val) in (int, float):
        return val