
from pydantic import BaseModel


class BudgetRequest(BaseModel):
    city: str
    salary: float
    family_members: int = 1


class BudgetResponse(BaseModel):
    city: str
    salary: float
    rent: float
    food: float
    transport: float
    utilities: float
    remaining: float
    verdict: str