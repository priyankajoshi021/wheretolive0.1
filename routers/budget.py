
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import get_session
from schemas.budget_schema import BudgetRequest
from services.budget_service import calculate_budget

router = APIRouter(
    prefix="/budget",
    tags=["Budget Calculator"]
)


@router.post("/calculate")
def budget(
    request: BudgetRequest,
    session: Session = Depends(get_session)
):

    result = calculate_budget(
        request.city,
        request.salary,
        request.family_members,
        session
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    return result