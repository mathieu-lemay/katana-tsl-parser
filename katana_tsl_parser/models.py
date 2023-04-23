from enum import Enum, IntEnum
from typing import Any, Callable, Generator

from pydantic import (
    BaseModel,
    ConstrainedFloat,
    ConstrainedInt,
    Extra,
    Field,
    validator,
)

JsonDict = dict[str, Any]


def i(n: str) -> int:
    return int(n, 16)


def q(v: str) -> float:
    return 2.0 ** (i(v) - 1)


def gain_12db(v: str) -> float:
    return (i(v) - 24) * 0.5


def gain_20db(v: str) -> int:
    return i(v) - 20


def pitch(v: str) -> int:
    return i(v) - 24


def decode_delay_time(values: list[str]) -> int:
    time = 0
    for v in values:
        time <<= 7
        time += i(v)

    return time


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


class Gain20dB(ConstrainedInt):
    ge = -20
    le = 20


class Pitch(ConstrainedInt):
    ge = -24
    le = 24


class ContourChoice(Enum):
    Off = 0
    Contour1 = 1
    Contour2 = 2
    Contour3 = 3


class Q(float):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[float], float], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: float) -> float:
        if not isinstance(v, float):
            raise TypeError("float required")

        if v not in (0.5, 1, 2, 4, 8, 16):
            raise ValueError("invalid Q value")

        return v


class TslBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        extra = Extra.forbid

    @classmethod
    def _get_fields(cls, by_alias: bool = False) -> set[str]:
        return set(cls.schema(by_alias=by_alias)["properties"].keys())


class AmpType(Enum):
    # Official
    Acoustic = 0x01
    Clean = 0x08
    Crunch = 0x0B
    Lead = 0x18
    Brown = 0x17
    # Variations
    AcousticVar = 0x1C
    CleanVar = 0x1D
    CrunchVar = 0x1E
    LeadVar = 0x1F
    BrownVar = 0x20
    # "Sneaky Amps"
    NaturalClean = 0x00
    CleanTwin = 0x09
    ComboCrunch = 0x02
    ProCrunch = 0x0A
    DeluxeCrunch = 0x0C
    StackCrunch = 0x03
    VODrive = 0x0D
    BGDrive = 0x11
    MatchDrive = 0x0F
    PowerDrive = 0x05
    VOLead = 0x0E
    BGLead = 0x10
    ExtremeLead = 0x06
    TAmpLead = 0x16
    MS1959I = 0x12
    MS1959I_II = 0x13
    HiGainStack = 0x04
    RFierVintage = 0x14
    RFierModern = 0x15
    CoreMetal = 0x07
    Custom = 0x19


class BoostType(Enum):
    MidBoost = 0x00
    CleanBoost = 0x01
    TrebleBoost = 0x02
    CrunchOD = 0x03
    NaturalOD = 0x04
    WarmOD = 0x05
    FatDS = 0x06
    MetalDS = 0x08
    OCTFuzz = 0x09
    BluesDrive = 0x0A
    Overdrive = 0x0B
    Tubescreamer = 0x0C
    TurboOD = 0x0D
    Distortion = 0x0E
    Rat = 0x0F
    GuVDS = 0x10
    DSTPlus = 0x11
    MetalZone = 0x12
    SixtiesFuzz = 0x13
    MuffFuzz = 0x14
    HM2 = 0x15
    MetalCore = 0x16
    CentaOD = 0x17


class ModFxType(Enum):
    TWah = 0x00
    AutoWah = 0x01
    PedalWah = 0x02
    Compressor = 0x03
    Limiter = 0x04
    GraphicEq = 0x06
    ParametricEq = 0x07
    GuitarSim = 0x09
    SlowGear = 0x0A
    WaveSynth = 0x0C
    Octave = 0x0E
    PitchShifter = 0x0F
    Harmonist = 0x10
    AcProcessor = 0x12
    Phaser = 0x13
    Flanger = 0x14
    Tremolo = 0x15
    Rotary = 0x16
    UniV = 0x17
    Slicer = 0x19
    Vibrato = 0x1A
    RingMod = 0x1B
    Humanizer = 0x1C
    Chorus = 0x1D
    AcGuitarSim = 0x1F
    Phaser90E = 0x23
    Flanger117E = 0x24
    Wah95E = 0x25
    DelayChorus30 = 0x26
    HeavyOctave = 0x27
    PedalBend = 0x28


class DelayType(Enum):
    Digital = 0x00
    Pan = 0x01
    Stereo = 0x02
    Reverse = 0x06
    Analog = 0x07
    TapeEcho = 0x08
    Modulate = 0x09
    SDE3000 = 0x0A


class ReverbType(IntEnum):
    Room = 0x01
    Hall = 0x03
    Plate = 0x04
    Spring = 0x05
    Modulate = 0x06


