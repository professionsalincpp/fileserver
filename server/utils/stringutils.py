def tostr(value: any) -> str:
    if value is None:
        return ''
    elif isinstance(value, type):
        return value.__name__
    else:
        return str(value)

def strpath(path: list) -> str:
    return '/'.join(path)