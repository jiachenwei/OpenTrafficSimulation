import re

import seaborn as sns

import sys

from example import *

from matplotlib import pyplot as plt

import os

from pprint import pprint as pp

mod = sys.argv[1]

path = sys.argv[2]

if path[-1] is not '/':
    path = path + '/'
    pass

dirs = os.listdir(path)


def plot(mean_matrix, standard_deviation_matrix):
    sns.set()
    plt.clf()
    plt.figure(figsize=(10, 8), dpi=80)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    ax = sns.heatmap(mean_matrix, annot=True, fmt=".1f", vmin=0, vmax=MAX_SPEED,
                     cmap="jet_r")  # , cmap="RdBu_r", center=MAX_SPEED/2
    ax.set_title('平均速度')
    ax.set_xlabel('渗透率')
    ax.set_ylabel('车流密度')
    label_y = ax.get_yticklabels()
    plt.setp(label_y, rotation=360, horizontalalignment='right')
    label_x = ax.get_xticklabels()
    plt.setp(label_x, rotation=45, horizontalalignment='right')
    plt.tight_layout()
    plt.savefig(path + 'heatmap_mean' + '.jpg')
    plt.close()

    plt.clf()
    plt.figure(figsize=(10, 8), dpi=80)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    ax = sns.heatmap(standard_deviation_matrix, annot=True, fmt=".2f", vmin=0, vmax=1, cmap="bwr", center=0.2)  # cool
    ax.set_title('标准差')
    ax.set_xlabel('渗透率')
    ax.set_ylabel('车流密度')
    label_y = ax.get_yticklabels()
    plt.setp(label_y, rotation=360, horizontalalignment='right')
    label_x = ax.get_xticklabels()
    plt.setp(label_x, rotation=45, horizontalalignment='right')
    plt.tight_layout()
    plt.savefig(path + 'heatmap_standard_deviation' + '.jpg')
    plt.close()


if mod == "-one":
    dirs_csv = []
    for _ in dirs:
        if ('csv' in _) and ('data' in _):
            dirs_csv.append(_)
            pass
        pass
    tmp = []
    tmp.extend(dirs_csv[88:99])
    tmp.extend(dirs_csv[:88])
    tmp.extend(dirs_csv[99:])
    dirs_csv = tmp
    pp(dirs_csv)

    list_file = []
    list_parameter = []
    for d in dirs_csv:
        k = d
        v = re.findall(r"\d+\.?\d*", d)
        for _ in range(len(v)):
            v[_] = float(v[_])
            pass
        list_file.append(k)
        list_parameter.append(v)
        pass

    ret = []
    max_count = len(list_file)
    count = 0
    for k, v in zip(list_file, list_parameter):
        count += 1
        print("(" + str(count) + "/" + str(max_count) + ")  " + "wait..." + time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                          time.localtime()))
        data = pd.read_csv(path + k,
                           sep=',',
                           header=0,
                           index_col=0,
                           dtype=np.float64)
        data = np.array(data['v'][data['time'] > SAMPLING_TIME]) * 3.6

        mean = np.mean(data)
        standard_deviation = 2 * ((np.sum(
            np.power((data - mean) / MAX_SPEED, 2)
        ) / len(data)) ** 0.5)
        v.extend([mean, standard_deviation])
        ret.append(v)
        pass

    cols = ['traffic_density', 'permeability', 'mean', 'standard_deviation']
    ret = pd.DataFrame(ret, columns=cols, dtype='double')
    ret.to_csv(path + 'result' + '.csv', sep=',', index=False)

    cols = ret['permeability'].unique()
    index = ret['traffic_density'].unique()
    mean_matrix = pd.DataFrame(np.array(ret['mean']).reshape(11, -1), index=index, columns=cols)
    standard_deviation_matrix = pd.DataFrame(np.array(ret['standard_deviation']).reshape(11, -1), index=index,
                                             columns=cols)
    plot(mean_matrix, standard_deviation_matrix)
elif mod == "-summary":
    mean_matrix = None
    standard_deviation_matrix = None
    ret = None
    dirs_csv = []
    for _ in dirs:
        file_name, file_type = os.path.splitext(_)
        if file_type == '':
            tmp = path + _ + '/' + 'result.csv'
            print(tmp)
            dirs_csv.append(tmp)
            pass
        pass
    if not dirs_csv:
        exit()
    for _ in dirs_csv:
        data = pd.read_csv(_,
                           sep=',',
                           header=0,
                           dtype=np.float64)

        if ret is None:
            ret = data
        else:
            ret['mean'] = ret['mean'] + data['mean']
            ret['standard_deviation'] = ret['standard_deviation'] + data['standard_deviation']
            pass
        pass

    ret['mean'] = ret['mean'] / len(dirs_csv)
    ret['standard_deviation'] = ret['standard_deviation'] / len(dirs_csv)
    ret = pd.DataFrame(ret, dtype='double')
    print(ret)
    ret.to_csv(path + 'result' + '.csv', sep=',', index=False)
    cols = ret['permeability'].unique()
    index = ret['traffic_density'].unique()
    mean_matrix = pd.DataFrame(np.array(ret['mean']).reshape(11, -1), index=index, columns=cols)
    standard_deviation_matrix = pd.DataFrame(np.array(ret['standard_deviation']).reshape(11, -1), index=index,
                                             columns=cols)
    plot(mean_matrix, standard_deviation_matrix)
elif mod == '-vf':
    pass
else:
    exit()
