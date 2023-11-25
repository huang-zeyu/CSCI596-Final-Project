import json
import re
from itertools import combinations

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def clean_and_tokenize(text):
    # 清洗文本并分割为单词
    cleaned_text = re.sub(r"[^a-zA-Z0-9-]", " ", text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    tokens = cleaned_text.strip().split()
    return tokens

def generate_k_tuples(tokens, k):
    # 生成长度为k的连续子序列
    k_tuples = set()
    for i in range(len(tokens) - k + 1):
        k_tuple = tuple(tokens[i:i + k])
        k_tuples.add(k_tuple)
    return k_tuples

