import json
from typing import List, Tuple, Dict

from prettytable import PrettyTable, TableStyle

LABEL_COLUMN_NAME = 'For the portion of the taxable amount'
RATE_COLUMN_NAME = 'Rate'
TAXABLE_COLUMN_NAME = 'Taxable portion'
TAX_DUE_COLUMN_NAME = 'Tax Due'
TOTAL_LABEL = 'Total'


def format_float(amount: float) -> str:
    return '' if amount is None else f'{amount:_.2f}'


def format_integer(amount: float) -> str:
    return '' if amount is None else f'{amount:_}'


def format_rate(rate: float) -> str:
    return '' if rate is None else f'{(rate * 100):.2f}%'


def column_width(column: List[str]) -> int:
    return max([len(text) for text in column])


def format_column_left(column: List[str], width: int) -> List[str]:
    return [f'{text:<{width}}' for text in column]


def format_column_right(column: List[str], width: int) -> List[str]:
    return [f'{text:>{width}}' for text in column]


class TaxCalculation(object):
    taxable: float
    tax_due: float

    def __init__(self, taxable: float, tax_due: float):
        self.taxable = taxable
        self.tax_due = tax_due

    def format_columns(self) -> tuple[str, str]:
        return f'{format_float(self.taxable)}', f'{format_float(self.tax_due)}'


class TaxCalculations(object):
    labels: List[str]
    rates: List[str]
    calculations: List[TaxCalculation]
    taxable: float
    tax_due: float

    def __init__(self, labels: List[str], rates: List[str], calculations: List[TaxCalculation]):
        self.labels = labels
        self.rates = rates
        self.calculations = calculations
        taxable, tax_due = zip(*[(calculation.taxable, calculation.tax_due) for calculation in self.calculations])
        self.taxable = sum(taxable)
        self.tax_due = sum(tax_due)

    def format_columns(self) -> Tuple[List[str], List[str]]:
        taxable_portions: List[str]
        tax_dues: List[str]
        taxable_portions, tax_dues = zip(*[calculation.format_columns() for calculation in self.calculations])
        return taxable_portions, tax_dues

    def format_totals(self) -> Tuple[str, str]:
        return f'{format_float(self.taxable)}', f'{format_float(self.tax_due)}'

    def __str__(self):
        taxable_portions, tax_due_portions = self.format_columns()
        taxable, tax_due = self.format_totals()
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_column(LABEL_COLUMN_NAME, self.labels, 'l')
        table.add_column(RATE_COLUMN_NAME, self.rates, 'r')
        table.add_column(TAXABLE_COLUMN_NAME, taxable_portions, 'r')
        table.add_column(TAX_DUE_COLUMN_NAME, tax_due_portions, 'r')
        table.add_divider()
        table.add_row(['', TOTAL_LABEL, taxable, tax_due])
        return table.get_string()


class TaxBand(object):
    lower: float
    upper: float | None
    rate: float

    def __init__(self, lower: float, upper: float | None, rate: float):
        self.lower = lower
        self.upper = upper
        self.rate = rate

    def calculate(self, total_taxable: float):
        if total_taxable <= self.lower:
            taxable = 0
        elif self.upper is None:
            taxable = total_taxable - self.lower
        elif total_taxable >= self.upper:
            taxable = self.upper - self.lower
        else:
            taxable = total_taxable - self.lower
        return TaxCalculation(taxable, taxable * self.rate)

    def format_columns(self) -> Tuple[str, str]:
        formatted_lower = format_integer(self.lower)
        formatted_upper = format_integer(self.upper)
        if self.lower == 0:
            if self.upper is None:
                label = 'always'
            else:
                label = f'up to {formatted_upper}'
        elif self.upper is None:
            label = f'above {formatted_lower}'
        else:
            label = f'from {formatted_lower} to {formatted_upper}'
        return label, format_rate(self.rate)


class TaxBands(object):
    bands: List[TaxBand]

    def __init__(self, bands: Dict[float, float]):
        sorted_bands = sorted(bands.items())
        if not bands[0.0]:
            # if no band is specified for above 0, then assume
            # the rate up to the first band is 0.0
            sorted_bands = [(0.0, 0.0)] + sorted_bands
        self.bands = []
        last_rate: float | None = None
        last_above: float | None = None
        for above, rate in sorted_bands:
            if last_rate is not None:
                self.bands.append(TaxBand(last_above, above, last_rate))
            last_rate = rate
            last_above = above
        self.bands.append(TaxBand(last_above, None, last_rate))

    def calculate(self, taxable: float):
        labels, rates = self.format_columns()
        return TaxCalculations(labels, rates, [band.calculate(taxable) for band in self.bands])

    def format_columns(self) -> Tuple[List[str], List[str]]:
        labels: List[str]
        rates: List[str]
        labels, rates = zip(*[band.format_columns() for band in self.bands])
        return labels, rates

    def __str__(self):
        labels, rates = self.format_columns()
        table = PrettyTable()
        table.set_style(TableStyle.SINGLE_BORDER)
        table.add_column(LABEL_COLUMN_NAME, labels, 'l')
        table.add_column(RATE_COLUMN_NAME, rates, 'r')
        return table.get_string()


class TaxBandsByYear(object):
    def __init__(self, data_file: str):
        years: Dict[int, TaxBands]

        # Load the tax bands and sort them by year and threshold
        with open(data_file) as f:
            data = json.load(f)
            years: Dict[int, TaxBands] = {}
            for year_bands in data:
                year = year_bands['year']
                bands: Dict[float, float] = {}
                for band in year_bands['bands']:
                    bands[band['above']] = band['rate']
                years[year] = TaxBands(bands)
            self.years = dict(sorted(years.items()))

    def get_bands(self, year: int) -> TaxBands:
        # Search for the year equal to or lower than the required year.
        # We assume that if we do not have bands for a year, then the bands
        # have not changed since the previous year. If we cannot find a band
        # equal to or lower than the required year, then we throw an error
        bands = [b for y, b in self.years.items() if y <= year]
        if not bands:
            raise Exception('No bands found for year {}'.format(year))
        return bands[-1]
