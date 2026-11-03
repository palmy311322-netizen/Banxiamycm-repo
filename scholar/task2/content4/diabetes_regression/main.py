import diabetes_model
from sklearn.linear_model import LinearRegression

def main():
    df=diabetes_model.load_data()

    df.to_csv("diabetes_dataset.csv",index=False)
    print(f'数据形状：{df.shape}')
    print(df.head())

    X_train,X_test,y_train,y_test=diabetes_model.split_dataset(df)
    print(f'训练集大小：{X_train.shape}，测试集大小：{X_test.shape}')

    model=LinearRegression()
    model=diabetes_model.train_model(model,X_train,y_train)

    score,MSE=diabetes_model.evaluate_model(model,X_test,y_test)
    print(f'得分：{score:.4f}')
    print(f'均方误差：{MSE:.4f}')

    w,b=diabetes_model.model_params(model)
    print(f'系数：{w}')
    print(f'截距：{b}')

    diabetes_model.figure(df)

if __name__=='__main__':
    main()
