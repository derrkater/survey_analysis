LANGUAGE = 'en'

DATA_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/data/{}'.format(LANGUAGE)
OUTPUT_PATH = '/Users/derrkater/PycharmProjects/survey_analysis/output/{}'.format(LANGUAGE)

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
