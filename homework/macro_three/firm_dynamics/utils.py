from numbers import Number


def functionify(factor):
    if factor is None:
        return lambda *args: 1
    elif isinstance(factor, Number):
        return lambda *args: factor
    elif callable(factor):
        return factor
    else:
        raise ValueError(
            "Factor type not understood, use None, number or callable")
