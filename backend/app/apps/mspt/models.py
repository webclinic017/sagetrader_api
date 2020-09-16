from typing import (
    TYPE_CHECKING,
    Iterable,
    Optional,
    Union,
)
from uuid import uuid4
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Float,
    DateTime,
    LargeBinary,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.apps.users import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)

class BaseImage(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    # image = Column(LargeBinary)
    location = Column(String)
    alt = Column(String(128))

class StrategyImage(BaseImage):
    strategy_id = Column(Integer, ForeignKey("strategy.id"))
    strategy = relationship("Strategy", backref="images")

    def get_ordering_queryset(self):
        return self.strategy.images.all
    
    def __str__(self) -> str:
        return self.strategy.name + " <image alt:> " + self.alt

class TradeImage(BaseImage):
    trade_id = Column(Integer, ForeignKey("trade.id"))
    trade = relationship("Trade", backref="images")

    def get_ordering_queryset(self):
        return self.trade.images.all
    
    def __str__(self) -> str:
        return self.trade.name + " <image alt:> " + self.alt

class Instrument(BaseModel):
    # trades = relationship("Trade", back_populates="instrument")
    pass

class Strategy(BaseModel):
    # images = relationship("StrategyImage")
    # trades = relationship("Trade", back_populates="strategy")
    pass

class Style(BaseModel):
    # trades = relationship("Trade", back_populates="style")
    pass

class Trade(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    instrument_id = Column(Integer, ForeignKey("instrument.id"))
    instrument = relationship("Instrument", backref="trades")
    strategy_id = Column(Integer, ForeignKey("strategy.id"))
    strategy = relationship("Strategy", backref="trades")
    position = Column(Boolean(), default=True) # True == Long Trade, False == Short Trade
    outcome = Column(Boolean(), default=False) # True == Pfotibale Trade, False == Losing Trade
    status = Column(Boolean(), default=False) # True == Running / Open Trade, False == Closed Trade
    pips = Column(Integer) 
    rr = Column(Float) 
    style_id = Column(Integer, ForeignKey("style.id"))
    style = relationship("Style", backref="trades")
    description = Column(String)
    # images = relationship("TradeImage", back_populates="image")

class TradingPlan(BaseModel):
    pass

class Task(BaseModel): # or Notes same same
    pass