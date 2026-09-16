import numpy as np
from collections import Counter

def calculate_information_entropy(y):
    #信息熵的计算
    if len(y)==0:
        return 0
    label_counts=Counter(y)
    total_samples=len(y)
    entropy=0
    for count in label_counts.values():
        probability=count/total_samples
        if probability>0:
            entropy-=probability*np.log2(probability)
    return entropy

def calculate_information_gain(X,y,feature_idx):
    #信息增益的计算
    total_samples=len(y)
    base_entropy=calculate_information_entropy(y)#计算原始信息熵
    weighted_entropy=0
    unique_values=np.unique(X[:,feature_idx])#获取该特征值的所有取值
    for value in unique_values:
        subset_y=y[X[:,feature_idx]==value]
        subset_weight=len(subset_y)/total_samples
        weighted_entropy+=subset_weight*calculate_information_entropy(subset_y)
    return base_entropy-weighted_entropy#信息增益=原始信息熵-分割后加权平均熵
    
def calculate_gain_ratio(X,y,feature_idx):
    #增益率的计算
    gain=calculate_information_gain(X,y,feature_idx)
    unique_values=np.unique(X[:,feature_idx])
    split_information=0#求IV(a)
    total_samples=len(y)
    for value in unique_values:
        subset_y=y[X[:,feature_idx]==value]
        subset_weight=len(subset_y)/total_samples
        split_information-=subset_weight*np.log2(subset_weight)
    if split_information==0:
        return 0
    return gain/split_information

def calculate_gini(y):
    #计算基尼值
    if len(y)==0:
        return 0
    label_counts=Counter(y)
    total_samples=len(y)
    geni=1.0
    for count in label_counts.values():
        probability=count/total_samples
        geni-=probability**2
    return geni

def calculate_gini_index(X,y,feature_idx):
    #基尼指数的计算
    total_samples=len(y)
    if total_samples==0:
        return 0
    unique_values=np.unique(X[:,feature_idx])
    geni_index=0
    for value in unique_values:
        subset_y=y[X[:,feature_idx]==value]
        subset_weight=len(subset_y)/total_samples
        geni_index+=subset_weight*calculate_gini(subset_y)
    return geni_index


