from collections.abc import Sequence


class InvalidContourValuesError(ValueError):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(f"Invalid values for contour: ({x}, {y})")


class InvalidQValueError(ValueError):
    def __init__(self, val: float) -> None:
        super().__init__(f"invalid Q value: {val}")


class InvalidValueListLengthError(ValueError):
    def __init__(self, size: int, expected: Sequence[int] | int) -> None:
        if isinstance(expected, Sequence):
            expected_str = ", ".join(map(str, expected[:-1])) + f" or {expected[-1]}"
            msg = f"must contain exactly {expected_str} items, not {size}"
        else:
            msg = f"must contain exactly {expected} items, not {size}"

        super().__init__(msg)


class NameTooLongError(ValueError):
    def __init__(self, n: int) -> None:
        super().__init__(f"must be 16 chars or fewer, not {n}")


class UnsupportedDeviceError(ValueError):
    def __init__(self, device: str) -> None:
        super().__init__(f"Unsupported device: {device}")
