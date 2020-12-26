from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.apps.mspt import (
    schemas,
    crud,
)
from app.apps.users import models as user_models
from app.settings.database import get_db
from app.settings.security import (
    get_current_active_user
)

router = APIRouter()
db_session = Session()


@router.get("/trading-plan", response_model=List[schemas.TradingPlan])
def read_trading_plans(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        shared: bool = Query(False),
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve trading plans.
    """
    if not shared:
        trading_plans = crud.trading_plan.get_multi_for_user(db, owner_uid=current_user.uid, skip=skip, limit=limit)
    else:
        trading_plans = crud.trading_plan.get_multi_shared(db, public=shared, skip=skip, limit=limit)
    return trading_plans


@router.post("/trading-plan", response_model=schemas.TradingPlan)
def create_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_in: schemas.TradingPlanCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new trading plan.
    """
    t_plan = crud.trading_plan.get_by_name_owner(db, name=plan_in.name, owner_uid=current_user.uid)
    if t_plan:
        raise HTTPException(
            status_code=400,
            detail="A trading plan with this name already exists",
        )
    plan_in.owner_uid = current_user.uid
    trading_plan = crud.trading_plan.create(db, obj_in=plan_in)
    return trading_plan


@router.put("/trading-plan/{plan_uid}", response_model=schemas.TradingPlan)
def update_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_uid: int,
        plan_in: schemas.TradingPlanUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, uid=plan_uid)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.update(db, db_obj=trading_plan, obj_in=plan_in)
    return trading_plan


@router.delete("/trading-plan/{plan_uid}", response_model=schemas.TradingPlanDelete)
def delete_trading_plan(
        *,
        db: Session = Depends(get_db),
        plan_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, uid=plan_uid)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.remove(db, uid=plan_uid)
    return trading_plan
