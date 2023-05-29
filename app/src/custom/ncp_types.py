from typing import Optional, Union

from typing_extensions import NotRequired, TypedDict


class ClovaSpeechSpeaker(TypedDict):
    label: str
    name: str
    edited: NotRequired[bool]


class ClovaSpeechUserdata(TypedDict):
    _ncp_DomainCode: str
    _ncp_DomainId: int
    _ncp_TaskId: int
    _ncp_TraceId: str


class ClovaSpeechDiarization(TypedDict):
    enable: bool
    speakerCountMin: int
    speakerCountMax: int


class ClovaSpeechParams(TypedDict):
    service: str
    domain: str
    lang: str
    completion: str
    callback: str
    diarization: ClovaSpeechDiarization
    boostings: list[Optional[str]]
    forbiddens: Optional[str]
    fullText: NotRequired[bool]
    noiseFiltering: bool
    resultToObs: bool
    segment: NotRequired[str]
    morpheme: NotRequired[str]
    priority: int
    userdata: ClovaSpeechUserdata


class ClovaSpeechSegmentDiarization(TypedDict):
    label: str


class ClovaSpeechSegment(TypedDict):
    start: int
    end: int
    text: str
    confidence: float
    diarization: ClovaSpeechSegmentDiarization
    speaker: ClovaSpeechSpeaker
    words: list[list[Union[int, str]]]
    textEdited: str


class ClovaResponse(TypedDict):
    token: str
    result: str
    message: str
    version: NotRequired[str]
    params: NotRequired[ClovaSpeechParams]
    progress: NotRequired[int]
    segments: NotRequired[list[ClovaSpeechSegment]]
    text: NotRequired[str]
    confidence: NotRequired[float]
    speakers: NotRequired[list[ClovaSpeechSpeaker]]


class ClovaBoostingKeywords(TypedDict):
    words: str
