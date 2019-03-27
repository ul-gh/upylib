from functools import reduce

def compose2(f, g):
    "Compose two functions"
    return lambda *args, **kwargs: f(g(*args, **kwargs))

def compose(*funcs):
    "Compose multiple functions"
    return reduce(compose2, funcs)