class ReverbMode(IntEnum):
    Delay = 0x00
    DelayReverb = 0x01
    Reverb = 0x02


class Range(IntEnum):
    KHz8 = 0x00
    KHz17 = 0x01


class Phase(IntEnum):
    Normal = 0x00
    Inverse = 0x01


class Light(Enum):
    Green = 0
    Red = 1
    Yellow = 2


class CabResonance(Enum):
    Vintage = 0
    Modern = 1
    Deep = 2


class EqPosition(Enum):
    AmpIn = 0
    AmpOut = 1


class LowCutFreq(Enum):
    Flat = 0
    Hz20 = 1
    Hz25 = 2
    Hz31_5 = 3
    Hz40 = 4
    Hz50 = 5
    Hz63 = 6
    Hz80 = 7
    Hz100 = 8
    Hz125 = 9
    Hz160 = 10
    Hz200 = 11
    Hz250 = 12
    Hz315 = 13
    Hz400 = 14
    Hz500 = 15
    Hz630 = 16
    Hz800 = 17


class MidFreq(IntEnum):
    def __new__(cls, value: int, description: str = "") -> "MidFreq":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore[attr-defined]

        return obj

    Hz20 = 0, "20.0 Hz"
    Hz25 = 1, "25.0 Hz"
    Hz31_5 = 2, "31.5 Hz"
    Hz40 = 3, "40.0 Hz"
    Hz50 = 4, "50.0 Hz"
    Hz63 = 5, "63.0 Hz"
    Hz80 = 6, "80.0 Hz"
    Hz100 = 7, "100 Hz"
    Hz125 = 8, "125 Hz"
    Hz160 = 9, "160 Hz"
    Hz200 = 10, "200 Hz"
    Hz250 = 11, "250 Hz"
    Hz315 = 12, "315 Hz"
    Hz400 = 13, "400 Hz"
    Hz500 = 14, "500 Hz"
    Hz630 = 15, "630 Hz"
    Hz800 = 16, "800 Hz"
    Hz1000 = 17, "1.00 kHz"
    Hz1250 = 18, "1.25 kHz"
    Hz1600 = 19, "1.60 kHz"
    Hz2000 = 20, "2.00 kHz"
    Hz2500 = 21, "2.50 kHz"
    Hz3150 = 22, "3.15 kHz"
    Hz4000 = 23, "4.00 kHz"
    Hz5000 = 24, "5.00 kHz"
    Hz6300 = 25, "6.30 kHz"
    Hz8000 = 26, "8.00 kHz"
    Hz10000 = 27, "10.0 kHz"


class HighCutFreq(Enum):
    Hz630 = 0
    Hz800 = 1
    Hz1000 = 2
    Hz1250 = 3
    Hz1600 = 4
    Hz2000 = 5
    Hz2500 = 6
    Hz3150 = 7
    Hz4000 = 8
    Hz5000 = 9
    Hz6300 = 10
    Hz8000 = 11
    Hz10000 = 12
    Hz12500 = 13
    Flat = 14


class CrossoverFreq(Enum):
    Hz100 = 0
    Hz125 = 1
    Hz160 = 2
    Hz200 = 3
    Hz250 = 4
    Hz315 = 5
    Hz400 = 6
    Hz500 = 7
    Hz630 = 8
    Hz800 = 9
    Hz1000 = 10
    Hz1250 = 11
    Hz1600 = 12
    Hz2000 = 13
    Hz2500 = 14
    Hz3150 = 15
    Hz4000 = 16


class EqType(Enum):
    Parametric = 0
    Graphic10 = 1


class PhaserType(Enum):
    Stage4 = 0
    Stage8 = 1
    Stage12 = 2
    BiPhase = 3


class RingModMode(Enum):
    Normal = 0
    Intelligent = 1


class CompressorType(Enum):
    BossComp = 0
    HiBand = 1
    Light = 2
    DComp = 3
    Orange = 4
    Fat = 5
    Mild = 6


class LimiterType(Enum):
    BossLimiter = 0
    Rack160D = 1
    VintageRackU = 2


class Ratio(IntEnum):
    def __new__(cls, value: int, description: str = "") -> "Ratio":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore[attr-defined]

        return obj

    def __repr__(self) -> str:
        return self.description  # type: ignore[attr-defined,no-any-return]

    R1 = 0, "1:1"
    R1_2 = 1, "1.2:1"
    R1_4 = 2, "1.4:1"
    R1_6 = 3, "1.6:1"
    R1_8 = 4, "1.8:1"
    R2 = 5, "2:1"
    R2_3 = 6, "2.3:1"
    R2_6 = 7, "2.6:1"
    R3 = 8, "3:1"
    R3_5 = 9, "3.5:1"
    R4 = 10, "4:1"
    R5 = 11, "5:1"
    R6 = 12, "6:1"
    R8 = 13, "8:1"
    R10 = 14, "10:1"
    R12 = 15, "12:1"
    R20 = 16, "20:1"
    RInf = 17, "Inf:1"


