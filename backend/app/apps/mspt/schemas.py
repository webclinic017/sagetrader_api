from typing import Optional

from pydantic import BaseModel

#
# ........ Instrument Schemas .........
#
class InstrumentBase(BaseModel):
    name: str

class Instrument(InstrumentBase):
    id: int

    class Config:
        orm_mode = True

class InstrumentUpdate(Instrument):
    name: Optional[str] = None

class InstrumentCreate(InstrumentBase):
    pass


#
# ........ Strategy Schemas .........
#
class StrategyBase(BaseModel):
    name: str
    description: str

class Strategy(StrategyBase):
    id: int

    class Config:
        orm_mode = True

class StrategyUpdate(Strategy):
    name: Optional[str] = None
    description: Optional[str] = None

class StrategyCreate(StrategyBase):
    pass

class StrategyPlusStats(Strategy):
    total_trades: int
    won_trades: int
    lost_trades: int
#
# ........ StrategyImage Schemas .........
#
class StrategyImageBase(BaseModel):
    strategy_id: int
    strategy: Strategy
    alt: str
    location: str
    # image: bytes

class StrategyImage(StrategyImageBase):
    id: int

    class Config:
        orm_mode = True

class StrategyImageLocation(BaseModel):
    id: int
    strategy_id: int
    strategy: Strategy
    alt: str
    location: str

    class Config:
        orm_mode = True

class StrategyImageUpdate(StrategyImage):
    strategy: Optional[Strategy] = None
    strategy_id: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class StrategyImageCreate(StrategyImageBase):
    strategy: Optional[Strategy] = None


#
# ........ Style Schemas .........
#
class StyleBase(BaseModel):
    name: str
    description: str

class Style(StyleBase):
    id: int

    class Config:
        orm_mode = True

class StyleUpdate(Style):
    name: Optional[str] = None
    description: Optional[str] = None

class StyleCreate(StyleBase):
    pass


#
# ........ Trade Schemas .........
#
class TradeBase(BaseModel):
    instrument_id: int
    strategy_id: int
    position: bool
    outcome: bool
    status: bool
    pips: int
    rr: float
    style_id: int
    description: str
    date: str

class Trade(TradeBase):
    id: int
    instrument: Instrument
    strategy: Strategy
    style: Style

    class Config:
        orm_mode = True

class TradeUpdate(Trade):
    instrument_id: Optional[int] = None
    instrument: Optional[Instrument] = None
    strategy_id: Optional[int] = None
    strategy: Optional[Strategy] = None
    position: Optional[bool] = True
    outcome: Optional[bool] = True
    status: Optional[bool] = True
    pips: Optional[int] = 0
    rr: Optional[str] = None
    style_id: Optional[int] = None
    style: Optional[Style] = None
    description: Optional[str] = None
    date: Optional[str] = None

class TradeCreate(TradeBase):
    pass


#
# ........ StrategyImage Schemas .........
#
class TradeImageBase(BaseModel):
    trade_id: int
    trade: Trade
    alt: str
    location: str
    # image: bytes

class TradeImage(TradeImageBase):
    id: int

    class Config:
        orm_mode = True

class TradeImageLocation(BaseModel):
    id: int
    trade_id: int
    trade: Trade
    alt: str
    location: str

    class Config:
        orm_mode = True

class TradeImageUpdate(TradeImage):
    trade: Optional[Trade] = None
    trade_id: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class TradeImageCreate(TradeImageBase):
    trade: Optional[Trade] = None


#
# ........ TradingPlan Schemas .........
#
class TradingPlanBase(BaseModel):
    name: str
    description: str

class TradingPlan(TradingPlanBase):
    id: int

    class Config:
        orm_mode = True

class TradingPlanUpdate(TradingPlan):
    name: Optional[str] = None
    description: Optional[str] = None

class TradingPlanCreate(TradingPlanBase):
    pass

#
# ........ Tasks/Notes Schemas .........
#
class TaskBase(BaseModel):
    name: str
    description: str

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class TaskUpdate(Task):
    name: Optional[str] = None
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass