from datetime import date
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import streamlit as st

from voltaic import db, grading, stats, tasks


def update_state_vars():
    if 'area1' not in st.session_state:
        st.session_state['area1'] = None
    if 'area2' not in st.session_state:
        st.session_state['area2'] = None
    if 'task' not in st.session_state:
        st.session_state['task'] = None
    if 'area2_options' not in st.session_state:
        st.session_state['area2_options'] = tasks.get_area2s(
            area1=st.session_state['area1'])
    if 'task_options' not in st.session_state:
        st.session_state['task_options'] = tasks.get_tasks(
            area1=st.session_state['area1'],
            area2=st.session_state['area2'])
    # if the DO exist, update them based on the choices
    st.session_state['area2_options'] = tasks.get_area2s(
            area1=st.session_state['area1'])
    st.session_state['task_options'] = tasks.get_tasks(
            area1=st.session_state['area1'],
            area2=st.session_state['area2'])


# def main():
#     update_state_vars()
#     with st.form('data_input'):
#         row = st.columns([1,1,2,1])
#         row[0].selectbox(
#             label='Area1', 
#             options=tasks.get_area1s(), 
#             index=st.session_state['area1'],
#             on_change=update_state_vars,
#             key='area1')
#         row[1].selectbox(
#             label='Area2', 
#             options=st.session_state['area2_options'],
#             index=st.session_state['area2'],
#             on_change=update_state_vars,
#             key='area2')
#         row[2].selectbox(
#             label='Task', 
#             options=st.session_state[''],
#             index=st.session_state[''],
#             key='task')
#         row[3].text_input('Score')

#         st.form_submit_button('Save Result')


def save_scores(date, area1, area2, task, scores) -> None:
    for i in range(5):
        db.add_play(
            date=date.strftime('%Y-%M-%d'),
            area1=area1,
            area2=area2,
            task=task,\
            score=scores[i])


def save_notes(date, task, notes) -> None:
    notes = [x.strip() for x in notes.split('\n')]
    for note in notes:
        if note != '':
            db.add_note(date, task, note)


def get_grade_image_path(grade: str) -> str:
    return f'images/{grade}.png'


def is_valid_int(x: str) -> bool:
    try:
        _ = int(x)
        return True
    except:
        return False


def data_input(
    dt: date,
    area1: str,
    area2: str,
    task: str,
    scores: List[str],
    notes: str
) -> bool:
    all_scores = all(is_valid_int(x) for x in scores)
    if not all_scores and not notes:
        st.warning('You need to either provide scores or notes to submit data.')
        return False
    if all_scores:
        save_scores(dt.strftime('%Y-%m-%d'), str(area1), str(area2), str(task), [int(x) for x in scores])
    if notes:
        save_notes(dt.strftime('%Y-%m-%d'), str(task), str(notes))
    return True


def data_and_input():
    st.header('Data Input & Control')

    rows = st.columns([1,1.3,1.3,2.4,.8,.8,.8,.8,.8])
    
    dt = rows[0].date_input('Date', date.today())

    # Step 1: Load `area1` options from `tasks.get_area1s()`
    area1_options = tasks.get_area1s()
    area1 = rows[1].selectbox("Select Area 1", area1_options)

    # Step 2: Conditionally populate `area2` based on selected `area1`
    if area1:
        area2_options = tasks.get_area2s(area1)
        area2 = rows[2].selectbox("Select Area 2", area2_options)
    else:
        area2 = None

    # Step 3: Conditionally populate `task` based on selected `area1` and `area2`
    if area1 and area2:
        task_options = tasks.get_tasks(area1, area2)
        task = rows[3].selectbox("Select Task", task_options)
    else:
        task = None

    s1 = rows[4].text_input('Score 1')
    s2 = rows[5].text_input('Score 2')
    s3 = rows[6].text_input('Score 3')
    s4 = rows[7].text_input('Score 4')
    s5 = rows[8].text_input('Score 5')

    scores = [s1, s2, s3, s4, s5]

    notes = st.text_area('Task Notes:')

    # Submit form
    if st.button('Submit'):
        updated = data_input(
            dt=dt,
            area1=area1,
            area2=area2,
            task=task,
            scores=scores,
            notes=notes)
        # TODO: clear inputs if updated
    
    return dt, area1, area2, task, scores, notes