class WahMode(Enum):
    LPF = 0
    BPF = 1


class Polarity(Enum):
    Down = 0
    Up = 1


class PedalWahType(Enum):
    Cry = 0
    Vo = 1
    Fat = 2
    Light = 3
    SevenString = 4
    Reso = 5


class GuitarSimType(Enum):
    SingleToHumbucker = 0
    HumbuckerToSingle = 1
    HumbuckerToHalfTone = 2
    SingleToHollow = 3
    HumbuckerToHollow = 4
    SingleToAcoustic = 5
    HumbuckerToAcoustic = 6
    PiezoToAcoustic = 7


class AcProcessorType(Enum):
    Small = 0
    Medium = 1
    Bright = 2
    Power = 3


class WaveSynthType(Enum):
    Saw = 0
    Square = 1


class VoiceType(Enum):
    Voice1 = 0
    Voice2 = 1


class PitchShifterMode(Enum):
    Fast = 0
    Medium = 1
    Slow = 2
    Mono = 3


class Harmony(IntEnum):
    def __new__(cls, value: int, description: str = "") -> "Harmony":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore[attr-defined]

        return obj

    def __repr__(self) -> str:
        return self.description  # type: ignore[attr-defined,no-any-return]

    HMin2Oct = 0, "-2oct"
    HMin14th = 1, "-14th"
    HMin13th = 2, "-13th"
    HMin12th = 3, "-12th"
    HMin11th = 4, "-11th"
    HMin10th = 5, "-10th"
    HMin9th = 6, "-9th"
    HMin1Oct = 7, "-1oct"
    HMin7th = 8, "-7th"
    HMin6th = 9, "-6th"
    HMin5th = 10, "-5th"
    HMin4th = 11, "-4th"
    HMin3rd = 12, "-3rd"
    HMin2nd = 13, "-2nd"
    HMinUnison = 14, "Unison"
    HPlus2nd = 15, "+2nd"
    HPlus3rd = 16, "+3rd"
    HPlus4th = 17, "+4th"
    HPlus5th = 18, "+5th"
    HPlus6th = 19, "+6th"
    HPlus7th = 20, "+7th"
    HPlus1Oct = 21, "+1oct"
    HPlus9th = 22, "+9th"
    HPlus10th = 23, "+10th"
    HPlus11th = 24, "+11th"
    HPlus12th = 25, "+12th"
    HPlus13th = 26, "+13th"
    HPlus14th = 27, "+14th"
    HPlus2Oct = 28, "+2oct"
    HUser = 29, "User"


class Key(IntEnum):
    def __new__(cls, value: int, description: str = "") -> "Key":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description  # type: ignore[attr-defined]

        return obj

    def __repr__(self) -> str:
        return self.description  # type: ignore[attr-defined,no-any-return]

    C = 0, "C (Am)"
    Db = 1, "Db (Bbm)"
    D = 2, "D (Bm)"
    Eb = 3, "Eb (Cm)"
    E = 4, "E (C#m)"
    F = 5, "F (Dm)"
    Fs = 6, "F# (D#m)"
    G = 7, "G (Em)"
    Ab = 8, "Ab (Fm)"
    A = 9, "A (F#m)"
    Bb = 10, "Bb (Gm)"
    B = 11, "B (G#m)"


class HumanizerMode(Enum):
    Picking = 0
    Auto = 1


