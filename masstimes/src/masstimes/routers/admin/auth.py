from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from masstimes.routers.dependencies import get_config
from masstimes.routers.types import Config

security = HTTPBasic()


async def authorize(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    config: Annotated[Config, Depends(get_config)],
) -> None:
    if (
        config.admin.username != credentials.username
        or config.admin.password != credentials.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Basic"},
        )
