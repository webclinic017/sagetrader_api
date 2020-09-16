from typing import List
from fastapi import (
    APIRouter, 
    Body, 
    Request,
    Depends, 
    HTTPException, 
    File, 
    UploadFile, 
    Form
)
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from pathlib import Path
from PIL import Image
import io

from app.apps.mspt import (
    models, 
    schemas, 
    crud
)
from app.apps.users import models as user_models
from app.settings.database import  get_db
from app.settings.security import (
    get_current_active_superuser, 
    get_current_active_user
)
from app.settings import config
from app.apps.core.utils.upload_files import save_upload_file
from app.utils.create_dirs import resolve_media_dirs_for, deleteFile


router = APIRouter()
db_session = Session()


#
# ........ File Routes .........
#
@router.post("/uploads-handler")
async def handle_file_uploads(
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(...), 
    parent:str  = Form(...)
):
    parent, parent_id = parent.split('-')
    media_dir = resolve_media_dirs_for(parent)
    images = []
    if parent == "strategy":    
        for _file in files:
            image_obj = models.StrategyImage()
            image_obj.alt = ""
            image_obj.strategy = db.query(models.Strategy).get(int(parent_id))
            image_obj.strategy_id = int(parent_id)
            file_path = media_dir + _file.filename
            await _file.seek(0)
            image = await _file.read()
            _image = Image.open(io.BytesIO(image))
            _image.save(file_path)
            # image_obj.image = image
            image_obj.location = file_path
            db.add(image_obj)
            db.commit()
            db.refresh(image_obj)
        images: List[schemas.StrategyImageLocation] = db.query(models.StrategyImage).filter_by(strategy_id = int(parent_id)).offset(0).limit(100).all()
    elif parent == "trade":
        for _file in files:
            image_obj = models.TradeImage()
            image_obj.alt = ""
            image_obj.trade = db.query(models.Trade).get(int(parent_id))
            image_obj.trade_id = int(parent_id)
            file_path = media_dir + _file.filename
            await _file.seek(0)
            image = await _file.read()
            _image = Image.open(io.BytesIO(image))
            _image.save(file_path)
            # image_obj.image = image
            image_obj.location = file_path
            db.add(image_obj)
            db.commit()
            db.refresh(image_obj)

        images: List[schemas.TradeImageLocation] = db.query(models.TradeImage).filter_by(trade_id = int(parent_id)).offset(0).limit(100).all()
    return images

@router.get("/fetch-files/{parent_identifier}")
async def fetch_files(
    *,
    db: Session = Depends(get_db),
    parent_identifier: str
):
    parent, parent_id = parent_identifier.split('-')
    media_dir = resolve_media_dirs_for(parent)
    images = []
    if parent == "strategy":
        images: List[schemas.StrategyImageLocation] = db.query(models.StrategyImage).filter_by(strategy_id = int(parent_id)).offset(0).limit(100).all()
    elif parent == "trade":
        images: List[schemas.TradeImageLocation] = db.query(models.TradeImage).filter_by(trade_id = int(parent_id)).offset(0).limit(100).all()
    return images


@router.delete("/delete-file/{identifier}")
async def fetch_files(
    *,
    db: Session = Depends(get_db),
    identifier: str
):
    parent, file_id = identifier.split('-')
    if parent == "strategy":        
        obj = db.query(models.StrategyImage).get(int(file_id))
    elif parent == "trade":        
        obj = db.query(models.TradeImage).get(int(file_id))

    if deleteFile(obj.location):
        db.delete(obj)
        db.commit()

    return {}


#
# ........ Instrument Routes .........
#
@router.get("/instrument", response_model=List[schemas.Instrument])
def read_instruments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve instruments.
    """
    instruments = crud.instrument.get_multi(db, skip=skip, limit=limit)
    return instruments


@router.post("/instrument", response_model=schemas.Instrument)
def create_instrument(
    *,
    db: Session = Depends(get_db),
    instrument_in: schemas.InstrumentCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new instrument.
    """
    instrument = crud.instrument.get_by_name(db, name=instrument_in.name)
    if instrument:
        raise HTTPException(
            status_code=400,
            detail="This instrument already exists in the system.",
        )
    instrument_in.name = instrument_in.name.upper()
    instrument = crud.instrument.create(db, obj_in=instrument_in)
    return instrument


