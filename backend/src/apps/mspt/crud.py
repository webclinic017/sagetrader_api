from typing import Optional
from sqlalchemy.orm import Session
from apps.mspt import models
from apps.mspt import schemas
from settings.security import verify_password, get_password_hash
from apps.mixins.crud import CRUDMIXIN
from fastapi.encoders import jsonable_encoder


class CRUDInstrument(CRUDMIXIN[models.Instrument, schemas.InstrumentCreate, schemas.InstrumentUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[models.Instrument]:
        name = name.upper()
        result = db_session.query(models.Instrument).filter(models.Instrument.name == name).first()
        return result

instrument = CRUDInstrument(models.Instrument)

class CRUDStyle(CRUDMIXIN[models.Style, schemas.StyleCreate, schemas.StyleUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[models.Style]:
        result = db_session.query(models.Style).filter(models.Style.name == name).first()
        return result

style = CRUDStyle(models.Style)

class CRUDStrategy(CRUDMIXIN[models.Strategy, schemas.StrategyCreate, schemas.StrategyUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[models.Strategy]:
        result = db_session.query(models.Strategy).filter(models.Strategy.name == name).first()
        return result

strategy = CRUDStrategy(models.Strategy)


class CRUDTrade(CRUDMIXIN[models.Trade, schemas.TradeCreate, schemas.TradeUpdate]):
    def create(self, db_session: Session, *, obj_in: schemas.TradeCreate) -> models.Trade:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        # parse id's as integers
        db_obj.instrument_id = int(db_obj.instrument_id)
        db_obj.strategy_id = int(db_obj.strategy_id)
        db_obj.style_id = int(db_obj.style_id)
        # relationship mode linkages
        db_obj.instrument = db_session.query(models.Instrument).get(db_obj.instrument_id)
        db_obj.strategy = db_session.query(models.Strategy).get(db_obj.strategy_id)
        db_obj.style = db_session.query(models.Style).get(db_obj.style_id)
        ###
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self, db_session: Session, *, db_obj: models.Trade, obj_in: schemas.TradeUpdate
    ) -> models.Trade:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        # reset relationship mode linkages
        obj_in_data = jsonable_encoder(obj_in)
        db_obj.instrument = db_session.query(models.Instrument).get(obj_in_data["instrument_id"])
        db_obj.strategy = db_session.query(models.Strategy).get(obj_in_data["strategy_id"])
        db_obj.style = db_session.query(models.Style).get(obj_in_data["style_id"])
        ##
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

trade = CRUDTrade(models.Trade)

class CRUDTradingPlan(CRUDMIXIN[models.TradingPlan, schemas.TradingPlanCreate, schemas.TradingPlanUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[models.TradingPlan]:
        result = db_session.query(models.TradingPlan).filter(models.TradingPlan.name == name).first()
        return result

trading_plan = CRUDTradingPlan(models.TradingPlan)


class CRUDTask(CRUDMIXIN[models.Task, schemas.TaskCreate, schemas.TaskUpdate]):
    def get_by_name(self, db_session: Session, *, name: str) -> Optional[models.Task]:
        result = db_session.query(models.Task).filter(models.Task.name == name).first()
        return result

task = CRUDTask(models.Task)