from pathlib import Path
import pandas as pd

DATASET_DIR=Path(__file__).parent/"dataset"

DATASET_FILES={
    "A":"student_performance.csv",
    "B":"aids_clinical_trials_group_study_175_dataset.csv",
    "C":"auction_verification_dataset.csv",
    "D":"power_consumption_of_tetouan_city_dataset.csv",
    "E":"seoul_bike_sharing_demand_dataset.csv",
    "F":"wine_quality_dataset.csv",
}

TARGETS={
    "A":{"target":"G3","drop":["G1", "G2"]},
    "B":{"target":"time","drop":["cid"]},
    "C":{"target":"verification.result", "drop":["verification.time"]},
    "D":{"target":"Zone 1 Power Consumption","drop":["DateTime"]},
    "E":{"target":"Rented Bike Count","drop":["Date"]},
    "F":{"target":"quality","drop":[]},
}

def list_datasets():
    return list(DATASET_FILES)

def load_dataset(name):
    if name not in DATASET_FILES:
        raise ValueError(f"未知数据集：{name}")
    return pd.read_csv(DATASET_DIR/DATASET_FILES[name])

def load_xy(name):
    df=load_dataset(name)
    target=TARGETS[name]["target"]
    drop=TARGETS[name]["drop"]
    y=df[target]
    X=df.drop(columns=[target] + drop)
    X=pd.get_dummies(X,drop_first=True,dtype=int)
    return X,y

def load_all():
    return {name: load_dataset(name) for name in DATASET_FILES}
