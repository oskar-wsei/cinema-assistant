from typing import Self

from pydantic import Field

from .. import cinemacity as cc
from ..schemas.common import ApiModel


class Attribute(ApiModel):
    id: str = Field(
        description='Value for the `attribute` query parameter.', examples=['4dx']
    )
    icon_url: str | None
    visible: bool = Field(description='Whether the website shows it as a filter.')


class AttributeGroup(ApiModel):
    name: str = Field(examples=['screening-type'])
    attributes: list[Attribute]

    @classmethod
    def from_cinema_city(cls, group: cc.schemas.attribute.AttributeGroup) -> Self:
        return cls(
            name=group['group-name'],
            attributes=[
                Attribute(id=item['id'], icon_url=item['url'], visible=item['visible'])
                for item in group['items']
            ],
        )
