from dataclasses import dataclass
from datetime import` date

@dataclass(order=True)
class YearMonth:
    year: int
    month: int

    def __post_init__(self):
        if not (1 <= self.month <= 12):
            raise ValueError("Month must be between 1 and 12")

    def __str__(self):
        return f"{self.year}-{self.month:02d}"

    def __sub__(self, other) -> int:
        if isinstance(other, YearMonth):
            return 12 * (other.year - self.year) + other.month - self.month
        else:
            return NotImplemented

    def __contains__(self, other) -> bool:
        if isinstance(other, date):
            return (other.year == self.year) and (other.month == self.month)
        else:
            return NotImplemented

    @classmethod
    def from_date(cls, d: date):
        return cls(d.year, d.month)

    @classmethod
    def from_str(cls, s: str):
        pieces = s.split("-")
        assert len(pieces) == 2
        return cls(int(pieces[0]), int(pieces[1]))

    def day(d: int):
        return date(self.year, self.month, d)
