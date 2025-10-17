from collections.abc import Sequence
from typing import Annotated, Any, Generic, TypeVar, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    GetCoreSchemaHandler,
    PrivateAttr,
)
from pydantic_core import CoreSchema, core_schema

from katana_tsl_parser.errors import InvalidQValueError, InvalidValueListLengthError

JsonDict = dict[str, Any]


def i(n: str) -> int:
    return int(n, 16)


def decode_delay_time(values: list[str]) -> int:
    time = 0
    for v in values:
        time <<= 7
        time += i(v)

    return time


T = TypeVar("T")


class _TslBaseModel(BaseModel):
    _raw: list[str] | None = PrivateAttr(None)

    def __init__(self, **data: JsonDict) -> None:
        _raw = data.pop("_raw", None)

        super().__init__(**data)

        if _raw:
            self._raw = cast("list[str]", _raw)

    @classmethod
    def _get_fields(cls, *, by_alias: bool = False) -> set[str]:
        return set(cls.model_json_schema(by_alias=by_alias)["properties"].keys())

    @classmethod
    def _expect_size(
        cls, values: list[Any], expected: Sequence[int] | int | None = None
    ) -> None:
        size = len(values)
        if isinstance(expected, Sequence):
            if size not in expected:
                raise InvalidValueListLengthError(size, expected)

            return

        expected = expected or len(cls._get_fields())
        if size != expected:
            raise InvalidValueListLengthError(size, expected)


class TslObject(_TslBaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class TslList(_TslBaseModel, Generic[T]):
    root: list[T]


Percent = Annotated[int, Field(ge=0, le=100)]


class ToggleablePercentImpl(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))

    def __repr__(self) -> str:
        if self == 0:
            return "Off"

        return f"On<{self - 1}>"


ToggleablePercent = Annotated[ToggleablePercentImpl, Field(ge=0, le=101)]


class Gain12dBImpl(float):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(float))

    @classmethod
    def parse(cls, v: str) -> "Gain12dB":
        return cls((i(v) - 24) * 0.5)


Gain12dB = Annotated[Gain12dBImpl, Field(ge=-12.0, le=12.0, multiple_of=0.5)]


class Gain20dBImpl(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))

    @classmethod
    def parse(cls, v: str) -> "Gain20dB":
        return cls(i(v) - 20)


Gain20dB = Annotated[Gain20dBImpl, Field(ge=-20, le=20)]


class PitchImpl(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(int))

    @classmethod
    def parse(cls, v: str) -> "Pitch":
        return cls(i(v) - 24)


Pitch = Annotated[PitchImpl, Field(ge=-24, le=24)]


class Q(float):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate, handler(float)
        )

    @classmethod
    def parse(cls, v: str) -> "Q":
        return cls(2.0 ** (i(v) - 1))

    @classmethod
    def validate(cls, v: float) -> float:
        if not isinstance(v, float):
            # EM101: Exception must not use a string literal, assign to variable first
            # TRY003: Avoid specifying long messages outside the exception class
            raise TypeError("float required")  # noqa: EM101, TRY003

        if v not in (0.5, 1, 2, 4, 8, 16):
            raise InvalidQValueError(v)

        return v
