from typing import TypedDict


class Languages(TypedDict):
    original: list[str]
    dubbed: list[str]
    voiceover: list[str]
    subtitles: list[str]


class Media(TypedDict):
    type: str
    subType: str
    url: str
    dimensionWidth: str | None
    dimensionHeight: str | None


class AddressInfo(TypedDict):
    address1: str
    address2: str | None
    address3: str | None
    address4: str | None
    city: str
    state: str | None
    postalCode: str
