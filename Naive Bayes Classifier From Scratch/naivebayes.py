import csv, re
import math
from sklearn.metrics import f1_score
import numpy as np
import matplotlib.pyplot as plt

dat = []
dev = []
testarr = []

f = open('stopwords.txt', 'r')
stopwords = []
for line in f.readlines()[7:]:
	stopwords.append(line.strip())
f.close()


def tokenize(text):
    return text.split()


def better_tokenize(text):
    text = text.lower()
    s_text = text.split()
    cleantext = []
    for word in s_text:
    	if word not in stopwords:
    		cleantext.append(word)
    return cleantext

def train(data, alpha = 0):
    dict_xi_0 = {}
    dict_xi_1 = {}
    dict_pxi_0 = {}
    dict_pxi_1 = {}
    pos_total = 0
    neg_total = 0

    for i in data:
        if i['class'] == '0':
            pos_total += len(tokenize(i['text']))
            for k in better_tokenize(i['text']):
                dict_xi_0[k] = dict_xi_0.get(k,0) + 1
        else:
            for k in better_tokenize(i['text']):
                dict_xi_1[k] = dict_xi_1.get(k,0) + 1
            neg_total += len(better_tokenize(i['text']))

    total = pos_total + neg_total
    py0 = pos_total / total
    py1 = neg_total / total

    #delete duplicate keys
    words = set(list(dict_xi_0.keys()) + list(dict_xi_1.keys()))
    v = len(words)

    for i in words:
        dict_pxi_0[i] = (dict_xi_0.get(i, 0) + alpha) / (pos_total+v * alpha)
        dict_pxi_1[i] = (dict_xi_1.get(i, 0) + alpha) / (neg_total+v * alpha)

    dict_total = {'py0': py0, 'py1':py1, 'pxi_0':dict_pxi_0,'pxi_1':dict_pxi_1, 'words_set':words}
    return dict_total


def classify(words, dict_total, alpha = 0):
    w = better_tokenize(words)
    words_set = dict_total['words_set']
    py0 = dict_total['py0']
    py1 = dict_total['py1']
    pxi_0 = dict_total['pxi_0']
    pxi_1 = dict_total['pxi_1']
    pos = 1
    neg = 1
    for i in w:
        if i not in words_set:
            continue
        pos = pos * pxi_0[i]
        neg = neg * pxi_1[i]
    if alpha == 0:
        py0_x = pos * py0
        py1_x = neg * py1
        if py0_x >= py1_x:
            return 0
        else:
            return 1
    else:
        py0_x = math.log10(pos * py0)
        py1_x = math.log10(neg * py1)
        if py0_x >= py1_x:
            return 0
        else:
            return 1

def f1_check(deve, data, alpha):
    y_prediction = []
    y_true = []
    dct = train(data, alpha)
    for i in deve:
        y_prediction.append(classify(i['text'], dct, alpha))
        y_true.append(int(i['class']))
    F1 = f1_score(y_true, y_prediction)
    return F1

with open('train.tsv') as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for i in reader:
        dat.append(i)

with open('dev.tsv') as tsvfile:
    reader2 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for i in reader2:
        dev.append(i)

with open('test.unlabeled.tsv') as tsvfile:
    reader3 = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
    for i in reader3:
        testarr.append(i)

alpha_list = [0, 0.1, 0.3, 0.7, 1, 1.5, 2, 2.5, 3]
per_list = []

for i in alpha_list:
    per_list.append(f1_check(dev, dat, i))
plt.plot(alpha_list, per_list)
plt.show()
# print(per_list)

y_instanceids = []
y_pred = []
traindic = train(dat, 3.0)

csvfile = open("test.random.csv", 'w')

# classify
for i in testarr:
    y_instanceids.append(i['instance_id'])
    y_pred.append(classify(i['text'], traindic, 3.0))


with csvfile:
    titlerow = ['instance_id', 'class']
    writer = csv.writer(csvfile)
    writer.writerow(titlerow)

    for i in range(len(y_instanceids)):
        writer.writerow([y_instanceids[i], y_pred[i]])

# what's my f1 score with alpha = 3?
# dev_true = []
# dev_pred = []
# data_dev2 = train(dat, 3)
# for i in dev:
#     dev_pred.append(classify(i['text'], data_dev2, 3.0))
#     dev_true.append(int(i['class']))
# F1 = f1_score(dev_true, dev_pred)
# print('f1 score: ', F1)