class Vowel(Enum):
    a = 0
    e = 1
    i = 2
    o = 3
    u = 4


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
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 24:
            raise ValueError("must contain exactly 24 items")

        return {
            "on": i(values[0]) > 0,
            "type_": EqType(i(values[1])),
            "low_cut": LowCutFreq(i(values[2])),
            "low_gain": gain_20db(values[3]),
            "low_mid_freq": MidFreq(i(values[4])),
            "low_mid_q": q(values[5]),
            "low_mid_gain": gain_20db(values[6]),
            "high_mid_freq": MidFreq(i(values[7])),
            "high_mid_q": q(values[8]),
            "high_mid_gain": gain_20db(values[9]),
            "high_gain": gain_20db(values[10]),
            "high_cut": HighCutFreq(i(values[11])),
            "level": gain_20db(values[12]),
            "bar_31": gain_12db(values[13]),
            "bar_62": gain_12db(values[14]),
            "bar_125": gain_12db(values[15]),
            "bar_250": gain_12db(values[16]),
            "bar_500": gain_12db(values[17]),
            "bar_1000": gain_12db(values[18]),
            "bar_2000": gain_12db(values[19]),
            "bar_4000": gain_12db(values[20]),
            "bar_8000": gain_12db(values[21]),
            "bar_16000": gain_12db(values[22]),
            "bar_level": gain_12db(values[23]),
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
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 72:
            raise ValueError("must contain exactly 72 items")

        res = {
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
            "eq": EqModel.decode(values[48:]),
        }

        return res


class PedalFxType(Enum):
    Wah = 0
    Bend = 1
    Wah95E = 2


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

    contour: ContourChoice

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) not in (50, 91):
            raise ValueError("must contain exactly 50 or 91 items, not %d" % len(values))

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
            "pedal_fx_bend_pitch": pitch(values[24]),
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

        if len(values) == 91:
            res.update(
                {
                    "solo_on": i(values[84]) > 0,
                    "solo_level": i(values[85]),
                }
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
                    raise ValueError(f"Invalid values for contour: ({x}, {y})")

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
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 36:
            raise ValueError("must contain exactly 36 items")

        res = {
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

        return res


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
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 10:
            raise ValueError(f"must contain exactly 10 items, not {len(values)}")

        res = {
            "solo_eq_position": i(values[0]),
            "solo_eq_on": i(values[1]) > 0,
            "solo_eq_low_cut": LowCutFreq(i(values[2])),
            "solo_eq_low_gain": gain_12db(values[3]),
            "solo_eq_mid_freq": MidFreq(i(values[4])),
            "solo_eq_mid_q": q(values[5]),
            "solo_eq_mid_gain": gain_12db(values[6]),
            "solo_eq_high_gain": gain_12db(values[7]),
            "solo_eq_high_cut": HighCutFreq(i(values[8])),
            "solo_eq_level": gain_12db(values[9]),
        }

        return res


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
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 26:
            raise ValueError(f"must contain exactly 26 items, not {len(values)}")

        res = {
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

        return res


class ContourModel(TslBaseModel):
    contour_type: int
    freq_shift: int

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 2:
            raise ValueError(f"must contain exactly 2 items, not {len(values)}")

        res = {
            "contour_type": i(values[0]) + 1,
            "freq_shift": i(values[1]) - 50,
        }

        return res


class TWahModel(TslBaseModel):
    mode: WahMode
    polarity: Polarity
    sens: Percent
    frequency: Percent
    peak: Percent
    direct_mix: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "mode": i(values[0]),
            "polarity": i(values[1]),
            "sens": i(values[2]),
            "frequency": i(values[3]),
            "peak": i(values[4]),
            "direct_mix": i(values[5]),
            "level": i(values[6]),
        }

        return res


class AutoWahModel(TslBaseModel):
    mode: WahMode
    frequency: Percent
    peak: Percent
    rate: Percent
    depth: Percent
    direct_mix: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "mode": i(values[0]),
            "frequency": i(values[1]),
            "peak": i(values[2]),
            "rate": i(values[3]),
            "depth": i(values[4]),
            "direct_mix": i(values[5]),
            "level": i(values[6]),
        }

        return res


class PedalWahModel(TslBaseModel):
    type_: PedalWahType
    pedal_pos: Percent
    pedal_min: Percent
    pedal_max: Percent
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "pedal_pos": i(values[1]),
            "pedal_min": i(values[2]),
            "pedal_max": i(values[3]),
            "level": i(values[4]),
            "direct_mix": i(values[5]),
        }

        return res


class CompressorModel(TslBaseModel):
    type_: CompressorType
    sustain: Percent
    attack: Percent
    tone: int
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": CompressorType(i(values[0])),
            "sustain": i(values[1]),
            "attack": i(values[2]),
            "tone": i(values[3]) - 50,
            "level": i(values[4]),
        }

        return res


class LimiterModel(TslBaseModel):
    type_: LimiterType
    attack: Percent
    threshold: Percent
    ratio: Ratio
    release: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": LimiterType(i(values[0])),
            "attack": i(values[1]),
            "threshold": i(values[2]),
            "ratio": Ratio(i(values[3])),
            "release": i(values[4]),
            "level": i(values[5]),
        }

        return res


class GraphicEqModel(TslBaseModel):
    bar_31: Gain20dB
    bar_62: Gain20dB
    bar_125: Gain20dB
    bar_250: Gain20dB
    bar_500: Gain20dB
    bar_1000: Gain20dB
    bar_2000: Gain20dB
    bar_4000: Gain20dB
    bar_8000: Gain20dB
    bar_16000: Gain20dB
    bar_level: Gain20dB

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "bar_31": gain_20db(values[0]),
            "bar_62": gain_20db(values[1]),
            "bar_125": gain_20db(values[2]),
            "bar_250": gain_20db(values[3]),
            "bar_500": gain_20db(values[4]),
            "bar_1000": gain_20db(values[5]),
            "bar_2000": gain_20db(values[6]),
            "bar_4000": gain_20db(values[7]),
            "bar_8000": gain_20db(values[8]),
            "bar_16000": gain_20db(values[9]),
            "bar_level": gain_20db(values[10]),
        }

        return res