def progression_table(task: str, df: pd.DataFrame):
    if len(df.date.unique()) >= 3:
        n_cols = 3
    elif len(df.date.unique()) == 2:
        n_cols = 2
    elif len(df.date.unique()) == 1:
        n_cols = 1
    else:
        return
    
    dates = list(reversed(sorted(df.date.unique())))
    j2date = {j: dates[-j] for j in range(1, n_cols+1)}
    row_items = ['Date', 'Max', 'Mean', 'Std', 'Std/Mean', 'Rank']

    for i, title in enumerate(row_items):
        cols = st.columns(n_cols+1)  # +1 for the name column
        with cols[0]:
            st.markdown(f'**{title}**')
        for j in range(1, n_cols+1):
            date = j2date[j]
            dfd = df[df.date == date]
            with cols[j]:
                if title == 'Date':
                    st.markdown(f'**{date}**')
                elif title == 'Max':
                    st.text(int(round(dfd.score.max(), 0)))
                elif title == 'Mean':
                    st.text(int(round(dfd.score.mean(), 0)))
                elif title == 'Std':
                    st.text(int(round(dfd.score.std(), 0)))
                elif title == 'Std/Mean':
                    st.text(str(int(round(dfd.score.std() / dfd.score.mean() * 100))) + '%')
                elif title == 'Rank':
                    grade = grading.grade(task, dfd.score.mean())
                    img_path = get_grade_image_path(grade)
                    image = Image.open(img_path)
                    st.image(image, caption='', width=50)


def progression(task: str):
    st.header(f'{task}')

    c1, c2 = st.columns([5, 5])
    df = db.get_task_data(task)

    with c1:
        progression_table(task, df)

    with c2:
        df['color'] = df.score.apply(
            lambda x: grading.grade2color[grading.grade(task, x)])
        fig, ax = plt.subplots(figsize=(12, 4))
        sns.scatterplot(
            df,
            x='date',
            y='score',
            c=df.color,
            ax=ax)
        sns.lineplot(
            data=df.groupby('date').mean(numeric_only=True).reset_index(),
            x='date',
            y='score',
            c='black',
            ax=ax)
        ax.set_title(task)
        ax.set_xlabel('')
        ax.set_ylabel('')
        low = min(df.score.min(), grading.score(task, 'Platinum'))
        high = max(df.score.max(), grading.score(task, 'Immortal'))
        range_ = high - low
        offset = int(math.ceil(.1 * range_))
        ax.set_ylim((low - offset, high + offset))
        n = len(df.date.unique())
        for grade in grading.grades:
            plt.plot(
                range(n), 
                [grading.score(task, grade)] * n, 
                c=grading.grade2color[grade],
                linestyle='--')
        st.pyplot(fig)

    training_notes = db.get_notes(task)
    if training_notes is not None and len(training_notes) > 0:
        st.markdown('**Training Notes**')
        for tn in training_notes:
            c1, c2, c3 = st.columns([1, 5, 1])
            with c1:
                st.text(tn['Date'])
            with c2:
                st.text(tn['Note'])
            with c3:
                st.text('Delete Link')


def training_targets(area1: str):
    targets = stats.training_targets(area1)
    st.header(f'Training targets for {area1}')
    col_widths = [3,1,1,1,1,1,1]
    c1, c2, c3, c4, c5, c6, c7 = st.columns(col_widths)
    with c1:
        st.markdown('**Task**')
    with c2:
        st.markdown('**Mean**')
    with c3:
        st.markdown('**Max**')
    with c4:
        st.markdown('**Std**')
    with c5:
        st.markdown('**Std / Mean**')
    with c6:
        st.markdown('**Target (= Max)**')
    with c7:
        st.markdown('**Target Grade**')
    for x in targets:
        c1, c2, c3, c4, c5, c6, c7 = st.columns(col_widths)
        with c1:
            st.text(x['task'])
        with c2:
            st.text(x['mean'])
        with c3:
            st.text(x['max'])
        with c4:
            st.text(x['std'])
        with c5:
            st.text(x['std/mu'])
        with c6:
            st.text(x['max'])
        with c7:
            img_path = get_grade_image_path(x['grade'])
            image = Image.open(img_path)
            st.image(image, caption='', width=50)


def main():
    db.init()

    st.set_page_config(layout="wide")
    sns.set_style("dark")

    dt, area1, area2, task, scores, notes = data_and_input()    

    progression(task)
    # here, a table, similar to the voltaic table, but with my best average of five runs

    training_targets(area1)

    # here a table of all plays that can be deleted from the table


if __name__ == '__main__':
    main()
