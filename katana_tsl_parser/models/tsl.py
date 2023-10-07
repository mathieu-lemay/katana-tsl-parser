from pydantic import Extra, Field, validator

from katana_tsl_parser.errors import (
    InvalidContourValuesError,
    NameTooLongError,
    UnsupportedDeviceError,
)

from .enums import (
    AmpType,
    BoostType,
    CabResonance,
    ContourChoice,
    DelayType,
    EqPosition,
    EqType,
    HighCutFreq,
    Key,
    Light,
    LowCutFreq,
    MidFreq,
    ModFxType,
    PedalFxType,
    PedalWahType,
    Phase,
    Range,
    ReverbMode,
    ReverbType,
)
from .mod_fx import FxModel
from .types import (
    Gain12dB,
    Gain20dB,
    JsonDict,
    Percent,
    Pitch,
    Q,
    TslBaseModel,
    decode_delay_time,
    i,
)

MAX_NAME_LENGTH = 16


class EqModel(TslBaseModel):
    on: bool
    type_: EqType
    low_cut: LowCutFreq
    low_gain: Gain20dB
    low_mid_freq: MidFreq
    low_mid_q: float
    low_mid_gain: Gain20dB
    high_mid_freq: MidFreq
    high_mid_q: float
    high_mid_gain: Gain20dB
    high_gain: Gain20dB
    high_cut: HighCutFreq
    level: Gain20dB
    bar_31: Gain12dB
    bar_62: Gain12dB
    bar_125: Gain12dB
    bar_250: Gain12dB
    bar_500: Gain12dB
    bar_1000: Gain12dB
    bar_2000: Gain12dB
    bar_4000: Gain12dB
    bar_8000: Gain12dB
    bar_16000: Gain12dB
    bar_level: Gain12dB

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values)

        return {
            "on": i(values[0]) > 0,
            "type_": EqType(i(values[1])),
            "low_cut": LowCutFreq(i(values[2])),
            "low_gain": Gain20dB.parse(values[3]),
            "low_mid_freq": MidFreq(i(values[4])),
            "low_mid_q": Q.parse(values[5]),
            "low_mid_gain": Gain20dB.parse(values[6]),
            "high_mid_freq": MidFreq(i(values[7])),
            "high_mid_q": Q.parse(values[8]),
            "high_mid_gain": Gain20dB.parse(values[9]),
            "high_gain": Gain20dB.parse(values[10]),
            "high_cut": HighCutFreq(i(values[11])),
            "level": Gain20dB.parse(values[12]),
            "bar_31": Gain12dB.parse(values[13]),
            "bar_62": Gain12dB.parse(values[14]),
            "bar_125": Gain12dB.parse(values[15]),
            "bar_250": Gain12dB.parse(values[16]),
            "bar_500": Gain12dB.parse(values[17]),
            "bar_1000": Gain12dB.parse(values[18]),
            "bar_2000": Gain12dB.parse(values[19]),
            "bar_4000": Gain12dB.parse(values[20]),
            "bar_8000": Gain12dB.parse(values[21]),
            "bar_16000": Gain12dB.parse(values[22]),
            "bar_level": Gain12dB.parse(values[23]),
        }


class Patch0Model(TslBaseModel):
    boost_on: bool
    boost_type: BoostType
    boost_drive: Percent
    boost_bottom: int = Field(ge=-50, le=50)
    boost_tone: int = Field(ge=-50, le=50)
    boost_solo_on: bool
    boost_solo_level: Percent
    boost_direct_mix: Percent
    boost_level: Percent

    amp_type: AmpType
    amp_gain: Percent
    amp_volume: Percent
    amp_eq_bass: Percent
    amp_eq_middle: Percent
    amp_eq_treble: Percent
    amp_eq_presence: Percent

    eq: EqModel

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values, 72)

        return {
            "boost_on": i(values[0]) > 0,
            "boost_type": BoostType(i(values[1])),
            "boost_drive": i(values[2]),
            "boost_bottom": i(values[3]) - 50,
            "boost_tone": i(values[4]) - 50,
            "boost_solo_on": i(values[5]) > 0,
            "boost_solo_level": i(values[6]),
            "boost_level": i(values[7]),
            "boost_direct_mix": i(values[8]),
            # TODO: 9 -> 16
            "amp_type": AmpType(i(values[17])),
            "amp_gain": i(values[18]),
            "amp_eq_bass": i(values[20]),
            "amp_eq_middle": i(values[21]),
            "amp_eq_treble": i(values[22]),
            "amp_eq_presence": i(values[23]),
            "amp_volume": i(values[24]),
            # TODO: 25 -> 47
            "eq": EqModel.decode_tsl(values[48:]),
        }


