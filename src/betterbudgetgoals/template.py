from dataclasses import dataclass
import enum
from datetime import date

from .month import YearMonth

# Analogous classes to the Actual Budget templates, based on
# https://github.com/actualbudget/actual/blob/master/packages/loot-core/src/types/models/templates.ts
# Implementing 'template's only, ignoring 'goal' and 'error'

# I know you shouldn't use floats for currency. This is a proof of concept

RepeatUnit = enum.StrEnum("RepeatUnit", ["DAY", "WEEK", "MONTH", "YEAR"])
AdjustmentType = enum.StrEnum("AdjustmentType", ["PERCENT", "FIXED"])

@dataclass
class _Limit:
    amount: float
    hold: bool
    period: RepeatUnit | None = None
    start: date | None = None

@dataclass
class BaseTemplate:
    description: string | None = None

@dataclass
class BaseTemplateWithPriority(BaseTemplate):
    priority: int

#@dataclass
#class PercentageTemplate(BaseTemplateWithPriority):
#    percent: float
#    previous: bool
#    category: str

@dataclass
class PeriodicTemplate(BaseTemplateWithPriority):
    amount: float
    period_unit: RepatUnit
    period_amt: int
    starting: date
    limit: _Limit | None = None

@dataclass
class ByTemplate(BaseTemplateWithPriority):
    amount: float
    month: YearMonth
    annual: bool | None = None
    repeat: int | None = None
    
@dataclass
class SpendTemplate(ByTemplate):
    from_: YearMonth

@dataclass
class SimpleTemplate(BaseTemplateWithPriority):
    monthly: float | None = None
    limit: _Limit | None = None

#@dataclass
#class AverageTemplate(BaseTemplateWithPriority):
#    numMonths: int
#    adjustment: float | None = None
#    adjustmentType: AdjustmentType | None = None

#@dataclass
#class CopyTemplate(BaseTemplateWithPriority):
#    lookBack: int