class ParametricEqModel(TslBaseModel):
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

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "low_cut": i(values[0]),
            "low_gain": gain_20db(values[1]),
            "low_mid_freq": i(values[2]),
            "low_mid_q": q(values[3]),
            "low_mid_gain": gain_20db(values[4]),
            "high_mid_freq": i(values[5]),
            "high_mid_q": q(values[6]),
            "high_mid_gain": gain_20db(values[7]),
            "high_gain": gain_20db(values[8]),
            "high_cut": i(values[9]),
            "level": gain_20db(values[10]),
        }

        return res


class GuitarSimModel(TslBaseModel):
    type_: GuitarSimType
    low: int = Field(ge=-50, le=50)
    high: int = Field(ge=-50, le=50)
    level: Percent
    body: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "low": i(values[1]) - 50,
            "high": i(values[2]) - 50,
            "level": i(values[3]),
            "body": i(values[4]),
        }

        return res


class SlowGearModel(TslBaseModel):
    sens: Percent
    rise_time: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "sens": i(values[0]),
            "rise_time": i(values[1]),
            "level": i(values[2]),
        }

        return res


class WaveSynthModel(TslBaseModel):
    type_: WaveSynthType
    cutoff: Percent
    resonance: Percent
    level: Percent
    filter_sens: Percent
    filter_decay: Percent
    filter_depth: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "cutoff": i(values[1]),
            "resonance": i(values[2]),
            "filter_sens": i(values[3]),
            "filter_decay": i(values[4]),
            "filter_depth": i(values[5]),
            "level": i(values[6]),
            "direct_mix": i(values[7]),
        }

        return res


class OctaveModel(TslBaseModel):
    range_: int = Field(ge=1, le=4)
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "range_": i(values[0]) + 1,
            "level": i(values[1]),
            "direct_mix": i(values[2]),
        }

        return res


class PitchShifterModel(TslBaseModel):
    voice: VoiceType
    ps1_mode: PitchShifterMode
    ps1_pitch: Pitch
    ps1_fine: int = Field(ge=-50, le=50)
    ps1_pre_delay: int = Field(ge=0, le=300)
    ps1_level: Percent
    ps1_feedback: Percent
    ps2_mode: PitchShifterMode
    ps2_pitch: Pitch
    ps2_fine: int = Field(ge=-50, le=50)
    ps2_pre_delay: int = Field(ge=0, le=300)
    ps2_level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 15:
            raise ValueError(f"must contain exactly 15 items, not {len(values)}")

        res = {
            "voice": i(values[0]),
            "ps1_mode": i(values[1]),
            "ps1_pitch": pitch(values[2]),
            "ps1_fine": i(values[3]) - 50,
            "ps1_pre_delay": decode_delay_time(values[4:6]),
            "ps1_level": i(values[6]),
            "ps2_mode": i(values[7]),
            "ps2_pitch": pitch(values[8]),
            "ps2_fine": i(values[9]) - 50,
            "ps2_pre_delay": decode_delay_time(values[10:12]),
            "ps2_level": i(values[12]),
            "ps1_feedback": i(values[13]),
            "direct_mix": i(values[14]),
        }

        return res


class HarmonistUserSettings(TslBaseModel):
    e: Pitch
    f: Pitch
    f_sharp: Pitch
    g: Pitch
    a_flat: Pitch
    a: Pitch
    b_flat: Pitch
    b: Pitch
    c: Pitch
    d_flat: Pitch
    d: Pitch
    e_flat: Pitch

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "e": pitch(values[0]),
            "f": pitch(values[1]),
            "f_sharp": pitch(values[2]),
            "g": pitch(values[3]),
            "a_flat": pitch(values[4]),
            "a": pitch(values[5]),
            "b_flat": pitch(values[6]),
            "b": pitch(values[7]),
            "c": pitch(values[8]),
            "d_flat": pitch(values[9]),
            "d": pitch(values[10]),
            "e_flat": pitch(values[11]),
        }

        return res


class HarmonistModel(TslBaseModel):
    voice: VoiceType
    hr1_mode: Harmony
    hr1_level: Percent
    hr1_pre_delay: int = Field(ge=0, le=300)
    hr1_feedback: Percent
    hr2_mode: Harmony
    hr2_level: Percent
    hr2_pre_delay: int = Field(ge=0, le=300)
    direct_mix: Percent
    hr1_user: HarmonistUserSettings
    hr2_user: HarmonistUserSettings

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 35:
            raise ValueError(f"must contain exactly 35 items, not {len(values)}")

        res = {
            "voice": i(values[0]),
            "hr1_mode": Harmony(i(values[1])),
            "hr1_pre_delay": decode_delay_time(values[2:4]),
            "hr1_level": i(values[4]),
            "hr2_mode": Harmony(i(values[5])),
            "hr2_pre_delay": decode_delay_time(values[6:8]),
            "hr2_level": i(values[8]),
            "hr1_feedback": i(values[9]),
            "direct_mix": i(values[10]),
            "hr1_user": HarmonistUserSettings.decode(values[11:23]),
            "hr2_user": HarmonistUserSettings.decode(values[23:35]),
        }

        return res


