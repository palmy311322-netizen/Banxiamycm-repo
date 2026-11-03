import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeRegressor

iris=load_iris()
def data_load():
    data=iris.data
    feature_names=iris.feature_names
    df=pd.DataFrame(data,columns=feature_names)
    return df

def split_dataset(iris_df):
    X=iris_df.drop("petal width (cm)",axis=1)
    y=iris_df["petal width (cm)"]
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    return X_train,X_test,y_train,y_test

def train_model(X_train,y_train,max_depth=4,min_samples_leaf=3,min_samples_split=2,random_state=42):
    tree=DecisionTreeRegressor(
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        min_samples_split=min_samples_split,
        random_state=random_state,
    )
    tree.fit(X_train,y_train)
    return tree

def evaluate_model(model,X_test,y_test):
    from sklearn.metrics import mean_squared_error as mse
    y_pred=model.predict(X_test)
    score=model.score(X_test,y_test)
    MSE=mse(y_pred,y_test)
    return MSE,score

def figure(iris_df,target="petal width (cm)"):
    features=iris_df.columns.drop(target)
    plt.figure(figsize=(15,4.5))
    for i,col in enumerate(features):
        ax=plt.subplot(1,len(features),i+1)
        ax.scatter(iris_df[col],iris_df[target])
        ax.set_title(col)
    plt.tight_layout()
    plt.savefig('iris_scatter.png', dpi=150)
    plt.show()