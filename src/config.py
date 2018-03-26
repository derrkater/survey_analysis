DATA_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/data'
OUTPUT_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/output'

FILTER_OUT_LOW_PHILOSOPHY_KNOWLEDGE = False

REMOVE_CATEGORIES_PL = [
    'id',  #
    'submitdate',  # irrelevant
    'startlanguage',  # all 'pl'
    'startdate',  #
    'datestamp',  #
    'ipaddr',  # irrelevant
    'refurl'  # irrelevant
]

REMOVE_CATEGORIES_EN = [
    'id',
    'submitdate',
    'startlanguage',
    'startdate',
    'datestamp',
    'ipaddr',
    'lastpage'
]

def get_remove_categories(language):
    if language == 'pl':
        return REMOVE_CATEGORIES_PL
    elif language == 'en':
        return REMOVE_CATEGORIES_EN
    else:
        raise Exception


TIME_THRESHOLD_EN = 60

TIME_THRESHOLD_PL = 60

def get_time_threshold(language):
    if language == 'pl':
        return TIME_THRESHOLD_PL
    elif language == 'en':
        return TIME_THRESHOLD_EN
    else:
        raise Exception


MIN_YEAR = 1910

MAX_YEAR = 2005
