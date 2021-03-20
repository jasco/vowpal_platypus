from math import sqrt, log

def log_loss(results):
     predicted = [min([max([x, 1e-15]), 1-1e-15]) for x in map(lambda x: float(x[0]), results)]
     target = [min([max([x, 1e-15]), 1-1e-15]) for x in map(lambda x: float(x[1]), results)]
     return -(1.0 / len(target)) * sum([target[i] * log(predicted[i]) + (1.0 - target[i]) * log(1.0 - predicted[i]) for i in xrange(len(target))])

def rmse(results):
    return (sum(map(lambda x: (x[1] - x[0]) ** 2, results)) / float(len(results))) ** 0.5

def percent_correct(results, threshold=0.5):
    return sum(map(lambda x: x[1] == (0 if x[0] < threshold else 1), results)) / float(len(results))

def true_positives(results, threshold=0.5):
    return sum(map(lambda x: x[0] >= threshold, filter(lambda x: x[1] == 1, results)))

def true_negatives(results, threshold=0.5):
    return sum(map(lambda x: x[0] < threshold, filter(lambda x: x[1] == 0, results)))

def false_negatives(results, threshold=0.5):
    return sum(map(lambda x: x[0] < threshold, filter(lambda x: x[1] == 1, results)))

def false_positives(results, threshold=0.5):
    return sum(map(lambda x: x[0] >= threshold, filter(lambda x: x[1] == 0, results)))

def cost_rate(results, false_negative_cost=1, false_positive_cost=1, threshold=0.5):
    fp = false_positives(results, threshold=threshold)
    fn = false_negatives(results, threshold=threshold)
    n = len(results)
    return ((fp * false_positive_cost) + (fn * false_negative_cost)) / float(n)

def confusion_matrix(results, threshold=0.5):
    return {
        'TP': true_positives(results, threshold=threshold),
        'TN': true_negatives(results, threshold=threshold),
        'FP': false_positives(results, threshold=threshold),
        'FN': false_negatives(results, threshold=threshold)
    }

def tpr(results, threshold=0.5):
    tpc = true_positives(results, threshold=threshold)
    fnc = false_negatives(results, threshold=threshold)
    if tpc + fnc <= 0:
        return 0.0
    else:
        return tpc / float(tpc + fnc)

def sensitivity(results, threshold=0.5):
    return tpr(results, threshold=threshold)

def recall(results, threshold=0.5):
    return tpr(results, threshold=threshold)

def tnr(results, threshold=0.5):
    tnc = true_negatives(results, threshold=threshold)
    fpc = false_positives(results, threshold=threshold)
    if tnc + fpc <= 0:
        return 0.0
    else:
        return tnc / float(tnc + fpc)

def specificity(results, threshold=0.5):
    return tnr(results, threshold=threshold)

def fnr(results, threshold=0.5):
    fnc = false_negatives(results, threshold=threshold)
    tpc = true_positives(results, threshold=threshold)
    if tpc + fnc <= 0:
        return 0.0
    else:
        return fnc / float(tpc + fnc)

def fpr(results, threshold=0.5):
    fpc = false_positives(results, threshold=threshold)
    tnc = true_negatives(results, threshold=threshold)
    if fpc + tnc <= 0:
        return 0.0
    else:
        return fpc / float(fpc + tnc)

def precision(results, threshold=0.5):
    tpc = true_positives(results, threshold=threshold)
    fpc = false_positives(results, threshold=threshold)
    return tpc / max(float((tpc + fpc)), 1.0)

def f_score(results, threshold=0.5, beta=1):
    precision_value = precision(results, threshold=threshold)
    recall_value = recall(results, threshold=threshold)
    return (1 + pow(beta, 2)) * ((precision_value * recall_value) / max((pow(beta, 2) * precision_value) + recall_value, 0.000001))

def mcc(results, threshold=0.5):
    tpc = true_positives(results, threshold=threshold)
    tnc = true_negatives(results, threshold=threshold)
    fpc = false_positives(results, threshold=threshold)
    fnc = false_negatives(results, threshold=threshold)
    return ((tpc * tnc) - (fpc * fnc)) / sqrt(float(max((tpc + fpc) * (tpc + fnc) * (tnc + fpc) * (tnc + fnc), 1.0)))

def average_accuracy(results, threshold=0.5):
    tpc = true_positives(results, threshold=threshold)
    tnc = true_negatives(results, threshold=threshold)
    fpc = false_positives(results, threshold=threshold)
    fnc = false_negatives(results, threshold=threshold)
    return 0.5 * ((tpc / float(tpc + fnc)) + (tnc / float(tnc + fpc)))


def auc(results, threshold=0.5):
    def _tied_rank(x):
        sorted_x = sorted(zip(x,range(len(x))))
        r = [0 for k in x]
        cur_val = sorted_x[0][0]
        last_rank = 0
        for i in range(len(sorted_x)):
            if cur_val != sorted_x[i][0]:
                cur_val = sorted_x[i][0]
                for j in range(last_rank, i): 
                    r[sorted_x[j][1]] = float(last_rank+1+i)/2.0
                last_rank = i
            if i==len(sorted_x)-1:
                for j in range(last_rank, i+1): 
                    r[sorted_x[j][1]] = float(last_rank+i+2)/2.0
        return r

    def _auc(actual, posterior):
        r = _tied_rank(posterior)
        num_positive = len([0 for x in actual if x==1])
        num_negative = len(actual)-num_positive
        sum_positive = sum([r[i] for i in range(len(r)) if actual[i]==1])
        auc = ((sum_positive - num_positive*(num_positive+1)/2.0) /
               (num_negative*num_positive))
        return auc

    if threshold:
        preds = map(lambda y: 1 if y >= threshold else 0, map(lambda x: x[0], results))
    else:
        preds = map(lambda x: x[0], results)
    actuals = map(lambda x: x[1], results)
    return _auc(actuals, preds)
