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
from app.settings.database import get_db
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
        parent: str = Form(...)
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
        images: List[schemas.StrategyImageLocation] = db.query(models.StrategyImage).filter_by(
            strategy_id=int(parent_id)).offset(0).limit(100).all()
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
        images: List[schemas.TradeImageLocation] = db.query(models.TradeImage).filter_by(
            trade_id=int(parent_id)).offset(0).limit(100).all()
    elif parent == "studyitem":
        for _file in files:
            image_obj = models.StudyItemImage()
            image_obj.alt = ""
            image_obj.studyitem = db.query(models.StudyItem).get(int(parent_id))
            image_obj.studyitem_id = int(parent_id)
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
        images: List[schemas.StudyItemImageLocation] = db.query(models.StudyItemImage).filter_by(
            studyitem_id=int(parent_id)).offset(0).limit(100).all()

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
        images: List[schemas.StrategyImageLocation] = db.query(models.StrategyImage).filter_by(
            strategy_id=int(parent_id)).offset(0).limit(100).all()
    elif parent == "trade":
        images: List[schemas.TradeImageLocation] = db.query(models.TradeImage).filter_by(
            trade_id=int(parent_id)).offset(0).limit(100).all()
    elif parent == "studyitem":
        images: List[schemas.StudyItemImageLocation] = db.query(models.StudyItemImage).filter_by(
            studyitem_id=int(parent_id)).offset(0).limit(100).all()
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
@router.get("/strategy", response_model=List[schemas.StrategyPlusStats])  # List[schemas.Strategy]
def read_strategies(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve strategies.
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
                won += 1
        lost: int = total_trades - won
        if total_trades != 0:
            win_rate = (won / total_trades) * 100
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
    strategy = crud.strategy.get_by_name(db, name=strategy_in.name)
    if strategy:
        raise HTTPException(
            status_code=400,
            detail="This strategy already exists in the system.",
        )
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
        'id': strategy.id,
        'name': strategy.name,
        'description': strategy.description,
        'total_trades': total_trades,
        'won_trades': won,
        'lost_trades': lost,
        'win_rate': win_rate,
    }
    return _strategy


@router.put("/strategy/{strategy_id}", response_model=schemas.StrategyPlusStats)
def update_strategy(
        *,
        db: Session = Depends(get_db),
        strategy_id: int,
        strategy_in: schemas.StrategyUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
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
        'id': strategy.id,
        'name': strategy.name,
        'description': strategy.description,
        'total_trades': total_trades,
        'won_trades': won,
        'lost_trades': lost,
        'win_rate': win_rate,
    }
    return _strategy


