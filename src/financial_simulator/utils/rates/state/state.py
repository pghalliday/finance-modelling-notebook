from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from prettytable import PrettyTable, TableStyle

from ...format import format_day


@dataclass(frozen=True)
class State:
    current_date: date
    net_deposits: Decimal
    interest_paid: Decimal
    interest_accrued: Decimal

    def __str__(self) -> str:
        table = PrettyTable(['label', 'value'])
        table.add_row(['Current date', format_day(self.current_date)])
        table.add_row(['Net deposits', f'{self.net_deposits:.20}'])
        table.add_row(['Interest paid', f'{self.interest_paid:.20}'])
        table.add_row(['Interest accrued', f'{self.interest_accrued:.20}'])
        table.add_row(['Total', f'{self.net_deposits + self.interest_paid + self.interest_accrued:.20}'])
        table.set_style(TableStyle.SINGLE_BORDER)
        table.align['label'] = 'l'
        table.align['value'] = 'r'
        table.header = False
        return table.get_string()
