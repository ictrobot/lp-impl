def op_and(x, y):
    return x and y


def op_or(x, y):
    return x or y


def op_not(x):
    return not x


def op_implies(x, y):
    return (x and y) or (not x)


def op_iff(x, y):
    return x == y


__all__ = [
    "op_and",
    "op_or",
    "op_not",
    "op_implies",
    "op_iff"
]