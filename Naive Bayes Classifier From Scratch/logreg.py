import logging, sys
import re
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import f1_score
from scipy.sparse import csr_matrix, hstack



## references:
## https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
## https://beckernick.github.io/logistic-regression-from-scratch/


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

def parse_lines(file):
    instances = []
    with open(file) as tsvfile:
        reader = csv.DictReader(tsvfile, dialect='excel-tab', quoting=csv.QUOTE_NONE)
        for i in reader:
            instances.append(i)
        return instances

def write_output(ids, predictions):
    with open("test.labeled_{}.csv".format(model), 'w') as file:
        writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        writer.writerow(['instance_id', 'class'])
        writer.writerows(zip(ids, predictions))

train_data = "train.tsv"
dev_data = "dev.tsv"
test_data = "test.unlabeled.tsv"

train_inst = parse_lines(train_data)
dev_inst = parse_lines(dev_data)
test_inst = parse_lines(test_data)
wordlist = {}

def build_matrix(instances, pred=False):
    docs = [d['text'] for d in instances]
    indptr = [0]
    indices = []
    data = []

    for d in docs:
        words = better_tokenize(d)
        for word in words:
            if not pred:
                index = wordlist.setdefault(word, len(wordlist))
                indices.append(index)
                data.append(1)
            else:
                if word in wordlist:
                    index = wordlist.get(word)
                    indices.append(index)
                    data.append(1)

        indptr.append(len(indices))

    matrix = csr_matrix((data, indices, indptr), shape=(len(instances), len(wordlist)), dtype=int)

    return matrix


def signmoid(scores):
    return (1 / (1+np.exp(-scores)))

def log_likelihood(features, target, weights):
    scores = features.dot(weights)
    ll = np.sum(target*scores - np.log(1 + np.exp(scores)))
    return ll

def log_regression(features, target, learning_rate, num_steps):
    intercept = np.ones((features.shape[0], 1))
    features = hstack((intercept, features))

    weights = np.zeros(features.shape[1])
    steps = []
    lls = []
    for step in range(num_steps):
        scores = features.dot(weights)

        predictions = signmoid(scores)

        #update gradient
        output_error = target - predictions
        gradient = features.T.dot(output_error)
        weights += learning_rate * gradient

        # print log-likelihood log_likelihood
        if step % 10000 == 0:
            ll = log_likelihood(features, target, weights)
            # logging.debug("Step: {} LL: {}".format(step, ll))
            steps.append(step)
            lls.append(ll)
        stats = {"rate": learning_rate, "steps": steps, "lls": lls}

    return weights, stats

def predict(weights):
    features = build_matrix(dev_inst, pred=True)
    actual = np.array([int(d['class']) for d in dev_inst])

    intercept = np.ones((features.shape[0], 1))
    features = hstack((intercept, features))
    scores = features.dot(weights)
    predictions = signmoid(scores)
    pred_label =[]
    for pred in predictions:
        label = 1 if pred >= 0.5 else 0
        pred_label.append(label)
    f1 = f1_score(actual, pred_label)
    return f1

def predict_test(weights):
    features = build_matrix(test_inst, pred=True)
    intercept = np.ones((features.shape[0], 1))
    features = hstack((intercept, features))

    scores = features.dot(weights)
    pred_scores = signmoid(scores)
    ids = [d['instance_id'] for d in test_inst]
    predictions =[]
    for score in pred_scores:
        label = 1 if score >= 0.5 else 0
        predictions.append(label)
    write_output(ids, predictions, 'logistic')

def process(num_steps=300000, learning_rate=5e-5):
    reset()
    features = build_matrix(train_inst)
    target = np.array([int(d['class']) for d in train_inst])
    weights, stats = log_regression(features, target, learning_rate, num_steps)
    f1 = predict(weights)

    predict_test(weights)

    return stats

def reset():
	vocab = {}


learning_rate = [5e-5]
results = []
for rate in learning_rate:
    result = process(learning_rate=rate)
    results.append(result)
