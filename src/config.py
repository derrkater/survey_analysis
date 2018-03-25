DATA_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/data'
OUTPUT_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/output'

FILTER_OUT_LOW_PHILOSOPHY_KNOWLEDGE = False

REMOVE_CATEGORIES = [
    'id',  #
    'submitdate',  # irrelevant
    'startlanguage',  # all 'pl'
    'startdate',  #
    'datestamp',  #
    'ipaddr',  # irrelevant
    'refurl'  # irrelevant
]

COLUMNS_TO_DROP_EN = [
    'id',
    'submitdate',
    'startlanguage',
    'startdate',
    'datestamp',
    'ipaddr',
    'lastpage'
]

TIME_THRESHOLD_EN = 60

MIN_YEAR = 1910

MAX_YEAR = 2005
