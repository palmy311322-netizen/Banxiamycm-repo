import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_diabetes
from sklearn.linear_model import LinearRegression

diabetes=load_diabetes()

def load_data():
    data=diabetes.data
    feature_names=diabetes.feature_names
    df=pd.DataFrame(data, columns=feature_names)
    df['target']=diabetes.target
    return df

def split_dataset(df_diabetes):
    from sklearn.model_selection import train_test_split
    X=df_diabetes.drop('target',axis=1)
    y=df_diabetes['target']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    return X_train,X_test,y_train,y_test

def train_model(model,X_train,y_train):
    model.fit(X_train,y_train)
    return model

def evaluate_model(model,X_test,y_test):
    from sklearn.metrics import mean_squared_error as mse
    y_pred=model.predict(X_test)
    score=model.score(X_test,y_test)
    MSE=mse(y_test,y_pred)
    return score,MSE

def model_params(model):
    w=model.coef_
    b=model.intercept_
    return w,b

def figure(df_diabetes):
    features=df_diabetes.columns.drop('target')
    plt.figure(figsize=(20,10))
    for i,col in enumerate(features):
        ax=plt.subplot(2,5,i+1)
        data2=df_diabetes[col]
        ax.scatter(data2,df_diabetes['target'])
        model2=LinearRegression()
        model2.fit(df_diabetes[[col]],df_diabetes['target'])
        w=model2.coef_[0]
        b=model2.intercept_
        x_line=np.array([data2.min(),data2.max()])
        y_line=w*x_line+b
        ax.plot(x_line,y_line,color='red')
        ax.set_title(f'{col}: w={w:.2f}, b={b:.2f}')
    plt.tight_layout()
    plt.savefig('diabetes_scatter.png', dpi=150)
    plt.show()


        