class Patch1Model(TslBaseModel):
    reverb_on: bool
    reverb_type: ReverbType
    reverb_time: float = Field(ge=0.1, le=10.0, multiple_of=0.1)
    reverb_pre_delay: int = Field(ge=0, le=500)
    reverb_low_cut: LowCutFreq
    reverb_high_cut: HighCutFreq
    reverb_density: int = Field(ge=0, le=10)
    reverb_effect_level: Percent
    reverb_direct_mix: Percent
    reverb_color: Percent
    pedal_fx_type: PedalFxType
    pedal_fx_wah_type: PedalWahType
    pedal_fx_wah_pos: Percent
    pedal_fx_wah_min: Percent
    pedal_fx_wah_max: Percent
    pedal_fx_wah_level: Percent
    pedal_fx_wah_direct_mix: Percent
    pedal_fx_bend_pos: Percent
    pedal_fx_bend_pitch: Pitch
    pedal_fx_bend_level: Percent
    pedal_fx_bend_direct_mix: Percent
    pedal_fx_wah95_pos: Percent
    pedal_fx_wah95_min: Percent
    pedal_fx_wah95_max: Percent
    pedal_fx_wah95_level: Percent
    pedal_fx_wah95_direct_mix: Percent
    noise_suppressor_on: bool
    noise_suppressor_threshold: Percent
    noise_suppressor_release: Percent
    master_key: Key
    # V2
    solo_on: bool | None
    solo_level: Percent | None

    contour: ContourChoice | None

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values, (50, 91))

        res = {
            "reverb_on": i(values[0]) > 0,
            "reverb_type": ReverbType(i(values[1])),
            "reverb_time": (i(values[2]) + 1) / 10.0,
            "reverb_pre_delay": decode_delay_time(values[3:5]),
            "reverb_low_cut": LowCutFreq(i(values[5])),
            "reverb_high_cut": HighCutFreq(i(values[6])),
            "reverb_density": i(values[7]),
            "reverb_effect_level": i(values[8]),
            "reverb_direct_mix": i(values[9]),
            "reverb_color": i(values[11]),
            "pedal_fx_type": i(values[17]),
            "pedal_fx_wah_type": i(values[18]),
            "pedal_fx_wah_pos": i(values[19]),
            "pedal_fx_wah_min": i(values[20]),
            "pedal_fx_wah_max": i(values[21]),
            "pedal_fx_wah_level": i(values[22]),
            "pedal_fx_wah_direct_mix": i(values[23]),
            "pedal_fx_bend_pitch": Pitch.parse(values[24]),
            "pedal_fx_bend_pos": i(values[25]),
            "pedal_fx_bend_level": i(values[26]),
            "pedal_fx_bend_direct_mix": i(values[27]),
            "pedal_fx_wah95_pos": i(values[28]),
            "pedal_fx_wah95_min": i(values[29]),
            "pedal_fx_wah95_max": i(values[30]),
            "pedal_fx_wah95_level": i(values[31]),
            "pedal_fx_wah95_direct_mix": i(values[32]),
            "noise_suppressor_on": i(values[38]) > 0,
            "noise_suppressor_threshold": i(values[39]),
            "noise_suppressor_release": i(values[40]),
            "master_key": Key(i(values[49])),
        }

        if len(values) == 91:  # noqa: PLR2004
            res.update(
                {
                    "solo_on": i(values[84]) > 0,
                    "solo_level": i(values[85]),
                },
            )

            match i(values[86]), i(values[87]):
                case 0, 0:
                    contour = 0
                case 1, 0:
                    contour = 1
                case 1, 1:
                    contour = 2
                case 1, 2:
                    contour = 3
                case x, y:
                    raise InvalidContourValuesError(x, y)

            res["contour"] = contour

        return res