@router.put("/instrument/{instrument_id}", response_model=schemas.Instrument)
def update_instrument(
    *,
    db: Session = Depends(get_db),
    instrument_id: int,
    instrument_in: schemas.InstrumentUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an instrument.
    """
    instrument = crud.instrument.get(db, id=instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=404,
            detail="This instrument does not exist in the system",
        )
    instrument = crud.instrument.update(db, db_obj=instrument, obj_in=instrument_in)
    return instrument


@router.delete("/instrument/{instrument_id}", response_model=schemas.Instrument)
def delete_instrument(
    *,
    db: Session = Depends(get_db),
    instrument_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an instrument.
    """
    instrument = crud.instrument.get(db, id=instrument_id)
    if not instrument:
        raise HTTPException(
            status_code=404,
            detail="This instrument does not exist in the system",
        )
    instrument = crud.instrument.remove(db, id=instrument_id)
    return instrument


#
# ........ Style Routes .........
#
@router.get("/style", response_model=List[schemas.Style])
def read_styles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve styles.
    """
    styles = crud.style.get_multi(db, skip=skip, limit=limit)
    return styles


@router.post("/style", response_model=schemas.Style)
def create_style(
    *,
    db: Session = Depends(get_db),
    style_in: schemas.StyleCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new style.
    """
    style = crud.style.get_by_name(db, name=style_in.name)
    if style:
        raise HTTPException(
            status_code=400,
            detail="This style already exists in the system.",
        )
    style = crud.style.create(db, obj_in=style_in)
    return style


@router.put("/style/{style_id}", response_model=schemas.Style)
def update_style(
    *,
    db: Session = Depends(get_db),
    style_id: int,
    style_in: schemas.StyleUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an style.
    """
    style = crud.style.get(db, id=style_id)
    if not style:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    style = crud.style.update(db, db_obj=style, obj_in=style_in)
    return style


@router.delete("/style/{style_id}", response_model=schemas.Style)
def delete_style(
    *,
    db: Session = Depends(get_db),
    style_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an style.
    """
    style = crud.style.get(db, id=style_id)
    if not style:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    style = crud.style.remove(db, id=style_id)
    return style



#
# ........ Strategy Routes .........
#
@router.get("/strategy", response_model=List[schemas.StrategyPlusStats]) #List[schemas.Strategy]
def read_sttraties(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve straties.
    """
    # Get Stategies
    strategies = crud.strategy.get_multi(db, skip=skip, limit=limit)

    # Get strategy stats
    _strategies: list = []
    _strategy: dict = {}
    for strategy in strategies:
        won: int = 0
        total_trades: int = len(strategy.trades)
        for trade in strategy.trades:
            if trade.outcome:
                won+=1
        lost: int = total_trades - won
        if total_trades != 0:
            win_rate = (won/total_trades)*100
        else:
            win_rate = 0

        # Build strategy obj and push
        _strategy = {
            'id': strategy.id,
            'name': strategy.name,
            'description': strategy.description,
            'total_trades': total_trades,
            'won_trades': won,
            'lost_trades': lost,
        }
        _strategies.append(_strategy)
    return _strategies


@router.post("/strategy", response_model=schemas.Style)
def create_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_in: schemas.StrategyCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new strategy.
    """
    strategy = crud.strategy.get_by_name(db, name=strategy_in.name)
    if strategy:
        raise HTTPException(
            status_code=400,
            detail="This strategy already exists in the system.",
        )
    strategy = crud.strategy.create(db, obj_in=strategy_in)
    return strategy


@router.put("/strategy/{strategy_id}", response_model=schemas.Strategy)
def update_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_id: int,
    strategy_in: schemas.StrategyUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an strategy.
    """
    strategy = crud.strategy.get(db, id=strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="This strategy does not exist in the system",
        )
    strategy = crud.strategy.update(db, db_obj=strategy, obj_in=strategy_in)
    return strategy


@router.delete("/strategy/{strategy_id}", response_model=schemas.Strategy)
def delete_strategy(
    *,
    db: Session = Depends(get_db),
    strategy_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an strategy.
    """
    strategy = crud.strategy.get(db, id=strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="This style does not exist in the system",
        )
    strategy = crud.strategy.remove(db, id=strategy_id)
    return strategy


#
# ........ Trade Routes .........
#

@router.get("/trade", response_model=List[schemas.Trade])
def read_trades(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve trades.
    """
    trades = crud.trade.get_multi(db, skip=skip, limit=limit)
    for trade in trades:
        trade.date = str(trade.date)
    return trades

@router.post("/trade", response_model=schemas.Trade)
def create_trade(
    *,
    db: Session = Depends(get_db),
    trade_in: schemas.TradeCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new trade.
    """
    print("Inside Trade Create ....")
    trade = crud.trade.create(db, obj_in=trade_in)
    trade.date = str(trade.date)
    return trade

@router.put("/trade/{trade_id}", response_model=schemas.Trade)
def update_trade(
    *,
    db: Session = Depends(get_db),
    trade_id: int,
    trade_in: schemas.TradeUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an trade.
    """
    trade = crud.trade.get(db, id=trade_id)
    if not trade:
        raise HTTPException(
            status_code=404,
            detail="This trade does not exist in the system",
        )
    trade = crud.trade.update(db, db_obj=trade, obj_in=trade_in)
    trade.date = str(trade.date)
    return trade

@router.delete("/trade/{trade_id}", response_model=schemas.Trade)
def delete_trade(
    *,
    db: Session = Depends(get_db),
    trade_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an trade.
    """
    trade = crud.trade.get(db, id=trade_id)
    if not trade:
        raise HTTPException(
            status_code=404,
            detail="This trade does not exist in the system",
        )
    trade = crud.trade.remove(db, id=trade_id)
    trade.date = str(trade.date)
    return trade


#
# ........ TradingPlan Routes .........
#

@router.get("/trading-plan", response_model=List[schemas.TradingPlan])
def read_trading_plans(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve trading plans.
    """
    trading_plans = crud.trading_plan.get_multi(db, skip=skip, limit=limit)
    return trading_plans

@router.post("/trading-plan", response_model=schemas.TradingPlan)
def create_trading_plan(
    *,
    db: Session = Depends(get_db),
    plan_in: schemas.TradingPlanCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new trading plan.
    """
    trading_plan = crud.trading_plan.create(db, obj_in=plan_in)
    return trading_plan

@router.put("/trading-plan/{plan_id}", response_model=schemas.TradingPlan)
def update_trading_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    plan_in: schemas.TradingPlanUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, id=plan_id)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.update(db, db_obj=trading_plan, obj_in=plan_in)
    return trading_plan

@router.delete("/trading-plan/{plan_id}", response_model=schemas.TradingPlan)
def delete_trading_plan(
    *,
    db: Session = Depends(get_db),
    plan_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an trading_plan.
    """
    trading_plan = crud.trading_plan.get(db, id=plan_id)
    if not trading_plan:
        raise HTTPException(
            status_code=404,
            detail="This trading_plan does not exist in the system",
        )
    trading_plan = crud.trading_plan.remove(db, id=plan_id)
    return trading_plan


#
# ........ Task Routes .........
#

@router.get("/task", response_model=List[schemas.Task])
def read_task(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Retrieve tasks.
    """
    tasks = crud.task.get_multi(db, skip=skip, limit=limit)
    return tasks

@router.post("/task", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: schemas.TaskCreate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Create new task.
    """
    task = crud.task.create(db, obj_in=task_in)
    return task

@router.put("/task/{task_id}", response_model=schemas.Task)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: schemas.TaskUpdate,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Update an task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="This task does not exist in the system",
        )
    task = crud.task.update(db, db_obj=task, obj_in=task_in)
    return task

@router.delete("/task/{task_id}", response_model=schemas.Task)
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Delete an task.
    """
    task = crud.task.get(db, id=task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="This task does not exist in the system",
        )
    task = crud.task.remove(db, id=task_id)
    return task



#
# ........ Trading Statistics .........
#

@router.get("/peformance-measures")
def trade_stats(
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_active_superuser),
):
    """
    Calculate Trading Statistics.
    """

    #1. Stategy Win Rates
        # overal peformance
        # by pair
        # by style
        # by position type

    #2. RiskReward
        # overal peformance
        # by pair
        # by style
        # by strategy

    #3. Average Pips Lost/Gained
        # overal peformance
        # by pair
        # by strategy
        # by style

    #3. Intsrument Peformances
        # overal peformance
        # by strategy
        # by style
        # by position type

    #2. Other Stats

    return {}