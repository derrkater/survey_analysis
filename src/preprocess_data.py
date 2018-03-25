import re, glob, os
import pandas as pd

from config import DATA_PATH


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
    from config import COLUMNS_TO_DROP_EN
    from translation import get_score_dict, get_education_dict, RENAMING_DICT_EN, BOOLEAN_DICT_EN

    SCORE_DICT = get_score_dict(language)
    EDUCATION_DICT = get_education_dict(language)
    RENAMING_DICT = RENAMING_DICT_EN
    BOOLEAN_DICT = BOOLEAN_DICT_EN
    COLUMNS_TO_DROP = COLUMNS_TO_DROP_EN

    return df.rename(columns=RENAMING_DICT) \
        .dropna(axis=1) \
        .drop(columns=COLUMNS_TO_DROP) \
        .applymap(lambda x: SCORE_DICT.get(x, x)) \
        .applymap(lambda x: BOOLEAN_DICT.get(x, x)) \
        .applymap(lambda x: EDUCATION_DICT.get(x, x))


def preprocess_control_questions(df, control_1, control_2):
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
    from config import TIME_THRESHOLD_EN, MIN_YEAR, MAX_YEAR
    time_threshold = TIME_THRESHOLD_EN

    df = preprocess_initial(df, language)

    control_1, knowledge_1, control_2, knowledge_2 = df.columns[5:9]
    person_1 = knowledge_1.replace('Know', '')
    person_2 = knowledge_2.replace('Know', '')

    df = preprocess_control_questions(df, control_1, control_2)
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
        df, person_1, person_2 = preprocess(df, 'en')

        if verbose:
            browse_data(df)

        interview = '{}-{}'.format(person_1, person_2)

        truetemp_data[interview] = list(df.TruetempKnow)
        dfs[interview] = df

    return dfs, truetemp_data
