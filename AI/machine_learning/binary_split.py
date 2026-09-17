import numpy as np
from feature_selection import calculate_information_gain, calculate_gain_ratio, calculate_gini_index

def binary_split_by_information_gain(X, y, feature_index):#基于信息增益最大化进行二分离散化
        
    feature_values = np.unique(X[:, feature_index])#获取指定特征的所有唯一值并排序
    
    best_split_value = None
    best_info_gain = float('-inf')  #信息增益要最大化
    best_left_indices = None
    best_right_indices = None
    
    #遍历所有可能的分割点
    for i in range(len(feature_values) - 1):
        split_value = (feature_values[i] + feature_values[i + 1]) / 2
        
        #根据分割值将数据分为两部分
        left_indices = np.where(X[:, feature_index] <= split_value)[0]
        right_indices = np.where(X[:, feature_index] > split_value)[0]
        
        info_gain = calculate_information_gain(X, y, feature_index, split_value)
        
        #更新最佳分割点（最大化信息增益）
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_split_value = split_value
            best_left_indices = left_indices
            best_right_indices = right_indices
    
    return best_split_value, best_info_gain, best_left_indices, best_right_indices

def binary_split_by_gain_ratio(X, y, feature_index):#基于增益率最大化进行二分离散化
   
    feature_values = np.unique(X[:, feature_index])#获取指定特征的所有唯一值并排序
    
    best_split_value = None
    best_gain_ratio = float('-inf')  #增益率要最大化
    best_left_indices = None
    best_right_indices = None
    
    #遍历所有可能的分割点
    for i in range(len(feature_values) - 1):
        split_value = (feature_values[i] + feature_values[i + 1]) / 2
        
        #根据分割值将数据分为两部分
        left_indices = np.where(X[:, feature_index] <= split_value)[0]
        right_indices = np.where(X[:, feature_index] > split_value)[0]
        
        gain_ratio = calculate_gain_ratio(X, y, feature_index, split_value)
        
        # 更新最佳分割点（最大化增益率）
        if gain_ratio > best_gain_ratio:
            best_gain_ratio = gain_ratio
            best_split_value = split_value
            best_left_indices = left_indices
            best_right_indices = right_indices
    
    return best_split_value, best_gain_ratio, best_left_indices, best_right_indices

def binary_split_by_gini(X, y, feature_index):#基于基尼指数最小化进行二分离散化
   
    feature_values = np.unique(X[:, feature_index]) #获取指定特征的所有唯一值并排序
    
    best_split_value = None
    best_gini = float('inf')  #基尼指数要最小化
    best_left_indices = None
    best_right_indices = None
    
    #遍历所有可能的分割点
    for i in range(len(feature_values) - 1):
        split_value = (feature_values[i] + feature_values[i + 1]) / 2
        
        #根据分割值将数据分为两部分
        left_indices = np.where(X[:, feature_index] <= split_value)[0]
        right_indices = np.where(X[:, feature_index] > split_value)[0]
        
        #计算左右子集的基尼指数
        gini_left = calculate_gini_index(y[left_indices])
        gini_right = calculate_gini_index(y[right_indices])
        
        #计算加权平均基尼指数
        total_samples = len(y)
        if total_samples == 0:
            continue
            
        weighted_gini = (len(left_indices) / total_samples) * gini_left + \
                       (len(right_indices) / total_samples) * gini_right
        
        #更新最佳分割点（最小化基尼指数）
        if weighted_gini < best_gini:
            best_gini = weighted_gini
            best_split_value = split_value
            best_left_indices = left_indices
            best_right_indices = right_indices
    
    return best_split_value, best_gini, best_left_indices, best_right_indices