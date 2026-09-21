import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
from bp_calculate import (
    sigmoid, mse_loss, compute_g, compute_e, update_params
)

class BPNeuralNetwork:
    def __init__(self, d, q, l, learning_rate=0.1):
        self.d = d#输入特征维度
        self.q = q#隐藏层神经元个数
        self.l = l#输出层神经元个数
        self.lr = learning_rate#学习率η
        
        self.params = {
            #输入层到隐藏层：权重v(d, q)，阈值gamma(1, q)
            'v': np.random.randn(d, q) * 0.1,
            'gamma': np.zeros((1, q)),
            # 隐藏层到输出层：权重w(q, l)阈值theta(1, l)
            'w': np.random.randn(q, l) * 0.1,
            'theta': np.zeros((1, l))
        }

    def forward(self, X):#前向传播
        v, gamma, w, theta = self.params['v'], self.params['gamma'], self.params['w'], self.params['theta']
        alpha = np.dot(X, v)
        self.b = sigmoid(alpha - gamma)
        beta = np.dot(self.b, w)
        self.y_hat = sigmoid(beta - theta)

    def compute_loss(self, y):
        return mse_loss(self.y_hat, y)

    def backward(self, X, y):
        v, w = self.params['v'], self.params['w']
        m = X.shape[0] #样本数量
        g = compute_g(self.y_hat, y)
        e = compute_e(self.b, w, g)
        grads = {}
        grads['dw'] = np.dot(self.b.T, g)
        grads['dtheta'] = -np.sum(g, axis=0, keepdims=True)
        grads['dv'] = np.dot(X.T, e)
        grads['dgamma'] = -np.sum(e, axis=0, keepdims=True)
        return grads
    def train_step(self, X, y):#训练一个步骤
        self.forward(X)
        loss = self.compute_loss(y)
        grads = self.backward(X, y)
        self.params = update_params(self.params, grads, self.lr)
        return loss
    def train(self, X, y, epochs=1000, print_cost=True):#循环训练
        for i in range(epochs):
            loss = self.train_step(X, y)
            if print_cost and i % 100 == 0:
                print(f"Epoch {i:4d} | Loss: {loss:.6f}")
    def predict(self, X):#预测
        self.forward(X)
        return (self.y_hat > 0.5).astype(int)