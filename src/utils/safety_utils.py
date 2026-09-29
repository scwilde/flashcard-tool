def try_to_int(s: str) -> int | ValueError:
    try:
        return int(s)
    except ValueError as e:
        return e

def assert_unreachable():
    raise AssertionError("Hit a code path that is supposed to be unreachable!")
