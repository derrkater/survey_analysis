import os, json
import numpy as np
from collections import defaultdict, OrderedDict
from tabulate import tabulate

from config import DATA_PATH


def load_data(language='pl'):
    return json.load(open(os.path.join(DATA_PATH, language, 'data.json'), encoding='utf-8'))


def knowledge(story):
    return '{}Know'.format(story)


def get_mean_answers_for_all_stories(dfs):
    labels = ['group', 'q1', 'std1', 'q2', 'std2']

    means_data = []
    for interview, df in dfs.items():
        person_1, person_2 = interview.split('-')
        q1 = df[knowledge(person_1)]
        q2 = df[knowledge(person_2)]
        means_data.append([interview, np.mean(q1), np.std(q1), np.mean(q2), np.std(q2)])

    print(tabulate(means_data, labels))


def get_values_histograms_dict(data):
    histograms_dict = defaultdict(lambda: defaultdict(lambda: 0))

    for group_id, interviewees in data.items():
        for interviewee in interviewees:
            for key, value in interviewee.items():
                histograms_dict[key][value] += 1

    # sort histograms
    for key, values_dict in histograms_dict.items():
        histograms_dict[key] = OrderedDict(sorted(values_dict.items()))

    return histograms_dict


if __name__ == '__main__':
    data = load_data()
    histograms_dict = get_values_histograms_dict(data)

    # with open(os.path.join(DATA_PATH, 'histograms_data.json'), 'w+') as file:
    #     json.dump(histograms_dict, file, indent=4)
