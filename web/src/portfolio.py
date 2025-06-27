"""Track user holdings and profit/loss."""
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Position:
    symbol: str
    quantity: float
    cost_basis: float


@dataclass
class Portfolio:
    positions: Dict[str, Position] = field(default_factory=dict)

    def update(self, symbol: str, quantity: float, price: float) -> None:
        pos = self.positions.get(symbol)
        if pos:
            total_cost = pos.cost_basis * pos.quantity + price * quantity
            pos.quantity += quantity
            pos.cost_basis = total_cost / pos.quantity
        else:
            self.positions[symbol] = Position(symbol, quantity, price)

    def value(self, prices: Dict[str, float]) -> float:
        return sum(prices.get(sym, 0) * pos.quantity for sym, pos in self.positions.items())
