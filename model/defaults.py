from mps060602 import ADChannelMode, MPS060602Para, PGAAmpRate
DEVICE_NUMBER = 0

AD_SAMPLE_RATE = 450000
BUFFER_SIZE: int = 2048

PARAMETER = MPS060602Para(
    ADChannel=ADChannelMode.in1,
    ADSampleRate=AD_SAMPLE_RATE,
    Gain=PGAAmpRate.range_10V,
)

