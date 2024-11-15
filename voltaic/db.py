import os
import sqlite3
from typing import Dict, List

import pandas as pd


def init():
    create_schema()


def clear_data():
    os.remove('voltaic.db')


def get_connection():
    return sqlite3.connect('voltaic.db')


def create_schema():
    statements = ["""
    CREATE TABLE IF NOT EXISTS plays(
        dt DATE,
        area1 VARCHAR(9),
        area2 VARCHAR(50),
        task VARCHAR(100),
        score INT
    );""",
    """
    CREATE TABLE IF NOT EXISTS notes(
        dt DATE,
        task VARCHAR(100),
        note VARCHAR(500)
    );
    """,
    ]
    with get_connection() as conn:
        cur = conn.cursor()
        for statement in statements:
            cur.execute(statement)
        conn.commit()


def get_all() -> pd.DataFrame:
    sql = 'SELECT * FROM plays;'
    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute(sql)
        data = res.fetchall()
        data = zip_data(data)
        return pd.DataFrame(data)


def add_play(
        date: str,
        area1: str,
        area2: str,
        task: str,
        score: int
) -> None:
    data = {
        'dt': date,
        'area1': area1,
        'area2': area2,
        'task': task,
        'score': score
    }
    sql = 'INSERT INTO plays VALUES(:dt, :area1, :area2, :task, :score);'
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()


def add_note(
        date: str,
        task: str,
        note: str
) -> None:
    data = {'dt': date, 'task': task, 'note': note}
    sql = 'INSERT INTO notes VALUES(:dt, :task, :note);'
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()


def get_task_data(task: str) -> pd.DataFrame:
    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute('SELECT * FROM plays WHERE task = :task;', [task])
        data = res.fetchall()
        data = zip_data(data)
        return pd.DataFrame(data)


def get_notes(task: str) -> List[Dict]:
    with get_connection() as conn:
        cur = conn.cursor()
        res = cur.execute('SELECT * FROM notes WHERE task = :task;', [task])
        data = res.fetchall()
        return [dict(zip(['Date', 'Task', 'Note'], x)) for x in data]


def zip_data(data):
    attrs = ['date', 'area1', 'area2', 'task', 'score']
    return [dict(zip(attrs, x)) for x in data]
