from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score

MODELS={
    "LinearRegression":LinearRegression(),
    "RandomForest":RandomForestRegressor(n_estimators=100, random_state=42),
    "GradientBoosting":GradientBoostingRegressor(random_state=42),
}

def get_model(name):
    if name not in MODELS:
        raise KeyError(f"没有找到匹配的模型：{name}")
    return clone(MODELS[name])

def train_model(keyword,X_train,y_train):
    model=get_model(keyword)
    model.fit(X_train,y_train)
    return model

def cross_validate_rmse(name,X,y,folds=5,seed=42):
    cv=KFold(n_splits=folds,shuffle=True,random_state=seed)
    scores=cross_val_score(get_model(name),X,y,cv=cv,scoring="neg_root_mean_squared_error")
    return -scores

def analyze_rmse(name,X,y,folds=5,seed=42):
    rmse=cross_validate_rmse(name,X,y,folds,seed)
    A=rmse.mean()
    B=rmse.std()
    return A,B