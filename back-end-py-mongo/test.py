from datetime import datetime

from pydantic import BaseModel, Field


class Model(BaseModel):
    x: list[datetime] = Field(None)


model = Model(x=[datetime.now(), datetime.now()])
print(model.x)