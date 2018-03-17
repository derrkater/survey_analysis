from collections import defaultdict


SCORE_DICT = {
    'Zdecydowanie się nie zgadzam' : -2,
    'Nie zgadzam się' : -1,
    'Częściowo się zgadzam, częściowo się nie zgadzam' : 0,
    'Zgadzam się' : 1,
    'Zdecydowanie się zgadzam': 2
}

EDUCATION_DICT = {
    'gimnazjalne' : 0,
    'zasadnicze zawodowe' : 1,
    'średnie' : 2,
    'wyższe (licencjat, inżynier, magister)' : 3,
    'wyższe (doktorat lub więcej)' : 4
}

TIME_DICT = {
    'groupTime8009' : 't1',
    'groupTime8010' : 't2',
    'groupTime8011' : 'misc',
    'groupTime8018' : 't1',
    'groupTime8017' : 't2',
    'groupTime8019' : 'misc',
    'groupTime8020' : 't1',
    'groupTime8021' : 't2',
    'groupTime8022' : 'misc',
    'groupTime8024' : 't1',
    'groupTime8023' : 't2',
    'groupTime8025' : 'misc',
    'interviewtime' : 'total_time'
}
