from typing_extensions import Annotated
from pydantic import BaseModel
from pydantic import BaseModel, Field

class ClientInput(BaseModel):
    id: int
    age: Annotated[int, Field(ge=0, le=120)]  # entre 0 et 120 ans
    revenue: Annotated[float, Field(ge=0)]    # revenu >= 0

    class Config:
        extra = "forbid"  # Rejette les champs inattendus
        
class ClientResponse(BaseModel):
    id: int
    age: int
    revenue: float

    class Config:
        from_attributes = True  # Important pour SQLAlchemy -> Pydantic
