from typing import Any, Callable, Generator

from pydantic import BaseModel, ConstrainedFloat, ConstrainedInt, Extra

JsonDict = dict[str, Any]


def i(n: str) -> int:
    return int(n, 16)


def decode_delay_time(values: list[str]) -> int:
    time = 0
    for v in values:
        time <<= 7
        time += i(v)

    return time


class TslBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid

    @classmethod
    def _get_fields(cls, by_alias: bool = False) -> set[str]:
        return set(cls.schema(by_alias=by_alias)["properties"].keys())


class Percent(ConstrainedInt):
    ge = 0
    le = 100


class ToggleablePercent(ConstrainedInt):
    ge = 0
    le = 101

    def __repr__(self) -> str:
        if self == 0:
            return "Off"

        return f"On<{self - 1}>"


class Gain12dB(ConstrainedFloat):
    ge = -12.0
    le = 12.0
    multiple_of = 0.5

    @classmethod
    def parse(cls, v: str) -> "Gain12dB":
        return cls((i(v) - 24) * 0.5)


class Gain20dB(ConstrainedInt):
    ge = -20
    le = 20

    @classmethod
    def parse(cls, v: str) -> "Gain20dB":
        return cls(i(v) - 20)


class Pitch(ConstrainedInt):
    ge = -24
    le = 24

    @classmethod
    def parse(cls, v: str) -> "Pitch":
        return cls(i(v) - 24)


class Q(float):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[float], float], None, None]:
        yield cls.validate

    @classmethod
    def parse(cls, v: str) -> "Q":
        return cls(2.0 ** (i(v) - 1))

    @classmethod
    def validate(cls, v: float) -> float:
        if not isinstance(v, float):
            raise TypeError("float required")

        if v not in (0.5, 1, 2, 4, 8, 16):
            raise ValueError("invalid Q value")

        return v
