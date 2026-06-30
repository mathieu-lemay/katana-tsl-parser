from enum import Enum
from typing import TYPE_CHECKING

from rich.console import Console
from rich.table import Table

from katana_tsl_parser.models.enums import EqType, ModFxType, PedalFxType
from katana_tsl_parser.models.mod_fx import FxModel
from katana_tsl_parser.models.tsl import (
    DelayModel,
    EqModel,
    Patch0Model,
    Patch1Model,
    PatchModel,
)

if TYPE_CHECKING:
    from katana_tsl_parser.models.types import TslObject


def print_patch(idx: int, patch: PatchModel) -> None:
    params = patch.param_set

    t = Table(title=f"Patch {idx}: {params.name}", show_lines=True, show_header=False)
    t.add_row("Amp", format_amp(params.patch0))
    t.add_row("Boost", format_boost(params.patch0))
    t.add_row("Mod", format_fx(params.fx1))
    t.add_row("FX", format_fx(params.fx2))
    t.add_row("Delay", format_delay(params.delay1))
    t.add_row("Delay 2", format_delay(params.delay2))
    t.add_row("Reverb", format_reverb(params.patch1))
    t.add_row("Cabinet", format_cabinet())
    t.add_row("Pedal FX", format_pedal_fx(params.patch1))
    t.add_row("EQ1", format_eq(params.patch0.eq))
    t.add_row("EQ2", format_eq(params.eq2))
    t.add_row("Noise Gate", format_noise_gate(params.patch1))
    t.add_row("Send/Return", format_send_return(params.patch1))

    c = Console()
    c.print(t)


def format_amp(patch: Patch0Model) -> Table:
    t = Table(show_header=False, box=None)
    t.add_row("Model", patch.amp_type.name)
    t.add_row("Gain", str(patch.amp_gain))
    t.add_row("Volume", str(patch.amp_volume))
    t.add_row("Bass", str(patch.amp_eq_bass))
    t.add_row("Middle", str(patch.amp_eq_middle))
    t.add_row("Treble", str(patch.amp_eq_treble))
    t.add_row("Presence", str(patch.amp_eq_presence))
    return t


def format_boost(patch: Patch0Model) -> Table:
    t = _data_table()

    if not patch.boost_on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Type", patch.boost_type.name)
    t.add_row("Level", str(patch.boost_level))
    t.add_row("Drive", str(patch.boost_drive))
    t.add_row("Bottom", str(patch.boost_bottom))
    t.add_row("Tone", str(patch.boost_tone))
    t.add_row("Direct Mix", str(patch.boost_direct_mix))
    t.add_row("Solo", str(patch.boost_solo_on))
    t.add_row("Solo Level", str(patch.boost_solo_level))

    return t


# C901: Too complex (>10)
# PLR0912: Too many branches (>12)
# PLR0915: Too many statements (>50)
def format_fx(fx: FxModel) -> Table:  # noqa: C901, PLR0912, PLR0915
    t = _data_table()
    if not fx.on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Effect", fx.type_.name)

    values: TslObject | None
    match fx.type_:
        case ModFxType.TWah:
            values = fx.touch_wah
        case ModFxType.AutoWah:
            values = fx.auto_wah
        case ModFxType.PedalWah:
            values = fx.pedal_wah
        case ModFxType.Compressor:
            values = fx.compressor
        case ModFxType.Limiter:
            values = fx.limiter
        case ModFxType.GraphicEq:
            values = fx.graphic_eq
        case ModFxType.ParametricEq:
            values = fx.parametric_eq
        case ModFxType.GuitarSim:
            values = fx.guitar_sim
        case ModFxType.SlowGear:
            values = fx.slow_gear
        case ModFxType.WaveSynth:
            values = fx.wave_synth
        case ModFxType.Octave:
            values = fx.octave
        case ModFxType.PitchShifter:
            values = fx.pitch_shifter
        case ModFxType.Harmonist:
            values = fx.harmonist
        case ModFxType.AcProcessor:
            values = fx.ac_processor
        case ModFxType.Phaser:
            values = fx.phaser
        case ModFxType.Flanger:
            values = fx.flanger
        case ModFxType.Tremolo:
            values = fx.tremolo
        case ModFxType.Rotary:
            values = fx.rotary
        case ModFxType.UniV:
            values = fx.univibe
        case ModFxType.Slicer:
            values = fx.slicer
        case ModFxType.Vibrato:
            values = fx.vibrato
        case ModFxType.RingMod:
            values = fx.ring_mod
        case ModFxType.Humanizer:
            values = fx.humanizer
        case ModFxType.Chorus:
            values = fx.chorus
        case ModFxType.AcousticGuitarSim:
            values = fx.ac_guitar_sim
        case ModFxType.Phaser90E:
            values = fx.phaser_90e
        case ModFxType.Flanger117E:
            values = fx.flanger_117e
        case ModFxType.Wah95E:
            values = fx.wah_95e
        case ModFxType.DelayChorus30:
            values = fx.delay_chorus_30
        case ModFxType.HeavyOctave:
            values = fx.heavy_octave
        case ModFxType.PedalBend:
            values = fx.pedal_bend

    if values is None:
        return t

    for k, v in values.model_dump().items():
        param_name = k.replace("_", " ").strip().title()
        match v:
            case Enum():
                param_value = v.name
            case _:
                param_value = str(v)

        t.add_row(param_name, param_value)

    return t


