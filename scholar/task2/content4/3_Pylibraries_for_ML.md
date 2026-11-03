```scikit-learn```主要用于做机器学习，比如回归，分类，聚类，模型评估等。  
以下是```scikit-learn```中的常用操作。  
|操作|写法|说明|
|:---:|:---:|:---:|
|加载数据|```load_iris()```,```make_classification()```|示例数据，模拟数据|
|划分训练集和测试集|```train_test_split(X, y, test_size=0.2)```|按比例拆分数据|
|数据标准化|```StandardScaler().fit_transform(X)```|把数据缩放到均值0、方差1|
|数据归一化|```MinMaxScaler().fit_transform(X)```|把数据缩放到0~1之间|
|训练模型|```model.fit(X_train, y_train)```|用训练数据拟合模型|
|预测|```model.predict(X_test)```|用模型对测试集做预测|
|分类准确率|```accuracy_score(y_test, y_pred)```|预测正确的比例|
|回归均方误差|```mean_squared_error(y_test, y_pred)```|预测值与真实值的差距|
|交叉验证|```cross_val_score(model, X, y, cv=5)```|5折交叉验证评估模型|
|保存模型|```joblib.dump(model, 'model.pkl')```|把训练好的模型保存到文件|
|加载模型|```joblib.load('model.pkl')```|从文件加载已保存的模型|

以下是```scikit-learn```中常用的模型。  
|模型|写法|说明|
|:---:|:---:|:---:|
|线性回归|```LinearRegression()```|用直线拟合数据，做回归预测|
|逻辑回归|```LogisticRegression()```|虽然叫回归，但其实是做分类的|
|K近邻|```KNeighborsClassifier()```|看最近的K个邻居属于哪类|
|决策树|```DecisionTreeClassifier()```|像流程图一样一层层做判断|
|随机森林|```RandomForestClassifier()```|很多棵决策树投票决定结果|
|支持向量机|```SVC()```|找到一个最优的分割面来分类|
|朴素贝叶斯|```GaussianNB()```|基于概率的分类方法|
|K均值聚类|```KMeans(n_clusters=3)```|把数据自动分成K个簇|
|PCA降维|```PCA(n_components=2)```|把高维数据降到2维或3维，方便可视化|

```pandas```常用于表格数据处理，比如CSV，Excel，DataFrame。
> 什么是DataFrame？
>简单来说，DataFrame就是Python数据分析中的“超级表格”。它是```Pandas```库中最核心的二维数据结构，也是后续进行数据清洗和机器学习建模的基础底座。
>它的核心特点可以总结为以下三点：
>1. 结构像Excel：由行（记录）、列（特征/变量）和索引组成，非常直观。
>2. 能力远超 Excel：能轻松处理百万级以上的大规模数据，支持高效的向量化计算（一行代码搞定整列运算），并且擅长处理缺失值和重复数据。
>3. 生态核心地位：它是连接原始数据与算法模型的桥梁，可以无缝对接```matplotlib```进行可视化，或直接喂给```Scikit-learn```等机器学习库进行训练。  

以下是```pandas```中的常用操作。  
|操作|写法|说明|
|:---:|:---:|:---:|
|创建数据|```pd.DataFrame({'A':[1,2], 'B':[3,4]})```|用字典创建一个DataFrame|
|读取CSV|```pd.read_csv('data.csv')```|从CSV文件读取数据|
|读取Excel|```pd.read_excel('data.xlsx')```|从Excel文件读取数据|
|保存CSV|```df.to_csv('data.csv', index=False)```|把DataFrame保存为CSV文件|
|查看前几行|```df.head()```|查看前5行数据|
|查看基本信息|```df.info()```|查看行列数、数据类型、缺失值|
|查看统计摘要|```df.describe()```|查看均值、最值、标准差等统计量|
|选择列|```df['列名']```|取出某一列数据|
|插入列|```df.insert(索引值,'新列名',[1,2])```|按索引值插入新列|
|插入列|```df['新列名']=[1,2]```|在尾端插入新列|
|筛选数据|```df[df['年龄']>18]```|按条件筛选行|
|排序|```df.sort_values('列名')```|按某一列排序|
|删除列|```df.drop('列名', axis=1)```|删除指定的列|
|处理缺失值|```df.fillna(0)```,```df.dropna()```|填充或删除缺失值|
|分组统计|```df.groupby('列名').mean()```|按某列分组后求均值|
|合并数据|```pd.merge(df1, df2, on='key')```|按某一列合并两个表|
|上下拼接|```pd.concat([df1, df2])```|把两个表按行摞在一起（列名相同的上下堆叠）|
|左右拼接|```pd.concat([df1, df2], axis=1)```|把两个表按列并排拼在一起（行索引对齐）|

```matplotlib```常用于数据可视化，比如折线图，柱状图，散点图，直方图。
以下是```matplotlib```中的常用操作。
|操作|写法|说明|
|:---:|:---:|:---:|
|画折线图|```plt.plot(x, y)```|用线连接数据点|
|画柱状图|```plt.bar(x, y)```|用柱子表示数据大小|
|画散点图|```plt.scatter(x, y)```|用点表示两个变量的关系|
|画直方图|```plt.hist(data, bins=10)```|展示数据的分布情况|
|画饼图|```plt.pie(sizes, labels=names)```|展示各部分占总体的比例|
|添加标题|```plt.title('标题')```|给图加一个标题|
|添加坐标轴标签|```plt.xlabel('X')```,```plt.ylabel('Y')```|给X轴和Y轴加标签|
|显示图形|```plt.show()```|把画好的图显示出来|
|保存图片|```plt.savefig('fig.png')```|把图保存为图片文件|
|设置图片大小|```plt.figure(figsize=(8, 6))```|设置图的宽度和高度|
|创建子图|```plt.subplot(2, 2, 1)```|在一个窗口中画2×2的子图，选中第1个|
|防止子图重叠|```plt.tight_layout()```|自动调整子图间距，避免标签互相遮挡|