class AcProcessorModel(TslBaseModel):
    type_: AcProcessorType
    bass: int = Field(ge=-50, le=50)
    middle: int = Field(ge=-50, le=50)
    middle_freq: MidFreq
    treble: int = Field(ge=-50, le=50)
    presence: int = Field(ge=-50, le=50)
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "bass": i(values[1]) - 50,
            "middle": i(values[2]) - 50,
            "middle_freq": i(values[3]),
            "treble": i(values[4]) - 50,
            "presence": i(values[5]) - 50,
            "level": i(values[6]),
        }

        return res


class PhaserModel(TslBaseModel):
    type_: PhaserType
    rate: Percent
    depth: Percent
    manual: Percent
    resonance: Percent
    step_rate: ToggleablePercent
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "rate": i(values[1]),
            "depth": i(values[2]),
            "manual": i(values[3]),
            "resonance": i(values[4]),
            "step_rate": ToggleablePercent(i(values[5])),
            "direct_mix": i(values[6]),
            "level": i(values[7]),
        }

        return res


class FlangerModel(TslBaseModel):
    rate: Percent
    depth: Percent
    manual: Percent
    resonance: Percent
    low_cut: LowCutFreq
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "rate": i(values[0]),
            "depth": i(values[1]),
            "manual": i(values[2]),
            "resonance": i(values[3]),
            "low_cut": LowCutFreq(i(values[4])),
            "direct_mix": i(values[5]),
            "level": i(values[6]),
        }

        return res


class TremoloModel(TslBaseModel):
    wave_shape: Percent
    rate: Percent
    depth: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "wave_shape": i(values[0]),
            "rate": i(values[1]),
            "depth": i(values[2]),
            "level": i(values[3]),
        }

        return res


class RotaryModel(TslBaseModel):
    rate: Percent
    depth: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 5:
            raise ValueError(f"must contain exactly 5 items, not {len(values)}")

        res = {
            "rate": i(values[0]),
            "depth": i(values[3]),
            "level": i(values[4]),
        }

        return res


class UniVModel(TslBaseModel):
    rate: Percent
    depth: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "rate": i(values[0]),
            "depth": i(values[1]),
            "level": i(values[2]),
        }

        return res


class SlicerModel(TslBaseModel):
    pattern: int = Field(ge=1, le=20)
    rate: Percent
    trigger_sens: Percent
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "pattern": i(values[0]) + 1,
            "rate": i(values[1]),
            "trigger_sens": i(values[2]),
            "level": i(values[3]),
            "direct_mix": i(values[4]),
        }

        return res


class VibratoModel(TslBaseModel):
    rate: Percent
    depth: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 5:
            raise ValueError(f"must contain exactly 5 items, not {len(values)}")

        res = {
            "rate": i(values[0]),
            "depth": i(values[1]),
            "level": i(values[4]),
        }

        return res


class RingModModel(TslBaseModel):
    type_: RingModMode
    frequency: Percent
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "frequency": i(values[1]),
            "level": i(values[2]),
            "direct_mix": i(values[3]),
        }

        return res


class HumanizerModel(TslBaseModel):
    mode: HumanizerMode
    vowel1: Vowel
    vowel2: Vowel
    rate: Percent
    depth: Percent
    sens: Percent
    manual: Percent
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "mode": i(values[0]),
            "vowel1": i(values[1]),
            "vowel2": i(values[2]),
            "sens": i(values[3]),
            "rate": i(values[4]),
            "depth": i(values[5]),
            "manual": i(values[6]),
            "level": i(values[7]),
        }

        return res


class ChorusModel(TslBaseModel):
    crossover_frequency: CrossoverFreq
    low_rate: Percent
    low_depth: Percent
    low_pre_delay: float = Field(ge=0, le=40, multiple_of=0.5)
    low_level: Percent
    high_rate: Percent
    high_depth: Percent
    high_pre_delay: float = Field(ge=0, le=40, multiple_of=0.5)
    high_level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "crossover_frequency": i(values[0]),
            "low_rate": i(values[1]),
            "low_depth": i(values[2]),
            "low_pre_delay": i(values[3]) * 0.5,
            "low_level": i(values[4]),
            "high_rate": i(values[5]),
            "high_depth": i(values[6]),
            "high_pre_delay": i(values[7]) * 0.5,
            "high_level": i(values[8]),
            "direct_mix": i(values[9]),
        }

        return res


class AcGuitarSimModel(TslBaseModel):
    body: Percent
    low: int = Field(ge=-50, le=50)
    high: int = Field(ge=-50, le=50)
    level: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 5:
            raise ValueError(f"must contain exactly 5 items, not {len(values)}")

        res = {
            "high": i(values[0]) - 50,
            "body": i(values[1]),
            "low": i(values[2]) - 50,
            "level": i(values[4]),
        }

        return res