def format_delay(delay: DelayModel) -> Table:
    t = _data_table()

    if not delay.delay_on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Type", delay.delay_type.name)
    t.add_row("Time", f"{delay.delay_time}ms")
    t.add_row("Feedback", str(delay.feedback))
    t.add_row("High Cut", str(delay.high_cut.name))
    t.add_row("Effect Level", str(delay.effect_level))
    t.add_row("Direct Mix", str(delay.direct_mix))
    t.add_row("Tap Time", str(delay.tap_time))
    t.add_row("Mod Rate", str(delay.mod_rate))
    t.add_row("Mod Depth", str(delay.mod_depth))
    t.add_row("Filter On", str(delay.filter_on))
    t.add_row("Range", str(delay.range_.name))
    t.add_row("Feedback Phase", str(delay.feedback_phase.name))
    t.add_row("Delay Phase", str(delay.delay_phase.name))
    t.add_row("Mod Switch On", str(delay.mod_sw_on))

    return t


def format_reverb(patch: Patch1Model) -> Table:
    t = _data_table()

    if not patch.reverb_on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Type", str(patch.reverb_type.name))
    t.add_row("Time", f"{patch.reverb_time}s")
    t.add_row("Pre Delay", f"{patch.reverb_pre_delay}ms")
    t.add_row("Low Cut", str(patch.reverb_low_cut.name))
    t.add_row("High Cut", str(patch.reverb_high_cut.name))
    t.add_row("Density", str(patch.reverb_density))
    t.add_row("Effect Level", str(patch.reverb_effect_level))
    t.add_row("Direct Mix", str(patch.reverb_direct_mix))
    t.add_row("Color", str(patch.reverb_color))

    return t


def format_cabinet() -> Table:
    t = _data_table()

    t.add_row("TODO", style="bold")

    return t


def format_pedal_fx(patch: Patch1Model) -> Table:
    t = _data_table()

    t.add_row("Type", patch.pedal_fx_type.name)

    match patch.pedal_fx_type:
        case PedalFxType.Wah:
            t.add_row("Wah Type", patch.pedal_fx_wah_type.name)
            t.add_row("Wah Position", str(patch.pedal_fx_wah_pos))
            t.add_row("Wah Min", str(patch.pedal_fx_wah_min))
            t.add_row("Wah Max", str(patch.pedal_fx_wah_max))
            t.add_row("Wah Level", str(patch.pedal_fx_wah_level))
            t.add_row("Wah Direct Mix", str(patch.pedal_fx_wah_direct_mix))
        case PedalFxType.Bend:
            t.add_row("Bend Position", str(patch.pedal_fx_bend_pos))
            t.add_row("Bend Pitch", str(patch.pedal_fx_bend_pitch))
            t.add_row("Bend Level", str(patch.pedal_fx_bend_level))
            t.add_row("Bend Direct Mix", str(patch.pedal_fx_bend_direct_mix))
        case PedalFxType.Wah95E:
            t.add_row("Wah95 Position", str(patch.pedal_fx_wah95_pos))
            t.add_row("Wah95 Min", str(patch.pedal_fx_wah95_min))
            t.add_row("Wah95 Max", str(patch.pedal_fx_wah95_max))
            t.add_row("Wah95 Level", str(patch.pedal_fx_wah95_level))
            t.add_row("Wah95 Direct Mix", str(patch.pedal_fx_wah95_direct_mix))

    return t


def format_eq(eq: EqModel) -> Table:
    t = _data_table()
    if not eq.on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Type", str(eq.type_.name))

    match eq.type_:
        case EqType.Graphic10:
            t.add_row("31 Hz", f"{eq.bar_31} dB")
            t.add_row("62 Hz", f"{eq.bar_62} dB")
            t.add_row("125 Hz", f"{eq.bar_125} dB")
            t.add_row("250 Hz", f"{eq.bar_250} dB")
            t.add_row("500 Hz", f"{eq.bar_500} dB")
            t.add_row("1 kHz", f"{eq.bar_1000} dB")
            t.add_row("2 kHz", f"{eq.bar_2000} dB")
            t.add_row("4 kHz", f"{eq.bar_4000} dB")
            t.add_row("8 kHz", f"{eq.bar_8000} dB")
            t.add_row("16 kHz", f"{eq.bar_16000} dB")
            t.add_row("Level", f"{eq.bar_level} dB")
        case EqType.Parametric:
            t.add_row("Low Cut", f"{eq.low_cut} Hz")
            t.add_row("Low Gain", f"{eq.low_gain} dB")
            t.add_row("Low Mid Freq", f"{eq.low_mid_freq} Hz")
            t.add_row("Low Mid Q", str(eq.low_mid_q))
            t.add_row("Low Mid Gain", f"{eq.low_mid_gain} dB")
            t.add_row("High Mid Freq", f"{eq.high_mid_freq} Hz")
            t.add_row("High Mid Q", str(eq.high_mid_q))
            t.add_row("High Mid Gain", f"{eq.high_mid_gain} dB")
            t.add_row("High Cut", f"{eq.high_cut} Hz")
            t.add_row("High Gain", f"{eq.high_gain} dB")
            t.add_row("Level", f"{eq.bar_level} dB")

    return t


def format_noise_gate(patch: Patch1Model) -> Table:
    t = _data_table()

    if not patch.noise_suppressor_on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Threshold", str(patch.noise_suppressor_threshold))
    t.add_row("Release", str(patch.noise_suppressor_release))

    return t


def format_send_return(patch: Patch1Model) -> Table:
    t = _data_table()

    if not patch.send_return_on:
        t.add_row("Off", style="italic")
        return t

    t.add_row("Mode", str(patch.send_return_mode.name))
    t.add_row("Send Level", str(patch.send_level))
    t.add_row("Return Level", str(patch.return_level))

    return t


def _data_table() -> Table:
    return Table(show_header=False, box=None)
