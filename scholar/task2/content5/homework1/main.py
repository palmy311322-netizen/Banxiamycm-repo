import pandas as pd
import data_loader
import experiment

def main():
    table={}
    for dataset in data_loader.list_datasets():
        X,y=data_loader.load_xy(dataset)
        table[dataset]={}
        for model in experiment.MODELS:
            mean,std=experiment.analyze_rmse(model,X,y)
            table[dataset][model]=f"{mean:.4f}±{std:.4f}"

    result=pd.DataFrame(table).T
    print("5折交叉验证RMSE（均值±标准差）")
    print(result.to_string())

if __name__=="__main__":
    main()
