#!/usr/bin/env python
from datetime import datetime

import streamlit as st
from lesson_4_sports_program import *

st.title('AI Sports Program Planner')

with st.form(key='my_form'):
    sport = st.text_input(label='Sport: ')
    city = st.text_input(label='City: ')
    date = st.date_input("Start Day: ", datetime.now())
    start_date = date.strftime("%d %B, %Y")
    language = st.text_input(label='Language: ', value='english')
    submit_button = st.form_submit_button('Go!')

if submit_button:
    if not sport:
        st.write('Input the sport first!')
    else:
        sport_activity_input = {
            'sport': sport,
            'city': city,
            'start_date': start_date
        }

        infos_result = create_gather_infos_crew().kickoff(inputs=sport_activity_input)

        plan_input = {
            'sports_aspects_task': sports_aspects_task.output.raw,
            'location_finder_task': location_finder_task.output.raw,
            'nutrition_task': nutrition_task.output.raw,
            'mental_activity_plan_task': mental_activity_plan_task.output.raw,
            'fitness_activity_plan_task': fitness_activity_plan_task.output.raw,
            'sport': sport,
            'city': city,
            'start_date': start_date
        }

        final_result = create_plan_crew().kickoff(inputs=plan_input)
        additional_md = '# Wrap-Up and Action Points'
        report = (f'{final_result.raw}\n\n# Wrap-Up and Action Points\n'
                  f'## Mental Exercises\n{mental_activity_plan_task.output.raw}\n'
                  f'## Fitness Exercises\n{fitness_activity_plan_task.output.raw}')

        if language and language.lower() != 'english':
            translation_input = {
                'translation_input': report,
                'language': language
            }
            report = create_translation_crew().kickoff(inputs=translation_input)

        with open("output/sport/final_report.md", "w", encoding="utf-8") as file:
            file.write(report)

        st.markdown(report)
