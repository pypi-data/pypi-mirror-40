class Filter():
    pass

class FilterText(Filter):
    def __init__(self, value: [str]):
        self._value = value

    def __repr__(self):
        return(f"({' '.join(self._value)})")


class FilterColumnEnum(Filter):
    def __init__(self, column: str, value: [str]):
        self._column = column
        self._value = value

    def __repr__(self):
        return(f"{self._column}:({' OR '.join(self._value)})")


def AND(*filters: Filter):
    tmp = " AND ".join([str(x) for x in filters])
    return(tmp)


def OR(*filters: Filter):
    tmp = " OR ".join([str(x) for x in filters])
    return(f"({tmp})")


def NOT(*filters: Filter):
    tmp = "NOT (" + AND(*filters) + ")"
    return(tmp)
