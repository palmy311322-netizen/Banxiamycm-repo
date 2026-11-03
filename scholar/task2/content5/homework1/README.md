#HOMEWORK1

##简介
HOMEWORK1主要是内容2和内容4的实际应用。  
我在UCI里面下载了六个用于回归任务的数据集然后写了一个```download.py```脚本来把这些数据集转变成了```.csv```文件（```download.py```脚本已经被我删了，不在此目录下）：
```
student_performance.csv
aids_clinical_trials_group_study_175_dataset.csv
auction_verification_dataset.csv
power_consumption_of_tetouan_city_dataset.csv
seoul_bike_sharing_demand_dataset.csv
wine_quality_dataset.csv
```
使用本地文件导入，可以避免网络、版本等因素，鲁棒性强。  

```data_loader.py```模块用于**数据库的导入和```X```，```y```的划分**；  
```experiment.py```模块用于**模型的导入、训练和计算指标**；  
```main.py```模块用于**计算和制表**。

##代码介绍  
###```data_loader.py```  
将六个数据集的键分别定为A,B,C,D,E,F，对表格里面的列进行审查和删除：  
|数据集|删除的列|原因|
|:---:|:---:|:---:|
|A|```G1```,```G2```|前两学期的成绩和第三学期高度相关，而且没必要在这里算一遍|
|B|```cid```|这只是病例的编号罢了|
|C|```verification.time```|验证过程的时间？似乎没用|
|D|```DateTime```|时间戳，删了吧|
|E|```Date```|同上同上|
|F|无|都很有用啊|

在```load_data(name)```函数中，使用```pd.read_csv()```读取csv文件，存储为DataFrame形式。  

在```load_xy(name)```函数中，分别按照前面的规则划分```X```,```y```并返回。  

###```experiment.py```  
```train_model(keyword,X_train,y_train)```函数用于训练模型。这里使用的model是来自前面的复制品。  
计算五折交叉验证后的RMSE。

###```main.py```  
主模块中，调用前面写的两个模块，主要使用了以下的功能：  
遍历A~F数据集->  
划分```X```,```y```->  
```analyze_rmse(name,X,y,folds=5,seed=42)```使用```cross_validate_rmse(name,X,y,folds=5,seed=42)```实现五折交叉验证下的RMSE->  
制表->  
展示```A±B```

##实验结果与分析  
将实验表格展示如下：  
|数据集\回归模型|LinearRegression|RandomForest|GradientGoosting|
|:---:|:---:|:---:|:---:|
|A|2.7533±0.2824|2.7114±0.3510|2.7851±0.3545|
|B|245.2290±3.8042|244.3937±4.8043|242.6978±5.7866|
|C|0.3178±0.0069|0.0714±0.0127|0.1507±0.0036|
|D|3057.9898±16.3610|1051.6283±8.3273|1946.9472±33.9800|
|E|433.0349±9.1695|232.7397±7.5884|257.3650±7.0558|
|F|0.7364±0.0032|0.6074±0.0044|0.6843±0.0083|

怎么这个数量级差了那么大啊...  
我们还是分开分析一下吧！  
数据集A和B在三个回归模型下，差异大概1%，也许只是能算得上噪声吧。我们的结论是，这两组数据近似线性，使用树模型完全没有额外增益啊！  
C~F四组，都是在树模型中取得了较好的效果！证明这四组数据集可能非线性比较强。  
再比较*随机森林*和*梯度提升*，发现随机森林的回归效果略好于梯度提升。  

