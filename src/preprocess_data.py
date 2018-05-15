import re, glob, os
import pandas as pd

from config import DATA_PATH, get_time_threshold, MIN_YEAR, MAX_YEAR, get_remove_categories
from translation import STORY_TO_PERSON, get_score_dict, get_education_dict, get_renaming_dict, get_boolean_dict

def browse_data(df):
    print(df.columns)

    possible_values = {column: df[column].unique() for column in df.columns}
    for column, values in possible_values.items():
        if len(values) < 7:
            print(column, values)
        else:
            try:
                print(column, min(values), max(values))
            except:
                print('ERROR', column, values)


def preprocess_initial(df, language):

    score_dict = get_score_dict(language)
    boolean_dict = get_boolean_dict(language)
    education_dict = get_education_dict(language)

    return df.rename(columns=get_renaming_dict(language)) \
        .drop(columns=get_remove_categories(language)) \
        .dropna(axis=1, how='all') \
        .applymap(lambda x: score_dict.get(x, x)) \
        .applymap(lambda x: boolean_dict.get(x, x)) \
        .applymap(lambda x: education_dict.get(x, x))


def preprocess_control_questions(df, control_1, control_2):
    """
    Drops interviewees that have answered false in control questions (did not read the story).
    :param df:
    :param control_1: 'ControlTruetemp' or 'ControlCoinflip' or 'ControlChemist'
    :param control_2: 'ControlTruetemp' or 'ControlCoinflip' or 'ControlChemist'
    :return: df
    """
    df = df[df[control_1]]
    df = df[df[control_2]]
    return df.drop(columns=[control_1, control_2])


def preprocess_not_active(df):
    df = df[df.native_speaker]
    return df.drop(columns=['native_speaker'])


def preprocess_by_interviewee_age(df, year_min, year_max):
    return df[df.year < year_max][df.year > year_min]


def preprocess_by_interview_time(df, interview_time_threshold):
    return df[df.interviewtime > interview_time_threshold]


def preprocess_times(df, story_1, story_2):
    times_regex = re.compile('groupTime.*')
    times = list(filter(times_regex.match, df.columns))
    interviewee_info_time, task_info_time_1, question_time_1, task_info_time_2, question_time_2 = times

    time_renaming_dict = {
        interviewee_info_time: 'interviewee_info_time',
        question_time_1: '{}_time'.format(story_1),
        question_time_2: '{}_time'.format(story_2)
    }

    return df.rename(columns=time_renaming_dict) \
        .drop(columns=[task_info_time_1, task_info_time_2])


def preprocess(df, language):
    """

    :param df: pandas DataFrame with columns:
        * pl    "id","submitdate","lastpage","startlanguage","startdate","datestamp","ipaddr","refurl","ch","t","rok","plec","wyksztalcenie","filozofia","filozofia2","interviewtime","groupTime8020","chTime","groupTime8021","tTime","groupTime8022","rokTime","plecTime","wyksztalcenieTime","filozofiaTime","filozofia2Time"
        * en    "id","submitdate","lastpage","startlanguage","startdate","datestamp","ipaddr","refurl","M1","M2","M3","M3[other]","M4","M5","M6","I1","Truetemp","ControlTruetemp","TruetempKnow","I2","Coinflip","ControlCoinflip","CoinflipKnow","interviewtime","groupTime8106","M1Time","M2Time","M3Time","M4Time","M5Time","M6Time","groupTime8109","I1Time","groupTime8110","TruetempTime","ControlTruetempTime","TruetempKnowTime","groupTime8108","I2Time","groupTime8107","CoinflipTime","ControlCoinflipTime","CoinflipKnowTime"
    :param language: 'en'/'pl'
    :return:
    """


    if language == 'pl':
        story_1, story_2 = df.columns[8:10]
        person_1 = STORY_TO_PERSON[story_1]
        person_2 = STORY_TO_PERSON[story_2]

    elif language == 'en':
        control_1, knowledge_1, control_2, knowledge_2 = df.columns[5:9]
        person_1 = knowledge_1.replace('Know', '')
        person_2 = knowledge_2.replace('Know', '')

        df = preprocess_control_questions(df, control_1, control_2)

    else:
        raise Exception

    df = preprocess_initial(df, language)
    print(df.columns)

    time_threshold = get_time_threshold(language)
    df = preprocess_not_active(df)
    df = preprocess_by_interviewee_age(df, MIN_YEAR, MAX_YEAR)
    df = preprocess_by_interview_time(df, time_threshold)
    df = preprocess_times(df, person_1, person_2)

    return df, person_1, person_2


def preprocess_pipeline(language, verbose=False):
    files = glob.glob(os.path.join(DATA_PATH, language, '**/*.csv'))

    truetemp_data = dict()
    dfs = dict()
    for file in files:
        df = pd.read_csv(file)
        df, person_1, person_2 = preprocess(df, language)

        if verbose:
            browse_data(df)

        interview = '{}-{}'.format(person_1, person_2)

        truetemp_data[interview] = list(df.TruetempKnow)
        dfs[interview] = df

    return dfs, truetemp_data
