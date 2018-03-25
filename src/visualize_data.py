import os
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from operator import itemgetter
from tabulate import tabulate

from config import OUTPUT_PATH
from translation import EDUCATION_DICT_PL

from analyze_data import load_data, get_values_histograms_dict


def plot_histogram(category, title, output_filename, numerical_labels=True, sort_dict=None):
    data = histograms_dict[category]
    if sort_dict:
        data = OrderedDict(sorted(data.items(), key=lambda x: sort_dict[x]))

    if numerical_labels:
        x_data = data.keys()
    else:
        x_data = range(len(data.keys()))

    plt.bar(x_data, data.values())
    plt.title(title)

    if not numerical_labels:
        plt.xticks(x_data, data.keys(), rotation=45)

    plt.savefig(os.path.join(OUTPUT_PATH, output_filename))
    plt.clf()


def plot_piechart(category, title, output_filename, sort_dict=None):
    data = histograms_dict[category]
    if sort_dict:
        data_items_with_order_parameter = [(i[0], i[1], sort_dict[i[0]]) for i in data.items()]
        sorted_data = [(i[0], i[1]) for i in sorted(data_items_with_order_parameter, key=itemgetter(2))]
        data = OrderedDict(sorted_data)

    fracs = [f / sum(data.values()) for f in data.values()]
    explode = (0, 0.3, 0, 0, 0.3)

    plt.pie(data.values(), autopct='%1.1f%%', explode=explode, pctdistance=1.2)
    plt.title(title)
    plt.axis('equal')
    plt.legend(data.keys(), loc='lower center')

    plt.savefig(os.path.join(OUTPUT_PATH, output_filename))
    plt.show()


def plot_truetemp_dependence_on_preceding_story(data, filename='mean_truetemp.png'):
    labels = ['preceding', 'truetemp mean', 'truetemp std']

    preceding_data = []
    for group, answers in data.items():
        preceding_data.append([group, np.mean(answers), np.var(answers)])

    print(tabulate(preceding_data, labels))

    answer = [d[1] for d in preceding_data]
    std = [d[2] for d in preceding_data]

    plt.figure(figsize=(10, 7), dpi=300)
    plt.errorbar(range(3), answer, yerr=std, fmt='o', capsize=4)
    plt.xticks(range(3), ('M-T', 'T-(M/C)', 'C-T'), fontsize=12)
    plt.grid(True)

    plt.title('Średnia odpowiedź na Truetemp w różnych wersjach ankiety', fontsize=20, y=1.05)
    plt.xlabel('Wersja ankiety\n(M-Moneta, T-Truetemp, C-Chemiczka)', fontsize=15)
    plt.ylabel('Średni wynik Truetempa\n(-1.0-nie zgadzam się, 1.0-zgadzam się)', fontsize=15)

    annotation_positions = ((.1, .1), (.1, .1), (-.53, -.05))
    d = 0.1
    for x, y, s, a in zip(range(3), answer, std, annotation_positions):
        plt.annotate('{:.3f} $\pm$ {:.3f}'.format(y, s), xy=[x + d, y + d], fontsize=12)

    plt.ylim(-2, 2)
    plt.xlim(-.1, 2.1)
    plt.savefig(os.path.join(OUTPUT_PATH, filename))


if __name__ == '__main__':
    histograms_dict = get_values_histograms_dict(load_data())

    # birth year
    # plot_histogram('rok', 'Rok urodzenia ankietowanych', 'year.png')

    # sex
    # plot_histogram('plec', 'Płeć ankietowanych', 'sex.png', numerical_labels=False)

    # education
    # plot_piechart('wyksztalcenie', 'Wykształcenie ankietowanych', 'education_pie.png', sort_dict=EDUCATION_DICT)

    # total time

    data = [float(i) for i in histograms_dict['t1']]
    print(data)

    hist, edges = np.histogram(data, bins=40)
    # hist = hist[:12]
    # edges = edges[:13]
    print(hist)
    print(edges)

    plt.bar(edges[:-1], hist, width=50, align='edge')
    plt.xlim(min(edges), max(edges))

    plt.savefig(os.path.join(OUTPUT_PATH, 'total_time.png'))
    plt.clf()
