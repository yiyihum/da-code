import json
import argparse
import re
import string

import numpy as np

from typing import List
from collections import Counter
import pandas as pd


def markdown_to_list(data):
    lines = data.split('\n')[2:]
    result = []

    for line in lines:
        if line.strip():
            content = line.split('|')
            content = [item.strip() for item in content]
            result.append(tuple(content))
    return result

def calculate_multi_em_score(pred, gold):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    pred_counts = {}
    gold_counts = {}

    # calculate the counts of each answer in the pred
    for answer in pred:
        pred_counts[answer] = pred_counts.get(answer, 0) + 1
    
    # calculate the counts of each answer in the gold
    for answer in gold:
        gold_counts[answer] = gold_counts.get(answer, 0) + 1
    
    # calculate TP, FP, FN
    for answer in pred_counts:
        true_positives += min(pred_counts[answer], gold_counts.get(answer, 0))
        false_positives += max(0, pred_counts[answer] - gold_counts.get(answer, 0))
    
    for answer in gold_counts:
        false_negatives += max(0, gold_counts[answer] - pred_counts.get(answer, 0))
    
    if true_positives == 0 or (true_positives + false_positives) == 0 or (true_positives + false_negatives) == 0:
        return 0
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)
    return f1_score


def comma_f1_score(prediction, ground_truth, **kwargs):

    prediction_tokens = prediction.split(',')
    pred = [item.strip() for item in prediction_tokens]
    ground_truth_tokens = ground_truth.split(',')
    gold = [item.strip() for item in ground_truth_tokens]
    
    true_positives = len(set(pred) & set(gold))
    false_positives = len(set(pred) - set(gold))
    false_negatives = len(set(gold) - set(pred))

    if true_positives == 0 or (true_positives + false_positives) == 0 or (true_positives + false_negatives) == 0:
        return 0

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    f1_score = 2 * (precision * recall) / (precision + recall)

    return f1_score



def is_numeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def f1_score(prediction, ground_truth, **kwargs):
    common = Counter(prediction) & Counter(ground_truth)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction)
    recall = 1.0 * num_same / len(ground_truth)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1
def qa_f1_score(prediction, ground_truth, **kwargs):
    if is_numeric(prediction) and is_numeric(ground_truth):
        if float(prediction) == float(ground_truth):
            return 1
        else:
            return 0
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    return f1_score(prediction_tokens, ground_truth_tokens)




def compare_csv(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    pred_str = df1.to_markdown(index=False)
    gold_str = df2.to_markdown(index=False)
    pred = markdown_to_list(pred_str)
    gold = markdown_to_list(gold_str)
    score = calculate_multi_em_score(pred, gold) 
    return score