# Import all the models, so that Base has them before being
# imported by Alembic

from app.settings.database import DBModel  #noqa
from app.apps.users.models import User  #noqa
from app.apps.mspt.models import (
    Instrument,
    Style,
    StrategyImage,
    Strategy,
    TradeImage,
    Trade,
)  #noqa

