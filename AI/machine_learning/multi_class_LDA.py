import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_X_y, check_array
from sklearn.utils.multiclass import unique_labels

class LinearDiscriminantAnalysis(BaseEstimator, ClassifierMixin):
    
    #线性判别分析 (Linear Discriminant Analysis, LDA) 实现（推广到多分类中）
    
    
    def __init__(self, n_components=None, priors=None, shrinkage=None):
        self.n_components = n_components
        self.priors = priors
        self.shrinkage = shrinkage
    
    def fit(self, X, y):#训练方法
        
        #X: 特征矩阵 (n_samples, n_features)
        #y: 标签向量 (n_samples,)
        
        X, y = check_X_y(X, y)# X,y形状是否匹配，类型是否合法
        self.classes_ = unique_labels(y)
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)
        
        if self.priors is None: # 如果没有提供先验概率，则假设均匀分布
            self.priors_ = np.bincount(y) / float(len(y))#统计每个类别出现的次数，除以总样本数得到经验概率
        else:
            self.priors_ = np.array(self.priors)
            
        # 计算各类别的均值向量
        self.means_ = np.zeros((n_classes, n_features))
        for i, class_label in enumerate(self.classes_):#enumerate()遍历可迭代对象，获得元素索引和元素本身，返回值是一个枚举对象
            self.means_[i, :] = np.mean(X[y == class_label], axis=0)
        
        # 计算总体均值
        self.global_mean_ = np.mean(X, axis=0)
        
        # 计算类内散度矩阵 (within-class scatter matrix)
        Sw = np.zeros((n_features, n_features))
        for i, class_label in enumerate(self.classes_):
            class_X = X[y == class_label]
            class_mean = self.means_[i, :]
            centered_class_X = class_X - class_mean
            Sw += np.dot(centered_class_X.T, centered_class_X)
        
        # 计算类间散度矩阵 (between-class scatter matrix)
        Sb = np.zeros((n_features, n_features))
        for i, class_label in enumerate(self.classes_):
            n_class = np.sum(y == class_label)
            mean_diff = (self.means_[i, :] - self.global_mean_).reshape(n_features, 1)
            Sb += n_class * np.dot(mean_diff, mean_diff.T)
        
        # 计算广义特征值问题 (Sw^(-1) * Sb)
        # 使用奇异值分解来处理可能的奇异矩阵情况
        try:
            eigenvals, eigenvecs = np.linalg.eigh(np.dot(np.linalg.inv(Sw), Sb))
        except np.linalg.LinAlgError:
            # 如果Sw是奇异的，使用伪逆
            eigenvals, eigenvecs = np.linalg.eigh(np.dot(np.linalg.pinv(Sw), Sb))
        
        # 按照特征值大小排序特征向量
        idx = np.argsort(eigenvals)[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        # 取前n_components个特征向量作为投影方向
        if self.n_components is not None:
            self.scalings_ = eigenvecs[:, :self.n_components]
        else:
            # 默认取所有类别数减1个分量
            self.scalings_ = eigenvecs[:, :(n_classes - 1)]
        
        # 计算每个类别的常数项，用于预测
        self.intercept_ = -0.5 * np.diag(np.dot(np.dot(self.means_, self.scalings_), 
                                               self.scalings_.T)) + np.log(self.priors_)
        
        return self
    
    def transform(self, X):
        """
        将数据投影到LDA空间
        
        参数:
        - X: 特征矩阵 (n_samples, n_features)
        
        返回:
        - X_new: 投影后的特征矩阵 (n_samples, n_components)
        """
        check_array(X)
        X_transformed = np.dot(X, self.scalings_)
        return X_transformed
    
    def predict(self, X):
        """
        对新数据进行分类预测
        
        参数:
        - X: 特征矩阵 (n_samples, n_features)
        
        返回:
        - y_pred: 预测标签 (n_samples,)
        """
        check_array(X)
        # 计算每个样本在各个类别上的判别函数值
        X_transformed = self.transform(X)
        class_scores = np.dot(X_transformed, self.scalings_.T.dot(self.means_.T)) + self.intercept_
        
        # 返回得分最高的类别
        y_pred = self.classes_[np.argmax(class_scores, axis=1)]
        return y_pred
    
    def predict_proba(self, X):
        """
        计算每个类别的预测概率
        
        参数:
        - X: 特征矩阵 (n_samples, n_features)
        
        返回:
        - probabilities: 各类别的预测概率 (n_samples, n_classes)
        """
        check_array(X)
        # 计算每个样本在各个类别上的判别函数值
        X_transformed = self.transform(X)
        class_scores = np.dot(X_transformed, self.scalings_.T.dot(self.means_.T)) + self.intercept_
        
        # 将得分转换为概率（通过softmax函数）
        exp_scores = np.exp(class_scores - np.max(class_scores, axis=1, keepdims=True))
        probabilities = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        
        return probabilities
    
    def decision_function(self, X):
        """
        计算决策函数值
        
        参数:
        - X: 特征矩阵 (n_samples, n_features)
        
        返回:
        - scores: 决策函数值 (n_samples, n_classes)
        """
        check_array(X)
        X_transformed = self.transform(X)
        scores = np.dot(X_transformed, self.scalings_.T.dot(self.means_.T)) + self.intercept_
        return scores


# 示例用法和测试
if __name__ == "__main__":
    # 导入必要的库
    import matplotlib.pyplot as plt
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, classification_report
    
    # 生成示例数据
    X, y = make_classification(n_samples=300, n_features=4, n_redundant=0, 
                              n_informative=4, n_classes=3, n_clusters_per_class=1,
                              random_state=42)
    
    # 分割训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 创建并训练LDA模型
    lda = LinearDiscriminantAnalysis()
    lda.fit(X_train, y_train)
    
    # 进行预测
    y_pred = lda.predict(X_test)
    
    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)
    print(f"LDA 分类准确率: {accuracy:.4f}")
    
    # 打印分类报告
    print("\n分类报告:")
    print(classification_report(y_test, y_pred))
    
    # 展示降维效果（如果原特征维数大于2）
    if X.shape[1] > 1:
        X_train_lda = lda.transform(X_train)
        X_test_lda = lda.transform(X_test)
        
        plt.figure(figsize=(12, 5))
        
        # 原始数据可视化（取前两个特征）
        plt.subplot(1, 2, 1)
        plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap='viridis', alpha=0.7)
        plt.title('原始数据')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        
        # LDA降维后数据可视化
        plt.subplot(1, 2, 2)
        if X_train_lda.shape[1] >= 2:
            plt.scatter(X_train_lda[:, 0], X_train_lda[:, 1], c=y_train, cmap='viridis', alpha=0.7)
            plt.title('LDA降维后数据')
            plt.xlabel('LD1')
            plt.ylabel('LD2')
        else:
            plt.scatter(X_train_lda[:, 0], np.zeros_like(X_train_lda[:, 0]), c=y_train, cmap='viridis', alpha=0.7)
            plt.title('LDA降维后数据')
            plt.xlabel('LD1')
            plt.ylabel('Constant')
        
        plt.tight_layout()
        plt.show()
    
    print("\nLDA算法实现完成!")
