from enum import Enum

from katana_tsl_parser.models.enums import ModFxType
from katana_tsl_parser.models.mod_fx import FxModel
from katana_tsl_parser.models.tsl import PatchModel, Patch0Model, DelayModel, Patch1Model
from katana_tsl_parser.models.types import TslObject


def print_patch(idx: int, patch: PatchModel) -> None:
    params = patch.param_set
    print(f"Patch {idx}: {params.name}")

    print_amp(params.patch0)
    print_boost(params.patch0)
    print_fx("Mod", params.fx1)
    print_fx("FX", params.fx2)
    print_delay("Delay", params.delay1)
    print_delay("Delay2", params.delay2)
    print_reverb(params.patch1)
    print_cabinet()
    print_pedal_fx()
    print_eq("EQ1")
    print_eq("EQ2")
    print_noise_gate(params.patch1)
    print_send_return(params.patch1)

def print_amp(patch: Patch0Model) -> None:
    print("Amp:")
    print(f"  Model: {patch.amp_type.name}")
    print(f"  Gain: {patch.amp_gain}")
    print(f"  Volume: {patch.amp_volume}")
    print(f"  Bass: {patch.amp_eq_bass}")
    print(f"  Middle: {patch.amp_eq_middle}")
    print(f"  Treble: {patch.amp_eq_treble}")
    print(f"  Presence: {patch.amp_eq_presence}")
    print()


def print_boost(patch: Patch0Model) -> None:
    if not patch.boost_on:
        print("Boost: Off\n")
        return

    print("Boost:")
    print(f"  Type: {patch.boost_type.name}")
    print(f"  Level: {patch.boost_level}")
    print(f"  Drive: {patch.boost_drive}")
    print(f"  Bottom: {patch.boost_bottom}")
    print(f"  Tone: {patch.boost_tone}")
    print(f"  Direct Mix: {patch.boost_direct_mix}")
    print(f"  Solo: {patch.boost_solo_on}")
    print(f"  Solo Level: {patch.boost_solo_level}")
    print()


def print_fx(name: str, fx: FxModel) -> None:
    if not fx.on:
        print(f"{name}: Off\n")
        return

    print(f"{name}:")
    print(f"  Effect: {fx.type_.name}")

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
        return

    for k, v in values.model_dump().items():
        param_name = k.replace("_", " ").strip().capitalize()
        match v:
            case Enum():
                param_value = v.name
            case _:
                param_value = v

        print(f"  {param_name}: {param_value}")

    print()


def print_delay(name: str, delay: DelayModel) -> None:
    if not delay.delay_on:
        print(f"{name}: Off\n")
        return

    print(f"{name}:")
    print(f"  Type: {delay.delay_type.name}")
    print(f"  Time: {delay.delay_time}")
    print(f"  Feedback: {delay.feedback}")
    print(f"  High Cut: {delay.high_cut.name}")
    print(f"  Effect Level: {delay.effect_level}")
    print(f"  Direct Mix: {delay.direct_mix}")
    print(f"  Tap Time: {delay.tap_time}")
    print(f"  Mod Rate: {delay.mod_rate}")
    print(f"  Mod Depth: {delay.mod_depth}")
    print(f"  Filter On: {delay.filter_on}")
    print(f"  Range: {delay.range_.name}")
    print(f"  Feedback Phase: {delay.feedback_phase.name}")
    print(f"  Delay Phase: {delay.delay_phase.name}")
    print(f"  Mod Switch On: {delay.mod_sw_on}")
    print()


def print_reverb(patch: Patch1Model) -> None:
    if not patch.reverb_on:
        print("Reverb: Off\n")
        return

    print(f"Reverb:")
    print(f"  Type: {patch.reverb_type.name}")
    print(f"  Time: {patch.reverb_time}s")
    print(f"  Pre Delay: {patch.reverb_pre_delay}ms")
    print(f"  Low Cut: {patch.reverb_low_cut.name}")
    print(f"  High Cut: {patch.reverb_high_cut.name}")
    print(f"  Density: {patch.reverb_density}")
    print(f"  Effect Level: {patch.reverb_effect_level}")
    print(f"  Direct Mix: {patch.reverb_direct_mix}")
    print(f"  Color: {patch.reverb_color}")
    print()


def print_cabinet() -> None:
    ...


def print_pedal_fx() -> None:
    ...


def print_eq(name: str) -> None:
    # EQ and EQ 2
    ...


def print_noise_gate(patch: Patch1Model) -> None:
    if not patch.noise_suppressor_on:
        print("Noise Gate: Off\n")
        return

    print("Noise Gate:")
    print(f"  Threshold: {patch.noise_suppressor_threshold}")
    print(f"  Release: {patch.noise_suppressor_release}")
    print()



def print_send_return(patch: Patch1Model) -> None:
    if not patch.send_return_on:
        print("Send/Return: Off\n")
        return

    print("Send/Return:")
    print(f"  Mode: {patch.send_return_mode.name}")
    print(f"  Send Level: {patch.send_level}")
    print(f"  Return Level: {patch.return_level}")
    print()
