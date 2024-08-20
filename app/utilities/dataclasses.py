from pydantic import BaseModel


class Coordinates(BaseModel):
    x: int = 0
    y: int = 0


