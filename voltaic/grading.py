import math
from typing import Tuple

import pandas as pd


dfg = pd.read_csv('grades.csv')


grade2color = {
    'Unranked': '#808080',
    'Platinum': '#66c2ff',
    'Diamond': '#cc66ff',
    'Ascendant': '#009933',
    'Immortal': '#990033',
}
grades = [
    'Platinum', 'Diamond', 'Ascendant', 'Immortal',
]


def grade(task: str, score: int) -> str:
    q = dfg[dfg.Task == task]
    if len(q) == 0:
        raise ValueError(task)
    row = q.iloc[0]
    if score < row.Platinum:
        return 'Unranked'
    elif score < row.Diamond:
        return 'Platinum'
    elif score < row.Ascendant:
        return 'Diamond'
    elif score < row.Immortal:
        return 'Ascendant'
    else:
        return 'Immortal'


def score(task: str, grade: str) -> int:
    q = dfg[dfg.Task == task]
    if len(q) == 0:
        raise ValueError(task)
    row = q.iloc[0]
    if grade not in row:
        raise ValueError(grade)
    return row[grade]


def plot_lims(task: str) -> Tuple[int, int]:
    low = score(task, 'Platinum')
    high = score(task, 'Immortal')
    range_ = high - low
    offset = int(math.ceil(.1 * range_))
    return low - offset, high + offset
