from typing import Optional, List, ForwardRef
from datetime import datetime
from pydantic import BaseModel


#
# ............................................ Instrument Schemas
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
# ............................................ Strategy Schemas
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
# ............................................ StrategyImage Schemas
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
# ............................................ Style Schemas
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
# ............................................ Trade Schemas
#
class TradeBase(BaseModel):
    instrument_id: Optional[int] = None
    strategy_id: Optional[int] = None
    position: Optional[bool] = True
    outcome: Optional[bool] = True
    status: Optional[bool] = True
    pips: Optional[int] = None
    rr: Optional[float] = None
    style_id: Optional[int] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    sl: Optional[int] = None
    tp: Optional[int] = None
    tp_reached: Optional[bool] = False
    tp_exceeded: Optional[bool] = False
    full_stop: Optional[bool] = False
    entry_price: Optional[float] = None
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None
    scaled_in: Optional[bool] = False
    scaled_out: Optional[bool] = False
    correlated_position: Optional[bool] = False

class Trade(TradeBase):
    id: int
    instrument: Instrument
    strategy: Strategy
    style: Style

    class Config:
        orm_mode = True

class TradeUpdate(TradeBase):
    pass

class TradeCreate(TradeBase):
    pass


#
# ............................................ StrategyImage Schemas
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
# ............................................ TradingPlan Schemas
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
# ............................................ Tasks/Notes Schemas
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


#
# ............................................ Study Schemas
#

class StudyBase(BaseModel):
    name: str
    description: str

class Study(StudyBase):
    id: int

    class Config:
        orm_mode = True

class StudyUpdate(Study):
    name: Optional[str] = None
    description: Optional[str] = None
    # attributes: Optional[List['Attribute']] = []

class StudyCreate(StudyBase):
    # attributes: Optional[List['Attribute']] = []
    pass


#
# ............................................ StudyItem Schemas
#
class StudyItemBase(BaseModel):
    description: str
    study_id: str
    instrument_id: int
    position: bool
    outcome: bool
    pips: int
    rrr: float
    style_id: int
    description: str
    date: datetime = None

class StudyItem(StudyItemBase):
    id: int
    instrument: Instrument
    style: Style

    class Config:
        orm_mode = True

class StudyItemUpdate(StudyItem):
    study_id: Optional[str] = None
    instrument_id: Optional[int] = None
    instrument: Optional[Instrument] = None
    position: Optional[bool] = True
    outcome: Optional[bool] = True
    pips: Optional[int] = 0
    rrr: Optional[str] = None
    style_id: Optional[int] = None
    style: Optional[Style] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class StudyItemCreate(StudyItemBase):
    pass

#
# ............................................ StudyItemImage Schemas
#
class StudyItemImageBase(BaseModel):
    study_id: int
    study: Study
    alt: str
    location: str
    # image: bytes

class StudyItemImage(StudyItemImageBase):
    id: int

    class Config:
        orm_mode = True

class StudyItemImageLocation(BaseModel):
    id: int
    study_id: int
    study: Study
    alt: str
    location: str

    class Config:
        orm_mode = True

class StudyItemImageUpdate(StudyItemImage):
    study: Optional[Strategy] = None
    study_id: Optional[int] = None
    alt: Optional[str] = None
    location: Optional[str] = None
    # image: Optional[bytes] = None

class StudyItemImageCreate(StudyItemImageBase):
    study: Optional[Strategy] = None


#
# ............................................ Attribute Schemas
#

class AttributeBase(BaseModel):
    name: str
    description: str
    study_id: str

class Attribute(AttributeBase):
    id: int
    # study: Study
    studyitems: List['StudyItem'] = []

    class Config:
        orm_mode = True

class AttributeUpdate(Attribute):
    name: Optional[str] = None
    description: Optional[str] = None
    study_id: Optional[str] = None

class AttributeCreate(AttributeBase):
    pass


#  ========================================================
#  ====       FowardRef for self-referencing models    ====
#  ========================================================

# ========================================================== # StudyWithAttrs
StudyWithAttrs = ForwardRef('Attribute')

class StudyWithAttrs(Study):
    attributes: List['Attribute'] = []

StudyWithAttrs.update_forward_refs()


# ========================================================== # StudyItemWithAttrs
StudyItemWithAttrs = ForwardRef('Attribute')

class StudyItemWithAttrs(StudyItem):
    attributes: List['Attribute'] = []

StudyItemWithAttrs.update_forward_refs()

# ========================================================== # StudyItemUpdateWithAttrs
StudyItemUpdateWithAttrs = ForwardRef('Attribute')

class StudyItemUpdateWithAttrs(StudyItemUpdate):
    attributes: Optional[List['Attribute']] = []

StudyItemUpdateWithAttrs.update_forward_refs()

# ========================================================== # StudyItemCreateWithAttrs
StudyItemCreateWithAttrs = ForwardRef('Attribute')

class StudyItemCreateWithAttrs(StudyItemBase):
    attributes: Optional[List['Attribute']] = []

StudyItemCreateWithAttrs.update_forward_refs()