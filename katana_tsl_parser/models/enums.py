from enum import IntEnum


class _DescIntEnum(IntEnum):
    description: str

    def __new__(cls, value: int, description: str = "") -> "_DescIntEnum":
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description

        return obj

    def __repr__(self) -> str:
        return self.description


class AcProcessorType(IntEnum):
    Small = 0
    Medium = 1
    Bright = 2
    Power = 3


class AmpType(IntEnum):
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
    RFireVintage = 0x14
    RFireModern = 0x15
    CoreMetal = 0x07
    Custom = 0x19


class BoostType(IntEnum):
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


class CabResonance(IntEnum):
    Vintage = 0
    Modern = 1
    Deep = 2


class ChainItem(IntEnum):
    PedalFX = 11
    Booster = 15
    Mod = 5
    FX = 6
    EQ = 4
    Solo = 10
    Preamp = 2
    EQ2 = 0
    NoiseGate = 13
    FootVolume = 12
    SendReturn = 1
    Delay = 7
    Delay2 = 17
    Reverb = 8

    Unknown1 = 9  # Is always after reverb
    Unknown2 = 18
    Unknown3 = 3
    Unknown4 = 14
    Unknown5 = 16
    Unknown6 = 19


class CompressorType(IntEnum):
    BossComp = 0
    HiBand = 1
    Light = 2
    DComp = 3
    Orange = 4
    Fat = 5
    Mild = 6


class ContourChoice(IntEnum):
    Off = 0
    Contour1 = 1
    Contour2 = 2
    Contour3 = 3


class CrossoverFreq(IntEnum):
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


class DelayChorusOutput(IntEnum):
    DAndE = 0
    DOverE = 1


class DelayChorusType(IntEnum):
    Chorus = 0
    Echo = 1


class DelayType(IntEnum):
    Digital = 0x00
    Pan = 0x01
    Stereo = 0x02
    Reverse = 0x06
    Analog = 0x07
    TapeEcho = 0x08
    Modulate = 0x09
    SDE3000 = 0x0A


class EqPosition(IntEnum):
    AmpIn = 0
    AmpOut = 1


class EqType(IntEnum):
    Parametric = 0
    Graphic10 = 1


class Footswitch(IntEnum):
    ChannelSwitch = 0
    BankAB = 1
    SoloOnOff = 2


class GuitarSimType(IntEnum):
    SingleToHumbucker = 0
    HumbuckerToSingle = 1
    HumbuckerToHalfTone = 2
    SingleToHollow = 3
    HumbuckerToHollow = 4
    SingleToAcoustic = 5
    HumbuckerToAcoustic = 6
    PiezoToAcoustic = 7


class Harmony(_DescIntEnum):
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


class HighCutFreq(IntEnum):
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


class HumanizerMode(IntEnum):
    Picking = 0
    Auto = 1


class Key(_DescIntEnum):
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


class KnobBooster(IntEnum):
    Preset = 0
    Drive = 1
    Tone = 2
    Bottom = 3
    EffectLevel = 4
    SoloSwitch = 5
    SoloLevel = 6
    DirectMix = 7


class KnobDelay(IntEnum):
    Preset = 0
    DelayTime = 1
    Feedback = 2
    HighCut = 3
    EffectLevel = 4
    DirectMix = 5
    ModRate = 6
    ModDepth = 7


class KnobReverb(IntEnum):
    Preset = 0
    ReverbTime = 1
    PreDelay = 2
    EffectLevel = 3
    DirectMix = 4
    LowCut = 5
    HighCut = 6
    Density = 7
    SpringSens = 8


class KnobChorus(IntEnum):
    Preset = 0
    LowRate = 1
    LowDepth = 2
    LowPreDelay = 3
    LowLevel = 4
    DirectMix = 5
    HighRate = 6
    HighDepth = 7
    HighPreDelay = 8
    HighLevel = 9
    Crossover = 10


class KnobFlanger(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Reso = 3
    Manual = 4
    EffectLevel = 5
    LowCut = 6
    DirectMix = 7


class KnobPhaser(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Reso = 3
    Manual = 4
    EffectLevel = 5
    StepRate = 6
    DirectMix = 7


class KnobUniV(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Level = 3


class KnobTremolo(IntEnum):
    Preset = 0
    WaveShape = 1
    Rate = 2
    Depth = 3
    Level = 4


class KnobVibrato(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Level = 3


class KnobRotaty(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Level = 3


class KnobRingMod(IntEnum):
    Preset = 0
    Frequency = 1
    EffectLevel = 2
    DirectMix = 3


class KnobSlowGear(IntEnum):
    Preset = 0
    Sens = 1
    RiseTime = 2
    Level = 3


class KnobSlicer(IntEnum):
    Preset = 0
    Rate = 1
    TriggerSens = 2
    EffectLevel = 3
    DirectMix = 4


class KnobCompressor(IntEnum):
    Preset = 0
    Sustain = 1
    Attack = 2
    Tone = 3
    Level = 4


class KnobLimiter(IntEnum):
    Preset = 0
    Threshold = 1
    Ratio = 2
    Attack = 3
    Release = 4
    Level = 5


class KnobTouchWah(IntEnum):
    Preset = 0
    Sens = 1
    Freq = 2
    Peak = 3
    EffectLevel = 4
    DirectMix = 5


class KnobAutoWah(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Freq = 3
    Peak = 4
    EffectLevel = 5
    DirectMix = 6


class KnobPedalWah(IntEnum):
    Preset = 0
    PedalPos = 1
    PedalMin = 2
    PedalMax = 3
    EffectLevel = 4
    DirectMix = 5


class KnobGraphicEq(IntEnum):
    Preset = 0
    Hz31 = 1
    Hz62 = 2
    Hz125 = 3
    Hz250 = 4
    Hz500 = 5
    Hz1000 = 6
    Hz2000 = 7
    Hz4000 = 8
    Hz8000 = 9
    Hz16000 = 10
    Level = 11


class KnobParametricEq(IntEnum):
    Preset = 0
    LowGain = 1
    LowMidGain = 2
    HighMidGain = 3
    HighGain = 4
    Level = 5
    LowMidFreq = 6
    LowMidQ = 7
    HighMidFreq = 8
    HighMidQ = 9
    LowCut = 10
    HighCut = 11


class KnobGuitarSim(IntEnum):
    Preset = 0
    Low = 1
    High = 2
    Body = 3
    Level = 4


class KnobAcGuitarSim(IntEnum):
    Preset = 0
    Low = 1
    High = 2
    Body = 3
    Level = 4


class KnobAcProcessor(IntEnum):
    Preset = 0
    Bass = 1
    Middle = 2
    Treble = 3
    Presence = 4
    Level = 5
    MidFreq = 6


class KnobWaveSynth(IntEnum):
    Preset = 0
    Cutoff = 1
    Reso = 2
    Level = 3
    FilterSens = 4
    FilterDecay = 5
    FilterDepth = 6
    DirectMix = 7


class KnobOctave(IntEnum):
    Preset = 0
    EffectLevel = 1
    DirectMix = 2


class KnobHeavyOctave(IntEnum):
    Preset = 0
    Oct1Level = 8
    Oct2Level = 9
    DirectMix = 10


class KnobPitchShifter(IntEnum):
    Preset = 0
    Ps1Pitch = 1
    Ps1Level = 2
    Ps2Pitch = 3
    Ps2Level = 4
    DirectMix = 5
    Ps1Fine = 6
    Ps1PreDelay = 7
    Ps1Feedback = 8
    Ps2Fine = 9
    Ps2PreDelay = 10


class KnobHarmonist(IntEnum):
    Preset = 0
    Hr1Harmony = 1
    Hr2Harmony = 2
    MasterKey = 3
    DirectMix = 4
    Hr1PreDelay = 5
    Hr1Feedback = 6
    Hr1Level = 7
    Hr2PreDelay = 8
    Hr2Level = 9


class KnobHumanizer(IntEnum):
    Preset = 0
    Rate = 1
    Depth = 2
    Level = 3
    Sens = 4
    Manual = 5


class KnobPhaser90E(IntEnum):
    Preset = 0
    Speed = 1


class KnobFlanger117E(IntEnum):
    Preset = 0
    Manual = 1
    Witdh = 2
    Speed = 3
    Regen = 4


class KnobWah95E(IntEnum):
    Preset = 0
    PedalPos = 1
    PedalMin = 2
    PedalMax = 3
    EffectLevel = 4
    DirectMix = 5


class KnobDC30(IntEnum):
    Preset = 0
    ChorusIntensity = 1
    EchoRepeatRate = 2
    EchoIntensity = 3
    EchoVolume = 4
    InputVolume = 5
    Tone = 6


class KnobPedalBend(IntEnum):
    Preset = 0
    PedalPos = 1
    Pitch = 2
    EffectLevel = 3
    DirectMix = 4


class Light(IntEnum):
    Green = 0
    Red = 1
    Yellow = 2


class LimiterType(IntEnum):
    BossLimiter = 0
    Rack160D = 1
    VintageRackU = 2


class LowCutFreq(IntEnum):
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


class MidFreq(_DescIntEnum):
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


class ModFxType(IntEnum):
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


class PedalFxType(IntEnum):
    Wah = 0
    Bend = 1
    Wah95E = 2


class PedalWahType(IntEnum):
    Cry = 0
    Vo = 1
    Fat = 2
    Light = 3
    SevenString = 4
    Reso = 5


class Phase(IntEnum):
    Normal = 0x00
    Inverse = 0x01


class PhaserType(IntEnum):
    Stage4 = 0
    Stage8 = 1
    Stage12 = 2
    BiPhase = 3


class PitchShifterMode(IntEnum):
    Fast = 0
    Medium = 1
    Slow = 2
    Mono = 3


class Polarity(IntEnum):
    Down = 0
    Up = 1


class Range(IntEnum):
    KHz8 = 0x00
    KHz17 = 0x01


class Ratio(_DescIntEnum):
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


class ReverbMode(IntEnum):
    Delay = 0x00
    DelayReverb = 0x01
    Reverb = 0x02


class ReverbType(IntEnum):
    Room = 0x01
    Hall = 0x03
    Plate = 0x04
    Spring = 0x05
    Modulate = 0x06


class RingModMode(IntEnum):
    Normal = 0
    Intelligent = 1


class VoiceType(IntEnum):
    Voice1 = 0
    Voice2 = 1


class Vowel(IntEnum):
    a = 0
    e = 1
    i = 2
    o = 3
    u = 4


class WahMode(IntEnum):
    LPF = 0
    BPF = 1


class WaveSynthType(IntEnum):
    Saw = 0
    Square = 1
