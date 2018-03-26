import csv, glob, os, json, re
from collections import defaultdict

from config import DATA_PATH, REMOVE_CATEGORIES_PL, FILTER_OUT_LOW_PHILOSOPHY_KNOWLEDGE
from translation import SCORE_DICT_PL, TIME_DICT_PL


def is_survey_finished(interviewee):
    if interviewee and 'lastpage' in interviewee and interviewee['lastpage'] == '3':
        interviewee.pop('lastpage')
        return True


def unify_question_categories_and_answers(interviewee, q1, q2):
    interviewee['q1'] = SCORE_DICT_PL[interviewee.pop(q1)]
    interviewee['q2'] = SCORE_DICT_PL[interviewee.pop(q2)]


def has_low_philosophy_knowledge(interviewee):
    return 'filozofia2' in interviewee


def remove_philosophy(interviewee):
    if 'filozofia' in interviewee: interviewee.pop('filozofia')
    if 'filozofia2' in interviewee: interviewee.pop('filozofia2')


def preprocess_times(interviewee):
    # preprocess survey duration times
    times_regex = re.compile('groupTime.*|interviewtime')
    times = filter(times_regex.match, interviewee.keys())
    for time in times:
        interviewee[TIME_DICT_PL[time]] = float(interviewee.pop(time))

    # preprocess birth year of interviewee
    interviewee['rok'] = int(interviewee['rok'])


def read_data(language='pl'):
    files = glob.glob(os.path.join(DATA_PATH, language, '**/*.csv'))

    data = defaultdict(lambda: dict())

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:  # iso-8859-1
            reader = csv.reader(f)
            group_data = []

            headers = next(reader)
            print('headers: {}'.format(headers))
            q1, q2 = headers[8:10]
            group_id = '-'.join(headers[8:10])

            for line in reader:
                interviewee = {key: val for key, val in zip(headers, line) if val and key not in REMOVE_CATEGORIES_PL}
                is_not_philosopher = not (
                            FILTER_OUT_LOW_PHILOSOPHY_KNOWLEDGE and has_low_philosophy_knowledge(interviewee))
                if is_survey_finished(interviewee) and is_not_philosopher:
                    unify_question_categories_and_answers(interviewee, q1, q2)
                    preprocess_times(interviewee)
                    remove_philosophy(interviewee)

                    if interviewee['rok'] > 1918:
                        group_data.append(interviewee)

            data[group_id] = group_data

    return data


if __name__ == '__main__':
    data = read_data()

    with open(os.path.join(DATA_PATH, 'pl', 'data.json'), 'w+') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
