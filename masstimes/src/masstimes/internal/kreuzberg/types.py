import datetime as dt
from typing import Literal, TypeAlias

from pydantic import BaseModel

ChurchName: TypeAlias = Literal["Kreuzberg", "St. Paul"]


class KreuzbergEvent(BaseModel):
    church: ChurchName
    time: dt.datetime
    description: str


class KreuzbergEvents(BaseModel):
    events: list[KreuzbergEvent]
