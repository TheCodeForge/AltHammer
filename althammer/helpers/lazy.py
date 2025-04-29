# Prevents certain properties from having to be recomputed each time they
# are referenced


def lazy(f):

    def wrapper(*args, **kwargs):

        o = args[0]

        key=f"{f.__name__}|{[str(x) for x in args[1:]]}|{sorted([str(x)+"="+str(kwargs[x]) for x in kwargs])}"

        if "_lazy" not in o.__dict__:
            o.__dict__["_lazy"] = {}

        if key not in o.__dict__["_lazy"]:
            o.__dict__["_lazy"][key] = f(*args, **kwargs)

        return o.__dict__["_lazy"][key]

    wrapper.__name__ = f.__name__
    return wrapper