@router.delete("/strategy/{strategy_id}", response_model=schemas.Strategy)
def delete_strategy(
        *,
        db: Session = Depends(get_db),
        strategy_id: int,
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new trade.
    """
    trade = crud.trade.create(db, obj_in=trade_in)
    trade.date = str(trade.date)
    return trade


@router.put("/trade/{trade_id}", response_model=schemas.Trade)
def update_trade(
        *,
        db: Session = Depends(get_db),
        trade_id: int,
        trade_in: schemas.TradeUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
        current_user: user_models.User = Depends(get_current_active_user),
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
# ........ Study Routes .........
#

@router.get("/study", response_model=List[schemas.StudyWithAttrs])
def read_study(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve studies.
    """
    studies = crud.study.get_multi(db, skip=skip, limit=limit)
    return studies


@router.post("/study", response_model=schemas.Study)
def create_study(
        *,
        db: Session = Depends(get_db),
        study_in: schemas.StudyCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new study.
    """
    study = crud.study.create(db, obj_in=study_in)
    return study


@router.put("/study/{study_id}", response_model=schemas.Study)
def update_study(
        *,
        db: Session = Depends(get_db),
        study_id: int,
        study_in: schemas.StudyUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an study.
    """
    study = crud.study.get(db, id=study_id)
    if not study:
        raise HTTPException(
            status_code=404,
            detail="This study does not exist in the system",
        )
    study = crud.study.update(db, db_obj=study, obj_in=study_in)
    return study


@router.delete("/study/{study_id}", response_model=schemas.Study)
def delete_study(
        *,
        db: Session = Depends(get_db),
        study_id: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an study.
    """
    study = crud.study.get(db, id=study_id)
    if not study:
        raise HTTPException(
            status_code=404,
            detail="This study does not exist in the system",
        )
    study = crud.study.remove(db, id=study_id)
    return study


#
# ........ Study Item Routes .........
#

@router.get("/studyitems/{study_id}", response_model=List[schemas.StudyItemWithAttrs])
def read_studyitems(
        db: Session = Depends(get_db),
        study_id: int = None,
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve studyitems.
    """
    studies = crud.studyitem.get_multi_by_study(db, study_id=study_id, skip=skip, limit=limit)
    # for study in studies:
    #     study.date = str(study.date)
    return studies


@router.post("/studyitems", response_model=schemas.StudyItemWithAttrs)
def create_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_in: schemas.StudyItemCreateWithAttrs,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new studyitem.
    """
    studyitem = crud.studyitem.create(db, obj_in=studyitem_in)
    # studyitem.date = str(studyitem.date)
    return studyitem


@router.put("/studyitems/{studyitem_id}", response_model=schemas.StudyItemWithAttrs)
def update_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_id: int,
        studyitem_in: schemas.StudyItemUpdateWithAttrs,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an studyitems.
    """
    studyitem = crud.studyitem.get(db, id=studyitem_id)
    if not studyitem:
        raise HTTPException(
            status_code=404,
            detail="This studyitem does not exist in the system",
        )

    studyitem = crud.studyitem.update(db, db_obj=studyitem, obj_in=studyitem_in)
    # studyitem.date = str(studyitem.date)
    return studyitem


@router.delete("/studyitems/{studyitem_id}", response_model=schemas.StudyItem)
def delete_studyitems(
        *,
        db: Session = Depends(get_db),
        studyitem_id: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an studyitem.
    """
    studyitem = crud.studyitem.get(db, id=studyitem_id)
    if not studyitem:
        raise HTTPException(
            status_code=404,
            detail="This studyitem does not exist in the system",
        )
    studyitem = crud.studyitem.remove(db, id=studyitem_id)
    return studyitem




#
# ........ Attribute Routes .........
#

@router.get("/attribute/{study_id}", response_model=List[schemas.Attribute])
def read_attributes(
        db: Session = Depends(get_db),
        study_id: int = None,
        skip: int = 0,
        limit: int = 100,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Retrieve Attrs.
    """
    attrs = crud.attribute.get_multi_by_study(db, study_id=study_id, skip=skip, limit=limit)
    return attrs


@router.post("/attribute", response_model=schemas.Attribute)
def create_attribute(
        *,
        db: Session = Depends(get_db),
        attrs_in: schemas.AttributeCreate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Create new attr.
    """
    attrs = crud.attribute.create(db, obj_in=attrs_in)
    return attrs


@router.put("/attribute/{attr_id}", response_model=schemas.Attribute)
def update_attribute(
        *,
        db: Session = Depends(get_db),
        attr_id: int,
        attr_in: schemas.AttributeUpdate,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Update an attr.
    """
    attr = crud.attribute.get(db, id=attr_id)
    if not attr:
        raise HTTPException(
            status_code=404,
            detail="This attribute does not exist in the system",
        )
    attr = crud.attribute.update(db, db_obj=attr, obj_in=attr_in)
    return attr


@router.delete("/attribute/{attr_id}", response_model=schemas.Attribute)
def delete_attribute(
        *,
        db: Session = Depends(get_db),
        attr_id: int,
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Delete an attr.
    """
    attr = crud.attribute.get(db, id=attr_id)
    if not attr:
        raise HTTPException(
            status_code=404,
            detail="This attribute does not exist in the system",
        )
    attr = crud.attribute.remove(db, id=attr_id)
    return attr


#
# ........ Trading Statistics .........
#

@router.get("/peformance-measures")
def trade_stats(
        db: Session = Depends(get_db),
        current_user: user_models.User = Depends(get_current_active_user),
):
    """
    Calculate Trading Statistics.
    """

    # 1. Stategy Win Rates
    # overal peformance
    # by pair
    # by style
    # by position type

    # 2. RiskReward
    # overal peformance
    # by pair
    # by style
    # by strategy

    # 3. Average Pips Lost/Gained
    # overal peformance
    # by pair
    # by strategy
    # by style

    # 3. Intsrument Peformances
    # overal peformance
    # by strategy
    # by style
    # by position type

    # 2. Other Stats

    return {}
