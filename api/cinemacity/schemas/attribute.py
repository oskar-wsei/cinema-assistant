from typing import TypedDict


class AttributeItem(TypedDict):
    id: str
    url: str | None
    visible: bool
    sequence: int | None


AttributeGroup = TypedDict(
    'AttributeGroup',
    {
        'group-name': str,
        'items': list[AttributeItem],
    },
)

DropdownConfig = TypedDict(
    'DropdownConfig',
    {
        'genres': list[str],
        'screening-type': list[str],
        'other': list[str],
    },
)


class AttributesConfig(TypedDict):
    attributes: list[AttributeGroup]
    dropdownConfig: DropdownConfig
    mobileFilterConfig: list[str]
