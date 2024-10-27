import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
states_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/survey.csv')

unique_survey_years = []
for i in survey_data['year'].unique:
    col = pd.read_csv(f'cache/col_{i}.csv')
    unique_survey_years.append(col)

col_data = pd.concat(unique_survey_years, ignore_index=True)

survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)
survey_states_combined = survey_data.merge(states_data, left_on = "If you're in the U.S., what state do you work in?", right_on = 'State', how = 'inner')
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']
combined = survey_states_combined.merge(col_data, left_on=['year', 'full_city'], right_on = ['year', 'full_city'], how='inner')

combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined['_annual_salary_adjusted'] = combined.apply(lambda row: row['__annual_salary_cleaned'] * (100 / row['Cost of Living Index']), axis = 1)
combined.to_csv("cache/survey_dataset.csv", index = False)

annual_salary_adjusted_by_location_and_age = combined.pivot_table(index = '_full_city', columns = 'How old are you?', values = '_annual_salary_adjusted', aggfunc= 'mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

annual_salary_adjusted_by_location_and_education = combined.pivot(index = '_full_city', columns = 'What is your highest level of education completed?', value = '_annual_salary_adjusted', aggfunc = 'mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
st.write(annual_salary_adjusted_by_location_and_education)

