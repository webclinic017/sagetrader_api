from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
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


@router.get("/strategy", response_model=List[schemas.StrategyPlusStats])  # List[schemas.Strategy]
def read_strategies(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        shared: bool = Query(False),
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve strategies.
    """
    
    if not shared:
        strategies = crud.strategy.get_multi_for_user(db, owner_uid=current_user.uid, skip=skip, limit=limit)
    else:
        strategies = crud.strategy.get_multi_shared(db, public=shared, skip=skip, limit=limit)

    # Get strategy stats
    _strategies: list = []
    _strategy: dict = {}
    for strategy in strategies:
        won: int = 0
        total_trades: int = len(strategy.trades)
        for trade in strategy.trades:
            if trade.outcome:
                won += 1
        lost: int = total_trades - won
        if total_trades != 0:
            win_rate = (won / total_trades) * 100
        else:
            win_rate = 0

        # Build strategy obj and push
        _strategy = {
            'uid': strategy.uid,
            'name': strategy.name,
            'owner_uid': strategy.owner_uid,
            'owner': strategy.owner,
            'description': strategy.description,
            'total_trades': total_trades,
            'won_trades': won,
            'lost_trades': lost,
            'public': strategy.public,
        }
        _strategies.append(_strategy)
    return _strategies


@router.post("/strategy", response_model=schemas.StrategyPlusStats)
def create_strategy(
        *,
        db: Session = Depends(get_db),
        strategy_in: schemas.StrategyCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new strategy.
    """
    strategy = crud.strategy.get_by_name_owner(db, name=strategy_in.name, owner_uid=current_user.uid)
    if strategy:
        raise HTTPException(
            status_code=400,
            detail="This strategy already exists in the system.",
        )
    strategy_in.owner_uid = current_user.uid
    strategy = crud.strategy.create(db, obj_in=strategy_in)
    #  stats
    won: int = 0
    total_trades: int = len(strategy.trades)
    for trade in strategy.trades:
        if trade.outcome:
            won += 1
    lost: int = total_trades - won
    if total_trades != 0:
        win_rate = (won / total_trades) * 100
    else:
        win_rate = 0

    # Build strategy obj and push
    _strategy = {
        'uid': strategy.uid,
        'name': strategy.name,
        'owner_uid': strategy.owner_uid,
        'owner': strategy.owner,
        'description': strategy.description,
        'total_trades': total_trades,
        'won_trades': won,
        'lost_trades': lost,
        'win_rate': win_rate,
        'public': strategy.public,
    }
    return _strategy


@router.put("/strategy/{strategy_uid}", response_model=schemas.StrategyPlusStats)
def update_strategy(
        *,
        db: Session = Depends(get_db),
        strategy_uid: int,
        strategy_in: schemas.StrategyUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an strategy.
    """
    strategy = crud.strategy.get(db, uid=strategy_uid)
    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="This strategy does not exist in the system",
        )
    strategy = crud.strategy.update(db, db_obj=strategy, obj_in=strategy_in)
    #  stats
    won: int = 0
    total_trades: int = len(strategy.trades)
    for trade in strategy.trades:
        if trade.outcome:
            won += 1
    lost: int = total_trades - won
    if total_trades != 0:
        win_rate = (won / total_trades) * 100
    else:
        win_rate = 0

    # Build strategy obj and push
    _strategy = {
        'uid': strategy.uid,
        'name': strategy.name,
        'description': strategy.description,
        'owner_uid': strategy.owner_uid,
        'owner': strategy.owner,
        'total_trades': total_trades,
        'won_trades': won,
        'lost_trades': lost,
        'win_rate': win_rate,
        'public': strategy.public,
    }
    return _strategy


@router.delete("/strategy/{strategy_uid}", response_model=schemas.StrategyDelete)
def delete_strategy(
        *,
        db: Session = Depends(get_db),
        strategy_uid: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an strategy.
    """
    strategy = crud.strategy.get(db, uid=strategy_uid)
    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    strategy = crud.strategy.remove(db, uid=strategy_uid)
    return strategy

