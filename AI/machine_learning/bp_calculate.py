import numpy as np
def sigmoid(z):
    """
    Sigmoid 激活函数。
    对应西瓜书公式 (5.2): f(x) = 1 / (1 + exp(-x))
    """
    # 截断防止 exp 溢出
    z = np.clip(z, -500, 500) 
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_derivative(a):
    """
    Sigmoid 的导数。
    注意：输入参数是激活后的值 a = sigmoid(z)，而不是 z。
    公式: f'(z) = f(z) * (1 - f(z)) => a * (1 - a)
    """
    return a * (1.0 - a)


# ==========================================
# 2. 损失函数及其导数 (Loss Functions)
# ==========================================
def mse_loss(y_hat, y):
    """
    均方误差 (MSE) 损失函数。
    对应西瓜书公式 (5.13) 的批量版本: E = 1/(2m) * sum((y_hat - y)^2)
    """
    return 0.5 * np.mean(np.sum((y_hat - y) ** 2, axis=1))

def mse_derivative(y_hat, y):
    """
    MSE 对预测值 y_hat 的偏导数。
    公式: d(E)/d(y_hat) = y_hat - y
    """
    return y_hat - y


# ==========================================
# 3. BP 核心梯度项计算 (Gradient Terms)
# ==========================================
def compute_g(y_hat, y):
    """
    计算输出层梯度项 g_j。
    对应西瓜书公式 (5.15): g_j = y_hat_j * (1 - y_hat_j) * (y_j - y_hat_j)
    
    💡 核心注意：这里的 g_j 已经包含了负号，即 g_j = - dE/d(beta_j)
    """
    # 等价于: sigmoid_derivative(y_hat) * (y - y_hat)
    return y_hat * (1.0 - y_hat) * (y - y_hat)

def compute_e(b, W, g):
    """
    计算隐藏层梯度项 e_h。
    对应西瓜书公式 (5.16): e_h = b_h * (1 - b_h) * sum(w_hj * g_j)
    
    :param b: 隐藏层的输出值 (m, q)
    :param W: 隐藏层到输出层的权重 (q, l)
    :param g: 输出层的梯度项 (m, l)
    """
    # np.dot(g, W.T) 巧妙地实现了 sum(w_hj * g_j) 的矩阵运算
    return sigmoid_derivative(b) * np.dot(g, W.T)


# ==========================================
# 4. 参数更新公式 (Parameter Update)
# ==========================================
def update_params(params, grads, lr):
    """
    西瓜书风格的参数更新（注意是加法，因为 g 和 e 自带负号）。
    对应西瓜书公式 (5.17) - (5.20)
    
    :param params: 字典，包含当前的 'W', 'theta', 'V', 'gamma'
    :param grads: 字典，包含计算出的更新量 'dW', 'dtheta', 'dV', 'dgamma'
    :param lr: 学习率 η
    """
    # 更新隐藏层到输出层的权重 w (公式 5.17)
    params['W'] += lr * grads['dW']
    # 更新输出层阈值 theta (公式 5.18)
    params['theta'] += lr * grads['dtheta']
    
    # 更新输入层到隐藏层的权重 v (公式 5.19)
    params['V'] += lr * grads['dV']
    # 更新隐藏层阈值 gamma (公式 5.20)
    params['gamma'] += lr * grads['dgamma']
    
    return params