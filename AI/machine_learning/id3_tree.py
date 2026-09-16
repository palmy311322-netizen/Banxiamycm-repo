import numpy as np
from collections import Counter
from feature_selection import calculate_information_entropy,calculate_information_gain

class Node:
    #决策树节点类
    def __init__(self,feature_idx=None,value=None,children=None):
        self.feature_idx=feature_idx#特征索引
        self.value=value
        self.children=children or {}

class ID3DecisionTree:
    #ID3决策树分类器
    #基于information gain的决策树
    def __init__(self,max_depth=None,min_samples_split=2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root = None#根节点
        self.feature_names = None#特征名称（可选）

    def fit(self,X,y,feature_name=None):
        self.feature_names=feature_name
        self.n_features=X.shape[1]
        self.root=self._build_tree(X,y,depth=0)

    def _should_stop(self,X,y,depth):#判断是否停止分割
        if self.max_depth is not None and depth>=self.max_depth:
            return True
        if len(y)<self.min_samples_split:
            return True
        if len(np.unique(y))<=1:
            return True
        return False

    def _find_best_feature(self,X,y):#寻找信息增益最大的特征
        best_gain=-1
        best_feature_idx=None
        for feature_idx in range(X.shape[1]):
            gain=calculate_information_gain(X,y,feature_idx)
            if gain>best_gain:
                best_gain=gain
                best_feature_idx=feature_idx
        return best_feature_idx#返回值是最佳特征索引

    def _get_majority_class(self,y):#获取最多见的类别
        counter=Counter(y)
        return counter.most_common(1)[0][0]

    def _build_tree(self,X,y,depth):
        #递归构建ID3决策树
        if self._should_stop(X,y,depth):#如果停止，创建叶节点，预测值为最常见的类别
            leaf_value=self._get_majority_class(y)
            return Node(value=leaf_value)

        best_feature_idx=self._find_best_feature(X,y)#选择最佳划分特征（衡量信息增益）

        if best_feature_idx is None:#如果找不到最佳划分特征，那就返回最多数的类别，并且创建叶节点
            leaf_value=self._get_majority_class(y)
            return Node(value=leaf_value)

        node=Node(feature_idx=best_feature_idx)#创建内部节点

        unique_values=np.unique(X[:,best_feature_idx])#得到该特征值的所有唯一值

        children={}#为每个值创建唯一的子树
        for value in unique_values:#分割数据
            mask=X[:,best_feature_idx]==value
            subset_X=X[mask]
            subset_y=y[mask]
            if len(subset_y)>0:#递归
                children[value]=self._build_tree(subset_X,subset_y,depth+1)

        node.children=children
        return node

    def predict_single(self, x, node=None):#预测单个样本
        if node is None:
            node = self.root
        
        if node.value is not None: # 如果是叶节点，返回预测值
            return node.value
        
        feature_val = x[node.feature_idx] # 获取当前节点使用的特征值
        if feature_val in node.children: # 检查是否有对应的子节点
            return self.predict_single(x, node.children[feature_val])# 递归预测子节点  
        else:# 如果没有对应的子节点，返回最常见的类别，也就是处理训练时未见过的值
            return self._get_most_frequent_value_in_subtree(node)
    
    def _get_most_frequent_value_in_subtree(self, node):#在子树中找到最常见的值（辅助处理未知特征值）
        if node.value is not None:
            return node.value
       
        values = [] # 收集所有叶节点的值
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
            print("ID3决策树结构:")
            print("="*50)
        indent = "  " * depth
        
        if node.value is not None:#叶节点
            print(f"{indent}{prefix} -> 预测: {node.value}")
        else:#内部节点
            feature_name = self.feature_names[node.feature_idx] if self.feature_names else f"特征{node.feature_idx}"
            print(f"{indent}{prefix} -> 根据 {feature_name} 分割:")
            
            for value, child_node in node.children.items():
                child_prefix = f"当 {feature_name} = {value}"
                self.print_tree(child_node, depth + 1, child_prefix)
