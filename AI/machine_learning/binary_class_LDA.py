import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.utils.multiclass import unique_labels


class BinaryLDA(BaseEstimator, ClassifierMixin):
    #本代码旨在实现周志华《机器学习》中的二分类LDA
    
    def __init__(self):
        pass
    
    def fit(self, X, y):
        # 验证输入
        X, y = check_X_y(X, y)
        self.classes_ = unique_labels(y)
        
        if len(self.classes_) != 2:
            raise ValueError(f"BinaryLDA只支持二分类，但检测到{len(self.classes_)}个类别")
        
        n_samples, n_features = X.shape
        
        # 获取两个类别的数据索引
        class1_mask = (y == self.classes_[0])
        class2_mask = (y == self.classes_[1])
        
        # 计算各类别样本数
        n1 = np.sum(class1_mask)
        n2 = np.sum(class2_mask)
        
        # 计算各类别均值向量
        mu1 = np.mean(X[class1_mask], axis=0)  # 第一类均值
        mu2 = np.mean(X[class2_mask], axis=0)  # 第二类均值
        
        # 计算类内散度矩阵 Sw = S1 + S2
        X1_centered = X[class1_mask] - mu1
        X2_centered = X[class2_mask] - mu2
        S1 = np.dot(X1_centered.T, X1_centered)
        S2 = np.dot(X2_centered.T, X2_centered)
        self.Sw_ = S1 + S2
        
        # 计算类间散度矩阵 Sb
        mean_diff = (mu1 - mu2).reshape(-1, 1)
        self.Sb_ = np.dot(mean_diff, mean_diff.T)
        
        # 根据周志华《机器学习》P61，优化目标是最大化广义瑞利商:
        # J(w) = w^T * Sb * w / (w^T * Sw * w)
        # 通过拉格朗日乘数法可得: Sb * w = λ * Sw * w
        # 即: Sw^(-1) * Sb * w = λ * w
        # 对于二分类，最优解为: w ∝ Sw^(-1) * (μ1 - μ2)
        # 求解 w ∝ Sw^(-1) * (μ2 - μ1) (注意顺序，使w指向类别2的方向！)
        try:
            # 使用奇异值分解处理Sw可能奇异的情况
            U, s, Vt = np.linalg.svd(self.Sw_)
            # 构造Sw的伪逆
            s_inv = np.where(s > 1e-10, 1.0 / s, 0)
            Sw_inv = np.dot(Vt.T, np.dot(np.diag(s_inv), U.T))    
            # 计算投影方向
            self.w_ = np.dot(Sw_inv, (mu2 - mu1))
        except np.linalg.LinAlgError:
            # 如果仍然失败，直接使用伪逆
            Sw_pinv = np.linalg.pinv(self.Sw_)
            self.w_ = np.dot(Sw_pinv, (mu2 - mu1))
        
        # 标准化投影向量
        self.w_ = self.w_ / np.linalg.norm(self.w_)
        
        # 计算决策阈值
        # 在投影空间中，两类的投影均值分别为 w^T * μ1 和 w^T * μ2
        proj_mu1 = np.dot(self.w_, mu1)
        proj_mu2 = np.dot(self.w_, mu2)
        
        # 决策边界设在两个投影均值的中点
        self.threshold_ = (proj_mu1 + proj_mu2) / 2
        
        self.n_features_in_ = n_features
        self.mu1_ = mu1
        self.mu2_ = mu2
        
        return self
    
    def transform(self, X):
        
        #将数据投影到LDA方向
        
        #Parameters:
        #X: 特征矩阵 (n_samples, n_features)
        #Returns:
        #X_transformed: 投影后的值 (n_samples,)
        
        check_array(X)
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"期望 {self.n_features_in_} 个特征，但得到 {X.shape[1]} 个")
        return np.dot(X, self.w_) # 投影到LDA方向
    
    def predict(self, X):
        #预测类别
        
        #Parameters:
        #X: 特征矩阵 (n_samples, n_features)
        #Returns:
        #y_pred: 预测标签 (n_samples,)
    
        check_array(X)
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"期望 {self.n_features_in_} 个特征，但得到 {X.shape[1]} 个")
        
        # 计算投影值
        projections = np.dot(X, self.w_)
        
        # 基于阈值进行分类
        # 如果投影值 >= 阈值，则属于第二类，否则属于第一类
        return np.where(projections >= self.threshold_, self.classes_[1], self.classes_[0])
    
    def predict_proba(self, X):
        #预测概率
        
        #Parameters:
        #X: 特征矩阵 (n_samples, n_features)
        #Returns:
        #probabilities: 各类别的预测概率 (n_samples, 2)
       
        check_array(X)
        n_samples = X.shape[0]
        probabilities = np.zeros((n_samples, 2))
        projections = np.dot(X, self.w_) # 计算投影值
        
        for i in range(n_samples):
            # 计算到各类别投影中心的距离
            dist_to_class1 = abs(projections[i] - np.dot(self.w_, self.mu1_))
            dist_to_class2 = abs(projections[i] - np.dot(self.w_, self.mu2_))
            
            # 距离越小，该类别的概率越大
            # 使用softmax将距离转换为概率
            neg_dists = np.array([-dist_to_class1, -dist_to_class2])
            # 数值稳定化
            neg_dists = neg_dists - np.max(neg_dists)
            exp_dists = np.exp(neg_dists)
            probabilities[i] = exp_dists / np.sum(exp_dists)
        return probabilities
