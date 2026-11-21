from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from .. import cinemacity as cc


class ApiModel(BaseModel):
    model_config = ConfigDict(frozen=True)


class ErrorResponse(ApiModel):
    detail: str = Field(description='Human-readable error description.')


class Languages(ApiModel):
    original: list[str] = Field(description='Original languages.')
    dubbed: list[str] = Field(description='Dubbing languages.')
    voiceover: list[str] = Field(description='Voice-over languages.')
    subtitles: list[str] = Field(description='Subtitle languages.')

    @classmethod
    def from_cinema_city(cls, languages: cc.schemas.common.Languages) -> Self:
        return cls(
            original=languages['original'],
            dubbed=languages['dubbed'],
            voiceover=languages['voiceover'],
            subtitles=languages['subtitles'],
        )
