from pydantic import Field

from .enums import (
    AcProcessorType,
    CompressorType,
    CrossoverFreq,
    DelayChorusOutput,
    DelayChorusType,
    GuitarSimType,
    Harmony,
    HighCutFreq,
    HumanizerMode,
    LimiterType,
    LowCutFreq,
    MidFreq,
    ModFxType,
    PedalWahType,
    PhaserType,
    PitchShifterMode,
    Polarity,
    Ratio,
    RingModMode,
    VoiceType,
    Vowel,
    WahMode,
    WaveSynthType,
)
from .types import (
    Gain20dB,
    JsonDict,
    Percent,
    Pitch,
    Q,
    ToggleablePercent,
    TslBaseModel,
    decode_delay_time,
    i,
)


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
            "bar_31": Gain20dB.parse(values[0]),
            "bar_62": Gain20dB.parse(values[1]),
            "bar_125": Gain20dB.parse(values[2]),
            "bar_250": Gain20dB.parse(values[3]),
            "bar_500": Gain20dB.parse(values[4]),
            "bar_1000": Gain20dB.parse(values[5]),
            "bar_2000": Gain20dB.parse(values[6]),
            "bar_4000": Gain20dB.parse(values[7]),
            "bar_8000": Gain20dB.parse(values[8]),
            "bar_16000": Gain20dB.parse(values[9]),
            "bar_level": Gain20dB.parse(values[10]),
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
            "low_gain": Gain20dB.parse(values[1]),
            "low_mid_freq": i(values[2]),
            "low_mid_q": Q.parse(values[3]),
            "low_mid_gain": Gain20dB.parse(values[4]),
            "high_mid_freq": i(values[5]),
            "high_mid_q": Q.parse(values[6]),
            "high_mid_gain": Gain20dB.parse(values[7]),
            "high_gain": Gain20dB.parse(values[8]),
            "high_cut": i(values[9]),
            "level": Gain20dB.parse(values[10]),
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
            "ps1_pitch": Pitch.parse(values[2]),
            "ps1_fine": i(values[3]) - 50,
            "ps1_pre_delay": decode_delay_time(values[4:6]),
            "ps1_level": i(values[6]),
            "ps2_mode": i(values[7]),
            "ps2_pitch": Pitch.parse(values[8]),
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
            "e": Pitch.parse(values[0]),
            "f": Pitch.parse(values[1]),
            "f_sharp": Pitch.parse(values[2]),
            "g": Pitch.parse(values[3]),
            "a_flat": Pitch.parse(values[4]),
            "a": Pitch.parse(values[5]),
            "b_flat": Pitch.parse(values[6]),
            "b": Pitch.parse(values[7]),
            "c": Pitch.parse(values[8]),
            "d_flat": Pitch.parse(values[9]),
            "d": Pitch.parse(values[10]),
            "e_flat": Pitch.parse(values[11]),
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
            "pitch": Pitch.parse(values[0]),
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
    pedal_bend: PedalBendModel | None

    @classmethod
    def decode(cls, values: list[str]) -> JsonDict:
        if len(values) not in (221, 225):
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
        }

        if len(values) == 225:
            res["pedal_bend"] = PedalBendModel.decode(values[221:])

        return res
