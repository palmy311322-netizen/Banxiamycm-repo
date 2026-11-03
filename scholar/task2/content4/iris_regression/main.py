import iris_model

def main():
    df=iris_model.data_load()

    X_train,X_test,y_train,y_test=iris_model.split_dataset(df)

    model=iris_model.train_model(X_train,y_train)

    MSE,score=iris_model.evaluate_model(model,X_test,y_test)
    print(f"均方误差：{MSE:.3f}, 得分：{score:.3f}")

    iris_model.figure(df)

if __name__=="__main__":
    main()