class Patch2Model(TslBaseModel):
    boost_green: BoostType
    boost_red: BoostType
    boost_yellow: BoostType
    mod_green: ModFxType
    mod_red: ModFxType
    mod_yellow: ModFxType
    fx_green: ModFxType
    fx_red: ModFxType
    fx_yellow: ModFxType
    delay_green: DelayType
    delay_red: DelayType
    delay_yellow: DelayType
    reverb_green: ReverbType
    reverb_red: ReverbType
    reverb_yellow: ReverbType
    delay2_green: DelayType
    delay2_red: DelayType
    delay2_yellow: DelayType
    reverb_green_mode: ReverbMode
    reverb_red_mode: ReverbMode
    reverb_yellow_mode: ReverbMode

    boost_light: Light
    mod_light: Light
    fx_light: Light
    delay_light: Light
    reverb_light: Light

    cab_resonance: CabResonance

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values, 36)

        return {
            "boost_green": BoostType(i(values[4])),
            "boost_red": BoostType(i(values[5])),
            "boost_yellow": BoostType(i(values[6])),
            "mod_green": ModFxType(i(values[7])),
            "mod_red": ModFxType(i(values[8])),
            "mod_yellow": ModFxType(i(values[9])),
            "fx_green": ModFxType(i(values[10])),
            "fx_red": ModFxType(i(values[11])),
            "fx_yellow": ModFxType(i(values[12])),
            "delay_green": DelayType(i(values[13])),
            "delay_red": DelayType(i(values[14])),
            "delay_yellow": DelayType(i(values[15])),
            "reverb_green": ReverbType(i(values[16])),
            "reverb_red": ReverbType(i(values[17])),
            "reverb_yellow": ReverbType(i(values[18])),
            "delay2_green": DelayType(i(values[19])),
            "delay2_red": DelayType(i(values[20])),
            "delay2_yellow": DelayType(i(values[21])),
            "reverb_green_mode": ReverbMode(i(values[22])),
            "reverb_red_mode": ReverbMode(i(values[23])),
            "reverb_yellow_mode": ReverbMode(i(values[24])),
            "boost_light": Light(i(values[25])),
            "mod_light": Light(i(values[26])),
            "fx_light": Light(i(values[27])),
            "delay_light": Light(i(values[28])),
            "reverb_light": Light(i(values[29])),
            "cab_resonance": CabResonance(i(values[35])),
        }


class PatchMk2v2Model(TslBaseModel):
    solo_eq_position: EqPosition
    solo_eq_on: bool
    solo_eq_low_cut: LowCutFreq
    solo_eq_low_gain: Gain12dB
    solo_eq_mid_freq: MidFreq
    solo_eq_mid_q: Q
    solo_eq_mid_gain: Gain12dB
    solo_eq_high_gain: Gain12dB
    solo_eq_high_cut: HighCutFreq
    solo_eq_level: Gain12dB

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values)

        return {
            "solo_eq_position": i(values[0]),
            "solo_eq_on": i(values[1]) > 0,
            "solo_eq_low_cut": LowCutFreq(i(values[2])),
            "solo_eq_low_gain": Gain12dB.parse(values[3]),
            "solo_eq_mid_freq": MidFreq(i(values[4])),
            "solo_eq_mid_q": Q.parse(values[5]),
            "solo_eq_mid_gain": Gain12dB.parse(values[6]),
            "solo_eq_high_gain": Gain12dB.parse(values[7]),
            "solo_eq_high_cut": HighCutFreq(i(values[8])),
            "solo_eq_level": Gain12dB.parse(values[9]),
        }


class DelayModel(TslBaseModel):
    delay_on: bool
    delay_type: DelayType
    delay_time: int
    feedback: int
    high_cut: HighCutFreq
    effect_level: int
    direct_mix: int
    tap_time: int
    mod_rate: int
    mod_depth: int
    filter_on: bool
    range_: Range
    feedback_phase: Phase
    delay_phase: Phase
    mod_sw_on: bool

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values, 26)

        return {
            "delay_on": i(values[0]) > 0,
            "delay_type": DelayType(i(values[1])),
            "delay_time": decode_delay_time(values[2:4]),
            "feedback": i(values[4]),
            "high_cut": HighCutFreq(i(values[5])),
            "effect_level": i(values[6]),
            "direct_mix": i(values[7]),
            "tap_time": i(values[8]),
            "mod_rate": i(values[19]),
            "mod_depth": i(values[20]),
            "range_": Range(i(values[21])),
            "filter_on": i(values[22]) > 0,
            "feedback_phase": Phase(i(values[23])),
            "delay_phase": Phase(i(values[24])),
            "mod_sw_on": i(values[25]) > 0,
        }


class ContourModel(TslBaseModel):
    contour_type: int
    freq_shift: int

    @classmethod
    def decode_tsl(cls, values: list[str]) -> JsonDict:
        cls._expect_size(values, (2, 8))

        # TODO: Items 2 to 7
        return {
            "contour_type": i(values[0]) + 1,
            "freq_shift": i(values[1]) - 50,
            "_raw": values,
        }


