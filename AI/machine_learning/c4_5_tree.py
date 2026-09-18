import numpy as np
from collections import Counter
from feature_selection import calculate_gain_ratio
from binary_split import binary_split_by_gain_ratio

class Node:
    # 决策树节点类
    def __init__(self, feature_idx=None, value=None, children=None, split_type='discrete', split_value=None):
        self.feature_idx = feature_idx  #特征索引
        self.value = value              
        self.children = children or {}  
        self.split_type = split_type    #分割类型：'discrete'或'continuous'
        self.split_value = split_value  #连续特征分割点

class C45DecisionTree:
    #C4.5决策树分类器
    #基于gain ratio的决策树
    def __init__(self, max_depth=None, min_samples_split=2, feature_types=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None#根节点
        self.feature_names = None#特征名称（可选）
        self.feature_types = feature_types#特征类型：'continuous' 或 'discrete'

    def fit(self, X, y, feature_names=None):
        self.feature_names = feature_names
        self.n_features = X.shape[1]
        if self.feature_types is None:#如果未指定特征类型，默认全部为离散
            self.feature_types = ['discrete'] * self.n_features    
        self.root = self._build_tree(X, y, depth=0)

    def _should_stop(self, X, y, depth):#判断是否停止分割
        if self.max_depth is not None and depth >= self.max_depth:
            return True
        if len(y) < self.min_samples_split:
            return True
        if len(np.unique(y)) <= 1:
            return True
        return False

    def _find_best_feature(self, X, y):#寻找增益率最大的特征
        best_criterion = -1
        best_feature_idx = None
        best_split_info = None#存储分割信息

        for feature_idx in range(X.shape[1]):
            if self.feature_types[feature_idx] == 'continuous':
                #连续特征：使用二分法分割
                split_value, gain_ratio, left_idx, right_idx = binary_split_by_gain_ratio(X, y, feature_idx)
                if gain_ratio > best_criterion:
                    best_criterion = gain_ratio
                    best_feature_idx = feature_idx
                    best_split_info = {
                        'split_value': split_value,
                        'left_idx': left_idx,
                        'right_idx': right_idx
                    }
            else:
                #离散特征：计算增益率
                gain_ratio = calculate_gain_ratio(X, y, feature_idx)
                
                if gain_ratio > best_criterion:
                    best_criterion = gain_ratio
                    best_feature_idx = feature_idx
                    best_split_info = None
        
        return best_feature_idx, best_split_info

    def _get_majority_class(self, y):  #获取最常见的类别
        counter = Counter(y)
        return counter.most_common(1)[0][0]

    def _build_tree(self, X, y, depth):
        #递归构建C4.5决策树
        if self._should_stop(X, y, depth):#如果停止，创建叶节点，预测值为最常见的类别
            leaf_value = self._get_majority_class(y)
            return Node(value=leaf_value)

        best_feature_idx, best_split_info = self._find_best_feature(X, y)#选择最佳分割特征

        if best_feature_idx is None:#如果找不到最佳分割特征，就返回最多数的类别，并且创建叶节点
            leaf_value = self._get_majority_class(y)
            return Node(value=leaf_value)

        #创建内部节点
        if best_split_info is not None:#连续特征
            node = Node(
                feature_idx=best_feature_idx,
                split_type='continuous',
                split_value=best_split_info['split_value']
            )
            
            #构建左右子树
            left_mask = best_split_info['left_idx']
            right_mask = best_split_info['right_idx']
            
            left_X, left_y = X[left_mask], y[left_mask]
            right_X, right_y = X[right_mask], y[right_mask]
            
            children = {}
            children['left'] = self._build_tree(left_X, left_y, depth + 1)
            children['right'] = self._build_tree(right_X, right_y, depth + 1)
            node.children = children
        else:#离散特征
            node = Node(feature_idx=best_feature_idx, split_type='discrete')
            
            unique_values = np.unique(X[:, best_feature_idx])#得到该特征值的所有唯一值

            children = {}#为每个值创建唯一的子树
            for value in unique_values:#分割数据
                mask = X[:, best_feature_idx] == value
                subset_X = X[mask]
                subset_y = y[mask]
                if len(subset_y) > 0:  # 递归
                    children[value] = self._build_tree(subset_X, subset_y, depth + 1)

            node.children = children
        return node

    def predict_single(self, x, node=None):#预测单个样本
        if node is None:
            node = self.root
        
        if node.value is not None:#如果是叶节点，返回预测值
            return node.value
        
        if node.split_type == 'continuous':#连续特征分割
            feature_val = x[node.feature_idx]
            split_val = node.split_value
            if feature_val <= split_val:
                return self.predict_single(x, node.children['left'])
            else:
                return self.predict_single(x, node.children['right'])
        else:#离散特征分割
            feature_val = x[node.feature_idx]#获取当前节点使用的特征值
            if feature_val in node.children:#检查是否有对应的子节点
                return self.predict_single(x, node.children[feature_val])#递归预测子节点
            else:#如果没有对应的子节点，返回最常见的类别，也就是处理训练时未见过的值
                return self._get_most_frequent_value_in_subtree(node)
    
    def _get_most_frequent_value_in_subtree(self, node):#在子树中找到最常见的值（辅助处理未知特征值）
        if node.value is not None:
            return node.value
       
        values = []#收集所有叶节点的值
        for child in node.children.values():
            if child.value is not None:
                values.append(child.value)
            else:
                values.extend(self._collect_leaf_values(child))
        
        if values:
            counter = Counter(values)
            return counter.most_common(1)[0][0]
        else:
            return None
    
    def _collect_leaf_values(self, node):#收集子树中所有叶节点的值
        if node.value is not None:
            return [node.value]
        
        values = []
        for child in node.children.values():
            if child.value is not None:
                values.append(child.value)
            else:
                values.extend(self._collect_leaf_values(child))
        
        return values

    def predict(self, X):#预测多个样本
        predictions = []
        for x in X:
            pred = self.predict_single(x)
            predictions.append(pred)
        return np.array(predictions)
    
    def score(self, X, y):#计算准确率
        predictions = self.predict(X)
        return np.mean(predictions == y)
    
    def print_tree(self, node=None, depth=0, prefix="Root"):#打印决策树结构
        if node is None:
            node = self.root
            print("C4.5决策树结构")
            print("="*50)
        indent = "  " * depth
        
        if node.value is not None:#叶节点
            print(f"{indent}{prefix} -> 预测: {node.value}")
        else:#内部节点
            feature_name = self.feature_names[node.feature_idx] if self.feature_names else f"特征{node.feature_idx}"
            
            if node.split_type == 'continuous':
                print(f"{indent}{prefix} -> 根据 {feature_name} <= {node.split_value} 分割:")
                self.print_tree(node.children['left'], depth + 1, f"当 {feature_name} <= {node.split_value}")
                self.print_tree(node.children['right'], depth + 1, f"当 {feature_name} > {node.split_value}")
            else:
                print(f"{indent}{prefix} -> 根据 {feature_name} 分割:")
                
                for value, child_node in node.children.items():
                    child_prefix = f"当 {feature_name} = {value}"
                    self.print_tree(child_node, depth + 1, child_prefix)