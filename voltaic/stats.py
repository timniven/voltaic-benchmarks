import math
from typing import Dict, List

import numpy as np
import pandas as pd

from voltaic import db, grading, tasks


def training_target(task: str) -> Dict:
    df = db.get_task_data(task)
    df = df.sort_values('date', ascending=False).iloc[0:10]
    mu = df.score.mean()
    std = df.score.std()
    mx = df.score.max()
    grade = grading.grade(task, mx)
    return {
        'task': task, 
        'mean': int(round(mu, 0)),
        'max': mx,
        'std': int(round(std, 0)),
        'std/mu': f'{int(round(std / mu * 100, 0))}%',
        'grade': grade,
    }


def training_targets(area1: str) -> List[Dict]:
    area2s = tasks.get_area2s(area1)
    tt = []
    for area2 in area2s:
        for t in tasks.get_tasks(area1, area2):
            target = training_target(t)
            tt.append(target)
    return tt   
