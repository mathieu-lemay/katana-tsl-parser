from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

from rich import box
from rich.console import Console, RenderableType
from rich.table import Table

from katana_tsl_parser.models.enums import DescIntEnum, EqType, ModFxType, PedalFxType
from katana_tsl_parser.models.mod_fx import FxModel
from katana_tsl_parser.models.tsl import (
    DelayModel,
    EqModel,
    ParamSetModel,
    Patch0Model,
    Patch1Model,
    Patch2Model,
    PatchModel,
)

if TYPE_CHECKING:
    from katana_tsl_parser.models.types import TslObject


class Orientation(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


@dataclass(kw_only=True, frozen=True)
class PrettyPrinter:
    orientation: Orientation = field(default=Orientation.VERTICAL)

    def print_patch(self, idx: int, patch: PatchModel) -> None:
        params = patch.param_set

        t = Table(
            title=f"Patch {idx}: {params.name}",
            box=box.ROUNDED,
            show_lines=True,
            show_header=False,
        )
        t.add_row("Amp", self.format_amp(params.patch0))
        t.add_row("Boost", self.format_boost(params.patch0))
        t.add_row("Mod", self.format_fx(params.fx1))
        t.add_row("FX", self.format_fx(params.fx2))
        t.add_row("Delay", self.format_delay(params.delay1))
        t.add_row("Delay 2", self.format_delay(params.delay2))
        t.add_row("Reverb", self.format_reverb(params.patch1))
        t.add_row("Cabinet", self.format_cabinet())
        t.add_row("Pedal FX", self.format_pedal_fx(params.patch1))
        t.add_row("EQ1", self.format_eq(params.patch0.eq))
        t.add_row("EQ2", self.format_eq(params.eq2))
        t.add_row("Noise Gate", self.format_noise_gate(params.patch1))
        t.add_row("Send/Return", self.format_send_return(params.patch1))
        t.add_row("Misc", self.format_misc(params))
        t.add_row("Panel Knobs", self.format_panel_knobs(params.patch2))

        c = Console()
        c.print(t)

    def format_amp(self, patch: Patch0Model) -> Table:
        names = ["Model", "Gain", "Volume", "Bass", "Middle", "Treble", "Presence"]
        values = [
            patch.amp_type.name,
            str(patch.amp_gain),
            str(patch.amp_volume),
            str(patch.amp_eq_bass),
            str(patch.amp_eq_middle),
            str(patch.amp_eq_treble),
            str(patch.amp_eq_presence),
        ]
        return self._data_table(names, values)

    def format_boost(self, patch: Patch0Model) -> Table:
        if not patch.boost_on:
            return self._empty_table()

        names = [
            "Type",
            "Level",
            "Drive",
            "Bottom",
            "Tone",
            "Direct Mix",
            "Solo",
            "Solo Level",
        ]
        values = [
            patch.boost_type.name,
            str(patch.boost_level),
            str(patch.boost_drive),
            str(patch.boost_bottom),
            str(patch.boost_tone),
            str(patch.boost_direct_mix),
            str(patch.boost_solo_on),
            str(patch.boost_solo_level),
        ]

        return self._data_table(names, values)

    # C901: Too complex (>10)
    # PLR0912: Too many branches (>12)
    # PLR0915: Too many statements (>50)
    def format_fx(self, fx: FxModel) -> Table:  # noqa: C901, PLR0912, PLR0915
        if not fx.on:
            return self._empty_table()

        names = ["Effect"]
        values = [fx.type_.name]

        fx_values: TslObject | None
        match fx.type_:
            case ModFxType.TWah:
                fx_values = fx.touch_wah
            case ModFxType.AutoWah:
                fx_values = fx.auto_wah
            case ModFxType.PedalWah:
                fx_values = fx.pedal_wah
            case ModFxType.Compressor:
                fx_values = fx.compressor
            case ModFxType.Limiter:
                fx_values = fx.limiter
            case ModFxType.GraphicEq:
                fx_values = fx.graphic_eq
            case ModFxType.ParametricEq:
                fx_values = fx.parametric_eq
            case ModFxType.GuitarSim:
                fx_values = fx.guitar_sim
            case ModFxType.SlowGear:
                fx_values = fx.slow_gear
            case ModFxType.WaveSynth:
                fx_values = fx.wave_synth
            case ModFxType.Octave:
                fx_values = fx.octave
            case ModFxType.PitchShifter:
                fx_values = fx.pitch_shifter
            case ModFxType.Harmonist:
                fx_values = fx.harmonist
            case ModFxType.AcProcessor:
                fx_values = fx.ac_processor
            case ModFxType.Phaser:
                fx_values = fx.phaser
            case ModFxType.Flanger:
                fx_values = fx.flanger
            case ModFxType.Tremolo:
                fx_values = fx.tremolo
            case ModFxType.Rotary:
                fx_values = fx.rotary
            case ModFxType.UniV:
                fx_values = fx.univibe
            case ModFxType.Slicer:
                fx_values = fx.slicer
            case ModFxType.Vibrato:
                fx_values = fx.vibrato
            case ModFxType.RingMod:
                fx_values = fx.ring_mod
            case ModFxType.Humanizer:
                fx_values = fx.humanizer
            case ModFxType.Chorus:
                fx_values = fx.chorus
            case ModFxType.AcousticGuitarSim:
                fx_values = fx.ac_guitar_sim
            case ModFxType.Phaser90E:
                fx_values = fx.phaser_90e
            case ModFxType.Flanger117E:
                fx_values = fx.flanger_117e
            case ModFxType.Wah95E:
                fx_values = fx.wah_95e
            case ModFxType.DelayChorus30:
                fx_values = fx.delay_chorus_30
            case ModFxType.HeavyOctave:
                fx_values = fx.heavy_octave
            case ModFxType.PedalBend:
                fx_values = fx.pedal_bend

        if not fx_values:
            return self._empty_table()

        for k, v in fx_values.model_dump().items():
            param_name = k.replace("_", " ").strip().title()
            match v:
                case DescIntEnum():
                    param_value = v.description
                case Enum():
                    param_value = v.name
                case _:
                    param_value = str(v)

            names.append(param_name)
            values.append(param_value)

        return self._data_table(names, values)

    def format_delay(self, delay: DelayModel) -> Table:
        if not delay.delay_on:
            return self._empty_table()

        names = [
            "Type",
            "Time",
            "Feedback",
            "High Cut",
            "Effect Level",
            "Direct Mix",
            "Tap Time",
            "Mod Rate",
            "Mod Depth",
            "Filter On",
            "Range",
            "Feedback Phase",
            "Delay Phase",
            "Mod Switch On",
        ]
        values = [
            delay.delay_type.name,
            f"{delay.delay_time}ms",
            str(delay.feedback),
            str(delay.high_cut.description),
            str(delay.effect_level),
            str(delay.direct_mix),
            str(delay.tap_time),
            str(delay.mod_rate),
            str(delay.mod_depth),
            str(delay.filter_on),
            str(delay.range_.name),
            str(delay.feedback_phase.name),
            str(delay.delay_phase.name),
            str(delay.mod_sw_on),
        ]

        return self._data_table(names, values)

    def format_reverb(self, patch: Patch1Model) -> Table:
        if not patch.reverb_on:
            return self._empty_table()

        names = [
            "Type",
            "Time",
            "Pre Delay",
            "Low Cut",
            "High Cut",
            "Density",
            "Effect Level",
            "Direct Mix",
            "Color",
        ]
        values = [
            patch.reverb_type.name,
            f"{patch.reverb_time}s",
            f"{patch.reverb_pre_delay}ms",
            patch.reverb_low_cut.description,
            patch.reverb_high_cut.description,
            str(patch.reverb_density),
            str(patch.reverb_effect_level),
            str(patch.reverb_direct_mix),
            str(patch.reverb_color),
        ]

        return self._data_table(names, values)

    def format_cabinet(
        self,
    ) -> Table:
        return self._todo_table()

    def format_pedal_fx(self, patch: Patch1Model) -> Table:
        names = ["Type"]
        values = [patch.pedal_fx_type.name]

        match patch.pedal_fx_type:
            case PedalFxType.Wah:
                names += [
                    "Wah Type",
                    "Wah Position",
                    "Wah Min",
                    "Wah Max",
                    "Wah Level",
                    "Wah Direct Mix",
                ]
                values += [
                    patch.pedal_fx_wah_type.name,
                    str(patch.pedal_fx_wah_pos),
                    str(patch.pedal_fx_wah_min),
                    str(patch.pedal_fx_wah_max),
                    str(patch.pedal_fx_wah_level),
                    str(patch.pedal_fx_wah_direct_mix),
                ]
            case PedalFxType.Bend:
                names += [
                    "Bend Position",
                    "Bend Pitch",
                    "Bend Level",
                    "Bend Direct Mix",
                ]
                values += [
                    str(patch.pedal_fx_bend_pos),
                    str(patch.pedal_fx_bend_pitch),
                    str(patch.pedal_fx_bend_level),
                    str(patch.pedal_fx_bend_direct_mix),
                ]
            case PedalFxType.Wah95E:
                names += [
                    "Wah95 Position",
                    "Wah95 Min",
                    "Wah95 Max",
                    "Wah95 Level",
                    "Wah95 Direct Mix",
                ]
                values += [
                    str(patch.pedal_fx_wah95_pos),
                    str(patch.pedal_fx_wah95_min),
                    str(patch.pedal_fx_wah95_max),
                    str(patch.pedal_fx_wah95_level),
                    str(patch.pedal_fx_wah95_direct_mix),
                ]

        return self._data_table(names, values)

    def format_eq(self, eq: EqModel) -> Table:
        if not eq.on:
            return self._empty_table()

        names = ["Type"]
        values = [eq.type_.name]

        match eq.type_:
            case EqType.Graphic10:
                names += [
                    "31 Hz",
                    "62 Hz",
                    "125 Hz",
                    "250 Hz",
                    "500 Hz",
                    "1 kHz",
                    "2 kHz",
                    "4 kHz",
                    "8 kHz",
                    "16 kHz",
                    "Level",
                ]
                values += [
                    f"{eq.bar_31} dB",
                    f"{eq.bar_62} dB",
                    f"{eq.bar_125} dB",
                    f"{eq.bar_250} dB",
                    f"{eq.bar_500} dB",
                    f"{eq.bar_1000} dB",
                    f"{eq.bar_2000} dB",
                    f"{eq.bar_4000} dB",
                    f"{eq.bar_8000} dB",
                    f"{eq.bar_16000} dB",
                    f"{eq.bar_level} dB",
                ]
            case EqType.Parametric:
                names += [
                    "Low Cut",
                    "Low Gain",
                    "Low Mid Freq",
                    "Low Mid Q",
                    "Low Mid Gain",
                    "High Mid Freq",
                    "High Mid Q",
                    "High Mid Gain",
                    "High Cut",
                    "High Gain",
                    "Level",
                ]
                values += [
                    f"{eq.low_cut.description}",
                    f"{eq.low_gain} dB",
                    f"{eq.low_mid_freq.description}",
                    str(eq.low_mid_q),
                    f"{eq.low_mid_gain} dB",
                    f"{eq.high_mid_freq.description}",
                    str(eq.high_mid_q),
                    f"{eq.high_mid_gain} dB",
                    f"{eq.high_cut.description}",
                    f"{eq.high_gain} dB",
                    f"{eq.bar_level} dB",
                ]

        return self._data_table(names, values)

    def format_noise_gate(self, patch: Patch1Model) -> Table:
        return self._data_table(
            ["Threshold", "Release"],
            [
                str(patch.noise_suppressor_threshold),
                str(patch.noise_suppressor_release),
            ],
        )

    def format_send_return(self, patch: Patch1Model) -> Table:
        if not patch.send_return_on:
            return self._empty_table()

        names = ["Mode", "Send Level", "Return Level"]
        values = [
            patch.send_return_mode.name,
            str(patch.send_level),
            str(patch.return_level),
        ]

        return self._data_table(names, values)

    def format_misc(self, params: ParamSetModel) -> Table:
        names = ["Master Key", "Solo On", "Solo Level", "Contour"]

        solo_on = (
            str(params.patch1.solo_on)
            if params.patch1.solo_on is not None
            else "<unspecified>"
        )
        solo_level = (
            str(params.patch1.solo_level)
            if params.patch1.solo_level is not None
            else "<unspecified>"
        )
        contour = (
            params.patch1.contour.name
            if params.patch1.contour is not None
            else "<unspecified>"
        )
        values = [params.patch1.master_key.description, solo_on, solo_level, contour]

        return self._data_table(names, values)

    def format_panel_knobs(self, patch: Patch2Model) -> Table:
        def _knob_table(g: str, r: str, y: str, current: str = "N/A") -> Table:
            kt_names = ["Green", "Red", "Yellow", "Current"]

            t = self._data_table(kt_names, [g, r, y, current])
            t.box = None

            return t

        names = ["Boost", "Mod", "FX", "Delay", "Reverb", "Delay2"]
        values = [
            _knob_table(
                patch.boost_green.name,
                patch.boost_red.name,
                patch.boost_yellow.name,
                patch.boost_light.name,
            ),
            _knob_table(
                patch.mod_green.name,
                patch.mod_red.name,
                patch.mod_yellow.name,
                patch.mod_light.name,
            ),
            _knob_table(
                patch.fx_green.name,
                patch.fx_red.name,
                patch.fx_yellow.name,
                patch.fx_light.name,
            ),
            _knob_table(
                patch.delay_green.name,
                patch.delay_red.name,
                patch.delay_yellow.name,
                patch.delay_light.name,
            ),
            _knob_table(
                f"{patch.reverb_green.name} [{patch.reverb_green_mode.name}]",
                f"{patch.reverb_red.name} [{patch.reverb_red_mode.name}]",
                f"{patch.reverb_yellow.name} [{patch.reverb_yellow_mode.name}]",
                patch.reverb_light.name,
            ),
            _knob_table(
                patch.delay2_green.name,
                patch.delay2_red.name,
                patch.delay2_yellow.name,
            ),
        ]

        t = self._data_table(names, values)

        t.show_lines = True
        t.box = box.ROUNDED

        return t

    def _data_table(
        self,
        names: Sequence[RenderableType],
        values: Sequence[RenderableType | None],
    ) -> Table:
        t = Table(show_header=False)

        match self.orientation:
            case Orientation.VERTICAL:
                t.box = None
                for name, value in zip(names, values, strict=True):
                    t.add_row(name, value)
            case Orientation.HORIZONTAL:
                t.box = box.ROUNDED
                t.show_lines = True
                t.add_row(*names)
                t.add_row(*values)

        return t

    @staticmethod
    def _empty_table() -> Table:
        t = Table(show_header=False, box=None)
        t.add_row("Off", style="italic")
        return t

    @staticmethod
    def _todo_table() -> Table:
        t = Table(show_header=False, box=None)
        t.add_row("TODO", style="bold")
        return t
