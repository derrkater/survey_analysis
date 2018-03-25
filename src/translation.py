SCORE_DICT_PL = {
    'Zdecydowanie się nie zgadzam': -2,
    'Nie zgadzam się': -1,
    'Częściowo się zgadzam, częściowo się nie zgadzam': 0,
    'Zgadzam się': 1,
    'Zdecydowanie się zgadzam': 2
}

SCORE_DICT_EN = {
    'Strongly disagree': -2,
    'Disagree': -1,
    'Neutral': 0,
    'Agree': 1,
    'Strongly agree': 2
}


def get_score_dict(language):
    if language == 'pl':
        return SCORE_DICT_PL
    elif language == 'en':
        return SCORE_DICT_EN
    else:
        raise Exception


EDUCATION_DICT_PL = {
    'gimnazjalne': 0,
    'zasadnicze zawodowe': 1,
    'średnie': 2,
    'wyższe (licencjat, inżynier, magister)': 3,
    'wyższe (doktorat lub więcej)': 4
}

EDUCATION_DICT_EN = {
    'Other': -1,
    'Did not complete High School': 0,
    'High School/GED': 1,
    'Some College': 2,
    "Bachelor's degree": 3,
    "Master's degree": 4,
    'Advanced Graduate work or Doctoral degree': 5
}


def get_education_dict(language):
    if language == 'pl':
        return EDUCATION_DICT_PL
    elif language == 'en':
        return EDUCATION_DICT_EN
    else:
        raise Exception


TIME_DICT_PL = {
    'groupTime8009': 't1',
    'groupTime8010': 't2',
    'groupTime8011': 'misc',
    'groupTime8018': 't1',
    'groupTime8017': 't2',
    'groupTime8019': 'misc',
    'groupTime8020': 't1',
    'groupTime8021': 't2',
    'groupTime8022': 'misc',
    'groupTime8024': 't1',
    'groupTime8023': 't2',
    'groupTime8025': 'misc',
    'interviewtime': 'total_time'
}

TIME_DICT_EN = {
    'groupTime8009': 't1',
    'groupTime8010': 't2',
    'groupTime8011': 'misc',
    'groupTime8018': 't1',
    'groupTime8017': 't2',
    'groupTime8019': 'misc',
    'groupTime8020': 't1',
    'groupTime8021': 't2',
    'groupTime8022': 'misc',
    'groupTime8024': 't1',
    'groupTime8023': 't2',
    'groupTime8025': 'misc',
    'interviewtime': 'total_time'
}


RENAMING_DICT_EN = {
    'M1': 'gender',
    'M2': 'year',
    'M3': 'education',
    'M3[other]': 'education_other',
    'M4': 'philosophy_education',
    'M5': 'philosophy_education_level',
    'M6': 'native_speaker',
}

BOOLEAN_DICT_EN = {'Yes': True, 'No': False}