class ParamSetModel(TslBaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = Extra.ignore

    name: str = Field(alias="UserPatch%PatchName")
    patch0: Patch0Model = Field(alias="UserPatch%Patch_0")

    fx1: FxModel = Field(alias="UserPatch%Fx(1)")
    fx2: FxModel = Field(alias="UserPatch%Fx(2)")
    delay1: DelayModel = Field(alias="UserPatch%Delay(1)")
    delay2: DelayModel = Field(alias="UserPatch%Delay(2)")
    patch1: Patch1Model = Field(alias="UserPatch%Patch_1")
    patch2: Patch2Model = Field(alias="UserPatch%Patch_2")
    # status: list[str] = Field(alias="UserPatch%Status")  # noqa: ERA001
    # knob_assign: list[str] = Field(alias="UserPatch%KnobAsgn")  # noqa: ERA001
    # expression_pedal_assign: list[str] = Field(alias="UserPatch%ExpPedalAsgn")  # noqa: ERA001, E501
    # expression_pedal_min_max: list[str] = Field(alias="UserPatch%ExpPedalAsgnMinMax")  # noqa: ERA001, E501
    # gafc_expression1_assign: list[str] = Field(alias="UserPatch%GafcExp1Asgn")  # noqa: ERA001, E501
    # gafc_expression1_min_max: list[str] = Field(alias="UserPatch%GafcExp1AsgnMinMax")  # noqa: ERA001, E501
    # gafc_expression2_assign: list[str] = Field(alias="UserPatch%GafcExp2Asgn")  # noqa: ERA001, E501
    # gafc_expression2_min_max: list[str] = Field(alias="UserPatch%GafcExp2AsgnMinMax")  # noqa: ERA001, E501
    # footswitch_assign: list[str] | None = Field(alias="UserPatch%FsAsgn")  # noqa: ERA001, E501
    patch_mk2v2: PatchMk2v2Model | None = Field(alias="UserPatch%Patch_Mk2V2")
    contour1: ContourModel | None = Field(alias="UserPatch%Contour(1)")
    contour2: ContourModel | None = Field(alias="UserPatch%Contour(2)")
    contour3: ContourModel | None = Field(alias="UserPatch%Contour(3)")
    eq2: EqModel = Field(alias="UserPatch%Eq(2)")

    # TODO: Move all the validators to parse_tsl and add Version enum

    @validator("name", pre=True)
    def validate_name(cls, v: str | list[str]) -> str:
        if isinstance(v, list):
            v = "".join([chr(int(i, 16)) for i in v])

        if len(v) > MAX_NAME_LENGTH:
            raise NameTooLongError(len(v))

        return v.rstrip()

    @validator("fx1", pre=True)
    def parse_fx1(cls, v: list[str]) -> JsonDict:
        return FxModel.decode_tsl(v)

    @validator("fx2", pre=True)
    def parse_fx2(cls, v: list[str]) -> JsonDict:
        return FxModel.decode_tsl(v)

    @validator("delay1", pre=True)
    def parse_delay1(cls, v: list[str]) -> JsonDict:
        return DelayModel.decode_tsl(v)

    @validator("delay2", pre=True)
    def parse_delay2(cls, v: list[str]) -> JsonDict:
        return DelayModel.decode_tsl(v)

    @validator("patch0", pre=True)
    def parse_patch0(cls, v: list[str]) -> JsonDict:
        return Patch0Model.decode_tsl(v)

    @validator("patch1", pre=True)
    def parse_patch1(cls, v: list[str]) -> JsonDict:
        return Patch1Model.decode_tsl(v)

    @validator("patch2", pre=True)
    def parse_patch2(cls, v: list[str]) -> JsonDict:
        return Patch2Model.decode_tsl(v)

    @validator("patch_mk2v2", pre=True)
    def parse_patch_mk2v2(cls, v: list[str]) -> JsonDict:
        return PatchMk2v2Model.decode_tsl(v)

    @validator("contour1", pre=True)
    def parse_contour1(cls, v: list[str]) -> JsonDict:
        return ContourModel.decode_tsl(v)

    @validator("contour2", pre=True)
    def parse_contour2(cls, v: list[str]) -> JsonDict:
        return ContourModel.decode_tsl(v)

    @validator("contour3", pre=True)
    def parse_contour3(cls, v: list[str]) -> JsonDict:
        return ContourModel.decode_tsl(v)

    @validator("eq2", pre=True)
    def parse_eq2(cls, v: list[str]) -> JsonDict:
        return EqModel.decode_tsl(v)


class MemoModel(TslBaseModel):
    memo: str
    is_tone_central_patch: bool = Field(alias="isToneCentralPatch")
    note: str | None


class PatchModel(TslBaseModel):
    memo: MemoModel | str | None
    param_set: ParamSetModel = Field(alias="paramSet")

    @classmethod
    def decode_tsl(cls, values: JsonDict) -> "PatchModel":
        return PatchModel(**values)


class TslModel(TslBaseModel):
    name: str
    format_rev: str = Field(alias="formatRev")
    device: str
    data: list[list[PatchModel]]

    @classmethod
    def decode_tsl(cls, values: JsonDict) -> "TslModel":
        for idx, entries in enumerate(values["data"]):
            values["data"][idx] = list(map(PatchModel.decode_tsl, entries))

        return TslModel(**values)

    @validator("device")
    def validate_device(cls, v: str) -> str:
        if v != "KATANA MkII":
            raise UnsupportedDeviceError(v)

        return v
