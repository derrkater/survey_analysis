import os, json
from collections import defaultdict, OrderedDict

from config import DATA_PATH


def load_data():
    return json.load(open(os.path.join(DATA_PATH, 'data.json'), encoding='utf-8'))


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
