from fastapi import APIRouter

from ..common.dependencies import ClientDep
from ..common.errors import UPSTREAM_ERROR_RESPONSE
from ..schemas.attributes import AttributeGroup

router = APIRouter(
    prefix='/attributes', tags=['Attributes'], responses=UPSTREAM_ERROR_RESPONSE
)


@router.get('', summary='List attributes')
def list_attributes(client: ClientDep) -> list[AttributeGroup]:
    groups = client.get_attributes()['attributes']
    return [AttributeGroup.from_cinema_city(group) for group in groups]
