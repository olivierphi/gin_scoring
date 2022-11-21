from datetime import datetime
from typing import Annotated

from sqlalchemy import SmallInteger, String, DateTime
from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(DateTime, default=datetime.now)]

str_50 = Annotated[str, mapped_column(String(50))]

small_int = Annotated[int, mapped_column(SmallInteger)]
