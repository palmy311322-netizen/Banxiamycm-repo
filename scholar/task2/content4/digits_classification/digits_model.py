import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_digits

digits=load_digits()

def load_data():
    data=digits.data
    feature_names=digits.feature_names
    df=pd.DataFrame(data, columns=feature_names)
    df['target']=digits.target
    return df

def split_dataset(df_digits):
    from sklearn.model_selection import train_test_split
    X=df_digits.drop('target',axis=1)
    y=df_digits['target']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    return X_train,X_test,y_train,y_test

def train_model(model,X_train,y_train):
    model.fit(X_train,y_train)
    return model

def evaluate_model(model,X_test,y_test):
    y_pred=model.predict(X_test)
    score=model.score(X_test,y_test)
    return score

def figure(df_digits):
    X=df_digits.drop('target',axis=1)
    plt.figure(figsize=(20,10))
    for i in range(10):
        ax=plt.subplot(2,5,i+1)
        ax.imshow(X.iloc[i].values.reshape(8,8),cmap='gray')
        ax.set_title(f'target={df_digits["target"].iloc[i]}')
        ax.axis('off')
    plt.tight_layout()
    plt.savefig('digits_images.png',dpi=150)
    plt.show()

def show_image(i=0):
    plt.figure(figsize=(4,4))
    plt.imshow(digits.images[i],cmap='gray')
    plt.title(f'target={digits.target[i]}')
    plt.axis('off')
    plt.savefig(f'digit_{i}.png', dpi=150)
    plt.show()


