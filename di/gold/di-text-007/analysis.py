import numpy as np 
import pandas as pd
# Some helper functions to make our plots cleaner with Plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import iplot


def gen_xaxis(title):
    """
    Creates the X Axis layout and title
    """
    xaxis = dict(
            title=title,
            titlefont=dict(
                color='#AAAAAA'
            ),
            showgrid=False,
            color='#AAAAAA',
            )
    return xaxis


def gen_yaxis(title):
    """
    Creates the Y Axis layout and title
    """
    yaxis=dict(
            title=title,
            titlefont=dict(
                color='#AAAAAA'
            ),
            showgrid=False,
            color='#AAAAAA',
            )
    return yaxis


def gen_layout(charttitle, xtitle, ytitle, lmarg, h, annotations=None):  
    """
    Creates whole layout, with both axis, annotations, size and margin
    """
    return go.Layout(title=charttitle, 
                     height=h, 
                     width=800,
                     showlegend=False,
                     xaxis=gen_xaxis(xtitle), 
                     yaxis=gen_yaxis(ytitle),
                     annotations = annotations,
                     margin=dict(l=lmarg),
                    )


def gen_bars(data, color, orient):
    """
    Generates the bars for plotting, with their color and orient
    """
    bars = []
    for label, label_df in data.groupby(color):
        if orient == 'h':
            label_df = label_df.sort_values(by='x', ascending=True)
        if label == 'a':
            label = 'lightgray'
        bars.append(go.Bar(x=label_df.x,
                           y=label_df.y,
                           name=label,
                           marker={'color': label},
                           orientation = orient
                          )
                   )
    return bars


def gen_annotations(annot):
    """
    Generates annotations to insert in the chart
    """
    if annot is None:
        return []
    
    annotations = []
    # Adding labels
    for d in annot:
        annotations.append(dict(xref='paper', x=d['x'], y=d['y'],
                           xanchor='left', yanchor='bottom',
                           text= d['text'],
                           font=dict(size=13,
                           color=d['color']),
                           showarrow=False))
    return annotations


def generate_barplot(text, annot_dict, orient='v', lmarg=120, h=400):
    """
    Generate the barplot with all data, using previous helper functions
    """
    layout = gen_layout(text[0], text[1], text[2], lmarg, h, gen_annotations(annot_dict))
    fig = go.Figure(data=gen_bars(barplot, 'color', orient=orient), layout=layout)
    return iplot(fig)

# Loading the multiple choices dataset, we will not look to the free form data on this study
mc = pd.read_csv('../multipleChoiceResponses.csv', low_memory=False)
# Separating questions from answers
# This Series stores all questions
mcQ = mc.iloc[0,:]
# This DataFrame stores all answers
mcA = mc.iloc[1:,:]
# removing everyone that took less than 4 minutes or more than 600 minutes to answer the survey
less3 = mcA[round(mcA.iloc[:,0].astype(int) / 60) <= 4].index
mcA = mcA.drop(less3, axis=0)
more300 = mcA[round(mcA.iloc[:,0].astype(int) / 60) >= 600].index
mcA = mcA.drop(more300, axis=0)

# removing gender trolls, because we noticed from other kernels thata there are some ouliers here
gender_trolls = mcA[(mcA.Q1 == 'Prefer to self-describe') | (mcA.Q1 == 'Prefer not to say')].index
mcA = mcA.drop(list(gender_trolls), axis=0)

# removing student trolls, because a student won't make more than 250k a year.
student_trolls = mcA[((mcA.Q6 == 'Student') & (mcA.Q9 > '500,000+')) | \
                     ((mcA.Q6 == 'Student') & (mcA.Q9 > '400-500,000')) | \
                     ((mcA.Q6 == 'Student') & (mcA.Q9 > '300-400,000')) | \
                     ((mcA.Q6 == 'Student') & (mcA.Q9 > '250-300,000'))].index
mcA = mcA.drop(list(student_trolls), axis=0)

# dropping all NaN and I do not wish to disclose my approximate yearly compensation, because we are only interested in respondents that revealed their earnings
mcA = mcA[~mcA.Q9.isnull()].copy()
not_disclosed = mcA[mcA.Q9 == 'I do not wish to disclose my approximate yearly compensation'].index
mcA = mcA.drop(list(not_disclosed), axis=0)
# Creating a table with personal data
personal_data = mcA.iloc[:,:13].copy()

# renaming columns
cols = ['survey_duration', 'gender', 'gender_text', 'age', 'country', 'education_level', 'undergrad_major', 'role', 'role_text',
        'employer_industry', 'employer_industry_text', 'years_experience', 'yearly_compensation']
personal_data.columns = cols

# Drop text and survey_duration columns 
personal_data.drop(['survey_duration', 'gender_text', 'role_text', 'employer_industry_text'], axis=1, inplace=True)
from pandas.api.types import CategoricalDtype

# transforming compensation into category type and ordening the values
categ = ['0-10,000', '10-20,000', '20-30,000', '30-40,000', '40-50,000',
         '50-60,000', '60-70,000', '70-80,000', '80-90,000', '90-100,000',
         '100-125,000', '125-150,000', '150-200,000', '200-250,000', '250-300,000',
         '300-400,000', '400-500,000', '500,000+']
cat_type = CategoricalDtype(categories=categ, ordered=True)
personal_data.yearly_compensation = personal_data.yearly_compensation.astype(cat_type)
# Doing this we are transforming the category "I do not wish to disclose my approximate yearly compensation" into NaN

# transforming age into category type and sorting the values
categ = ['18-21', '22-24', '25-29', '30-34', '35-39', '40-44', 
         '45-49', '50-54', '55-59', '60-69', '70-79', '80+']
cat_type = CategoricalDtype(categories=categ, ordered=True)
personal_data.age = personal_data.age.astype(cat_type)

# transforming years of experience into category type and sorting the values
categ = ['0-1', '1-2', '2-3', '3-4', '4-5', '5-10',
         '10-15', '15-20', '20-25', '25-30', '30+']
cat_type = CategoricalDtype(categories=categ, ordered=True)
personal_data.years_experience = personal_data.years_experience.astype(cat_type)

# transforming education level into category type and sorting the values
categ = ['No formal education past high school', 'Some college/university study without earning a bachelor’s degree',
         'Professional degree', 'Bachelor’s degree', 'Master’s degree', 'Doctoral degree', 'I prefer not to answer']
cat_type = CategoricalDtype(categories=categ, ordered=True)
personal_data.education_level = personal_data.education_level.astype(cat_type)

# creating masks to identify students and not students
is_student_mask = (personal_data['role'] == 'Student') | (personal_data['employer_industry'] == 'I am a student')
not_student_mask = (personal_data['role'] != 'Student') & (personal_data['employer_industry'] != 'I am a student')

# Counting the quantity of respondents per compensation (where is student)
barplot = personal_data[is_student_mask].yearly_compensation.value_counts(sort=False).to_frame().reset_index()
barplot.columns = ['yearly_compensation', 'qty']

# mapping back to get top 20%
barplot.columns = ['x', 'y',]
barplot['highlight'] = barplot.x != '0-10,000'

# applying color
barplot['color'] = barplot.highlight.apply(lambda x: 'lightgray' if x else 'crimson')

# title and annotations
title_text = ['<b>Do Students Get Paid at All?</b><br><i>only students</i>', 'Yearly Compensation (USD)', 'Quantity of Respondents']
annotations = [{'x': 0.06, 'y': 1650, 'text': '75% of students earn up to USD 10k','color': 'crimson'}]

# ploting
generate_barplot(title_text, annotations)
