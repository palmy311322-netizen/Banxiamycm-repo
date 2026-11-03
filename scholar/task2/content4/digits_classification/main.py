import digits_model
from sklearn.linear_model import LogisticRegression

def main():
    df=digits_model.load_data()

    df.to_csv("digit_dataset.csv",index=False)
    print(f"数据形状：{df.shape}")
    print(df.head())

    X_train,X_test,y_train,y_test=digits_model.split_dataset(df)
    print(f'训练集大小：{X_train.shape}，测试集大小：{X_test.shape}')

    model=LogisticRegression(max_iter=5000)
    model=digits_model.train_model(model,X_train,y_train)

    score=digits_model.evaluate_model(model,X_test,y_test)
    print(f'得分：{score:.4f}')

    digits_model.show_image(1)
    digits_model.figure(df)

if __name__=='__main__':
    main()
