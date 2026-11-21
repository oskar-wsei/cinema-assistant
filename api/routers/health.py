from typing import Literal

from fastapi import APIRouter

from ..schemas.common import ApiModel

router = APIRouter(prefix='/health', tags=['Health'])


class HealthStatus(ApiModel):
    status: Literal['ok']


@router.get('', summary='Check API health')
def get_health() -> HealthStatus:
    return HealthStatus(status='ok')
