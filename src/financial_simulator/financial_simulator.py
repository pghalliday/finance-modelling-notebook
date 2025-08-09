from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List

from src.financial_simulator.entity.entity import Entity, EntityState


@dataclass(frozen=True)
class SimulationDay:
    date: date
    state: Dict[str, EntityState]


def run_simulation(start_date: date, end_date: date, entities: Dict[str, Entity], state: Dict[str, EntityState]) -> \
        List[SimulationDay]:
    current_date = start_date
    simulation_days: List[SimulationDay] = []
    while current_date < end_date:
        simulation_days.append(SimulationDay(current_date, state))
        current_date += timedelta(days=1)
        state = {k: v.next(current_date, state[k]) for k, v in entities.items()}
    simulation_days.append(SimulationDay(current_date, state))
    return simulation_days