class Phaser90EModel(TslBaseModel):
    script_on: bool
    speed: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "script_on": i(values[0]) > 0,
            "speed": i(values[1]),
        }

        return res


class Flanger117EModel(TslBaseModel):
    manual: Percent
    width: Percent
    speed: Percent
    regen: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "manual": i(values[0]),
            "width": i(values[1]),
            "speed": i(values[2]),
            "regen": i(values[3]),
        }

        return res


class Wah95EModel(TslBaseModel):
    pedal_pos: Percent
    pedal_min: Percent
    pedal_max: Percent
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "pedal_pos": i(values[0]),
            "pedal_min": i(values[1]),
            "pedal_max": i(values[2]),
            "level": i(values[3]),
            "direct_mix": i(values[4]),
        }

        return res


class DelayChorusType(Enum):
    Chorus = 0
    Echo = 1


class DelayChorusOutput(Enum):
    DAndE = 0
    DOverE = 1


class DelayChorus30Model(TslBaseModel):
    type_: DelayChorusType
    chorus_intensity: Percent
    echo_repeat_rate: int = Field(ge=0, le=600)
    echo_intensity: Percent
    echo_volume: Percent
    input_volume: Percent
    tone: Percent
    output: DelayChorusOutput

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()) + 1:
            raise ValueError(f"must contain exactly {len(cls._get_fields()) + 1} items, not {len(values)}")

        res = {
            "type_": i(values[0]),
            "chorus_intensity": i(values[2]),
            "echo_repeat_rate": decode_delay_time(values[3:5]),
            "echo_intensity": i(values[5]),
            "echo_volume": i(values[6]),
            "tone": i(values[7]),
            "input_volume": i(values[1]),
            "output": i(values[8]),
        }

        return res


class HeavyOctaveModel(TslBaseModel):
    level_1_oct: Percent
    level_2_oct: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "level_1_oct": i(values[0]),
            "level_2_oct": i(values[1]),
            "direct_mix": i(values[2]),
        }

        return res


class PedalBendModel(TslBaseModel):
    pedal_pos: Percent
    pitch: Pitch
    level: Percent
    direct_mix: Percent

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != len(cls._get_fields()):
            raise ValueError(f"must contain exactly {len(cls._get_fields())} items, not {len(values)}")

        res = {
            "pitch": pitch(values[0]),
            "pedal_pos": i(values[1]),
            "level": i(values[2]),
            "direct_mix": i(values[3]),
        }

        return res


