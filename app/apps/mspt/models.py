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
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.apps.users import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)


class BaseImage(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    # image = Column(LargeBinary)
    location = Column(String)
    alt = Column(String(128))


class StrategyImage(BaseImage):
    strategy_id = Column(Integer, ForeignKey("strategy.id", ondelete="CASCADE"), nullable=False)
    strategy = relationship("Strategy", backref="images")

    def get_ordering_queryset(self):
        return self.strategy.images.all

    def __str__(self) -> str:
        return self.strategy.name + " <image alt:> " + self.alt


class TradeImage(BaseImage):
    trade_id = Column(Integer, ForeignKey("trade.id", ondelete="CASCADE"), nullable=False)
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
    instrument_id = Column(Integer, ForeignKey("instrument.id", ondelete="RESTRICT"), nullable=False)
    instrument = relationship("Instrument", backref="trades", lazy="joined")
    strategy_id = Column(Integer, ForeignKey("strategy.id", ondelete="RESTRICT"), nullable=False)
    strategy = relationship("Strategy", backref="trades", lazy="joined")
    position = Column(Boolean(), default=True)  # True == Long Trade, False == Short Trade
    outcome = Column(Boolean(), default=False)  # True == Protibale Trade, False == Losing Trade
    status = Column(Boolean(), default=False)  # True == Running / Open Trade, False == Closed Trade
    pips = Column(Integer)
    rr = Column(Float)
    style_id = Column(Integer, ForeignKey("style.id", ondelete="RESTRICT"), nullable=False)
    style = relationship("Style", backref="trades", lazy="joined")
    description = Column(String)
    # images = relationship("TradeImage", back_populates="image")
    sl = Column(Integer) # Slop loss initial
    tp = Column(Integer) # TP loss initial
    tp_reached = Column(Boolean(), default=False )# Did trade hit targeted tp
    tp_exceeded = Column(Boolean(), default=False)  # Did trade run beyond targeted tp
    full_stop = Column(Boolean(), default=False) # Did trade hit full stop on a loss
    entry_price = Column(Float)
    sl_price = Column(Float) # initial
    tp_price = Column(Float) # initial
    scaled_in = Column(Boolean(), default=False) # Added to existing positions
    scaled_out = Column(Boolean(), default=False) # Did you pay the trader
    # Are you opening a position on a instrument that is correlated  \
    # to another instrument with an open postion too?
    correlated_position = Column(Boolean(), default=False)

class TradingPlan(BaseModel):
    pass


class Task(BaseModel):  # or Notes same same
    pass


class StudyItemAttribute(Base):
    """ManyToManyField linkage between StudyItem and Attribute"""
    studyitem_id = Column(Integer, ForeignKey("studyitem.id"), primary_key=True)
    attribute_id = Column(Integer, ForeignKey("attribute.id"), primary_key=True)


class Study(BaseModel):
    pass


class StudyItemImage(BaseImage):
    studyitem_id = Column(Integer, ForeignKey("studyitem.id", ondelete="CASCADE"), nullable=False)
    studyitem = relationship("StudyItem", backref="images", lazy="joined")

    def get_ordering_queryset(self):
        return self.studyitem.images.all

    def __str__(self) -> str:
        return self.studyitem.name + " <image alt:> " + self.alt


class StudyItem(BaseModel):
    study_id = Column(Integer, ForeignKey("study.id", ondelete="RESTRICT"), nullable=False)
    study = relationship("Study", backref="studyitems", lazy="joined")
    instrument_id = Column(Integer, ForeignKey("instrument.id", ondelete="RESTRICT"), nullable=True)
    instrument = relationship("Instrument", backref="studyitems", lazy="joined")
    position = Column(Boolean(), default=True)  # True == Long Trade, False == Short Trade
    outcome = Column(Boolean(), default=False)  # True == Pfotibale Trade, False == Losing Trade
    pips = Column(Integer)
    rrr = Column(Float)
    style_id = Column(Integer, ForeignKey("style.id", ondelete="RESTRICT"), nullable=True)
    style = relationship("Style", backref="studyitems", lazy="joined")
    date = Column(DateTime)
    attributes = relationship("Attribute", secondary=lambda: StudyItemAttribute.__table__, lazy="joined")


class Attribute(BaseModel):
    """Additional Features being studied:
    E.g Study: OrderBlock
    Attributes: W1 OB, D1 OB, OB MT, OB Open/Close, OB Low/High
    Study: One SMA
    Attributes: H1/D1 Config, H4/W1 Config"""
    study_id = Column(Integer, ForeignKey("study.id", ondelete="RESTRICT"), nullable=False)
    study = relationship("Study", backref="attributes", lazy="joined")
    studyitems = relationship("StudyItem", secondary=lambda: StudyItemAttribute.__table__, lazy="joined")


class WatchList(BaseModel):
    pass