class FxModel(TslBaseModel):
    on: bool
    type_: ModFxType
    t_wah: TWahModel
    auto_wah: AutoWahModel
    pedal_wah: PedalWahModel
    compressor: CompressorModel
    limiter: LimiterModel
    graphic_eq: GraphicEqModel
    parametric_eq: ParametricEqModel
    guitar_sim: GuitarSimModel
    slow_gear: SlowGearModel
    wave_synth: WaveSynthModel
    octave: OctaveModel
    pitch_shifter: PitchShifterModel
    harmonist: HarmonistModel
    ac_processor: AcProcessorModel
    phaser: PhaserModel
    flanger: FlangerModel
    tremolo: TremoloModel
    rotary: RotaryModel
    uni_v: UniVModel
    slicer: SlicerModel
    vibrato: VibratoModel
    ring_mod: RingModModel
    humanizer: HumanizerModel
    chorus: ChorusModel
    ac_guitar_sim: AcGuitarSimModel
    phaser_90e: Phaser90EModel
    flanger_117e: Flanger117EModel
    wah_95e: Wah95EModel
    dc30: DelayChorus30Model
    heavy_octave: HeavyOctaveModel
    pedal_bend: PedalBendModel

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) != 225:
            raise ValueError(f"must contain exactly 225 items, not {len(values)}")

        res = {
            "on": i(values[0]) > 0,
            "type_": ModFxType(i(values[1])),
            "t_wah": TWahModel.decode(values[2:9]),
            "auto_wah": AutoWahModel.decode(values[9:16]),
            "pedal_wah": PedalWahModel.decode(values[16:22]),
            "compressor": CompressorModel.decode(values[22:27]),
            "limiter": LimiterModel.decode(values[27:33]),
            "graphic_eq": GraphicEqModel.decode(values[33:44]),
            "parametric_eq": ParametricEqModel.decode(values[44:55]),
            "guitar_sim": GuitarSimModel.decode(values[55:60]),
            "slow_gear": SlowGearModel.decode(values[60:63]),
            "wave_synth": WaveSynthModel.decode(values[63:71]),
            "octave": OctaveModel.decode(values[71:74]),
            "pitch_shifter": PitchShifterModel.decode(values[74:89]),
            "harmonist": HarmonistModel.decode(values[89:124]),
            "ac_processor": AcProcessorModel.decode(values[124:131]),
            "phaser": PhaserModel.decode(values[131:139]),
            "flanger": FlangerModel.decode(values[139:146]),
            # TODO: 146
            "tremolo": TremoloModel.decode(values[147:151]),
            # TODO: 151-152
            "rotary": RotaryModel.decode(values[153:158]),
            "uni_v": UniVModel.decode(values[158:161]),
            "slicer": SlicerModel.decode(values[161:166]),
            "vibrato": VibratoModel.decode(values[166:171]),
            "ring_mod": RingModModel.decode(values[171:175]),
            "humanizer": HumanizerModel.decode(values[175:183]),
            "chorus": ChorusModel.decode(values[183:193]),
            "ac_guitar_sim": AcGuitarSimModel.decode(values[193:198]),
            "phaser_90e": Phaser90EModel.decode(values[198:200]),
            "flanger_117e": Flanger117EModel.decode(values[200:204]),
            "wah_95e": Wah95EModel.decode(values[204:209]),
            "dc30": DelayChorus30Model.decode(values[209:218]),
            "heavy_octave": HeavyOctaveModel.decode(values[218:221]),
            "pedal_bend": PedalBendModel.decode(values[221:]),
        }

        return res


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
    # expression_pedal_assign: list[str] = Field(alias="UserPatch%ExpPedalAsgn")  # noqa: ERA001
    # expression_pedal_min_max: list[str] = Field(alias="UserPatch%ExpPedalAsgnMinMax")  # noqa: ERA001
    # gafc_expression1_assign: list[str] = Field(alias="UserPatch%GafcExp1Asgn")  # noqa: ERA001
    # gafc_expression1_min_max: list[str] = Field(alias="UserPatch%GafcExp1AsgnMinMax")  # noqa: ERA001
    # gafc_expression2_assign: list[str] = Field(alias="UserPatch%GafcExp2Asgn")  # noqa: ERA001
    # gafc_expression2_min_max: list[str] = Field(alias="UserPatch%GafcExp2AsgnMinMax")  # noqa: ERA001
    # footswitch_assign: list[str] | None = Field(alias="UserPatch%FsAsgn")  # noqa: ERA001
    patch_mk2v2: PatchMk2v2Model | None = Field(alias="UserPatch%Patch_Mk2V2")
    contour1: ContourModel | None = Field(alias="UserPatch%Contour(1)")
    contour2: ContourModel | None = Field(alias="UserPatch%Contour(2)")
    contour3: ContourModel | None = Field(alias="UserPatch%Contour(3)")
    eq2: EqModel = Field(alias="UserPatch%Eq(2)")

    @validator("name", pre=True)
    def validate_name(cls, v: str | list[str]) -> str:  # noqa: N805
        if isinstance(v, list):
            v = "".join([chr(int(i, 16)) for i in v])

        if len(v) > 16:
            raise ValueError("must be 16 chars or fewer")

        return v.rstrip()

    @validator("fx1", pre=True)
    def parse_fx1(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return FxModel.decode(v)

    @validator("fx2", pre=True)
    def parse_fx2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return FxModel.decode(v)

    @validator("delay1", pre=True)
    def parse_delay1(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return DelayModel.decode(v)

    @validator("delay2", pre=True)
    def parse_delay2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return DelayModel.decode(v)

    @validator("patch0", pre=True)
    def parse_patch0(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch0Model.decode(v)

    @validator("patch1", pre=True)
    def parse_patch1(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch1Model.decode(v)

    @validator("patch2", pre=True)
    def parse_patch2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return Patch2Model.decode(v)

    @validator("patch_mk2v2", pre=True)
    def parse_patch_mk2v2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return PatchMk2v2Model.decode(v)

    @validator("contour1", pre=True)
    def parse_contour1(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return ContourModel.decode(v)

    @validator("contour2", pre=True)
    def parse_contour2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return ContourModel.decode(v)

    @validator("contour3", pre=True)
    def parse_contour3(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return ContourModel.decode(v)

    @validator("eq2", pre=True)
    def parse_eq2(cls, v: list[str]) -> JsonDict:  # noqa: N805
        return EqModel.decode(v)


class MemoModel(TslBaseModel):
    memo: str
    is_tone_central_patch: bool = Field(alias="isToneCentralPatch")
    note: str | None


class PatchModel(TslBaseModel):
    memo: MemoModel | str
    param_set: ParamSetModel = Field(alias="paramSet")


class TslModel(TslBaseModel):
    name: str
    format_rev: str = Field(alias="formatRev")
    device: str
    data: list[list[PatchModel]]

    @validator("device")
    def validate_device(cls, v: str) -> str:  # noqa: N805
        if v != "KATANA MkII":
            raise ValueError(f"Unsupported device: {v}")

        return v
