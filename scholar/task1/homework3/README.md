#**HOMEWORK3**
##**代码介绍**
这期作业主要是构建一个学生成绩管理系统  
###model.py
这个模块主要定义和实现了Student类和Classroom类。  
|类|函数名|功能|
|:---:|:---:|:---:|
|Student|__init__|-|
|Student|add_subject(self,subject_name='Chinese',subject_grade=0.0)|增加科目和相应成绩|
|Student|average(self)|求各科平均分|
|Student|highest_subject(self)|求各科最高分|
|Student|total(self)|求该学生总分|
|Student|__str__(self)|-|
|Classroom|__init__(self)|-|
|Classroom|add(self,student)|增添学生|
|Classroom|find_by_id(self,id)|按学号（键）查找|
|Classroom|find_by_name(self,name)|按姓名查找|
|Classroom|remove(self,student)|删除学生|
|Classroom|update(self,id,name=None,grade=None)|修改学生信息|
|Classroom|rank(self)|排序|
|Classroom|quick_sort(self,member_grade)|辅助排序|
|Classroom|subject_stats(self,subject)|计算单科数据|

###storage.py
关于pickle的内容，确实了解不太多啊，所以这里经过了一些学习  
这个模块主要有两个函数：  
load_data() 这里在开启时载入存档数据。用try except保护了一下，没有存档就新建存档  
save_data() 这里在退出时保存存档数据。  

###main().py
这里主要就是一个略显简陋的循环交互。  
根据input的数字来进行交互，直到输入'0'，返回。  
这里面最重要的就是异常处理语句。重点保护的对象是  
1. 如果首次运行没有存档，要新建一个存档。这里主要放在了storage.py里面实现。  
2. 学号不存在。这里的交互场景应该是5（输入学号，删除学生）和6（输入学号修改学生信息）。  
这在里，5我运用了try-except的语句来保护，6我使用了student=classroom.find_by_id(sid)，如果找不到，直接continue，避免了可能找不到键的情况  
3. 输入非数字。这里主要是在涉及到成绩（数字）的输入的时候使用try-except保护。

##**思考题**
嘻嘻，不会。不过，这个应该是思考题，我思考的想法是：
||pickle|csv|
|:---:|:---:|:---:|
|优点|这个是二进制文件，它读写起来的速度肯定要比csv快|csv可以随时打开查看，并且不是仅支持py一种语言|
|缺点|应该只能支持py一种语言，并且甚至只能支持这个特定的对象|读写慢，而且他的模式应该是比较单调的，表格嘛|

然后，询问询问AI...  
pickle   
优点：  
• 可以直接序列化 Python 对象（类实例、字典、列表等），无需手动转换  
• 支持复杂数据结构，如嵌套对象、自定义类  
• 读写速度快，二进制格式  
缺点：  
• Python 专用，其他语言无法读取  
• 二进制格式，人类不可读  
• 版本兼容性差，Python 版本升级后可能无法读取旧文件  
• 存在安全风险  

csv  
优点：  
• 纯文本格式，人类可读可编辑  
• 通用格式，几乎所有语言和工具都支持（Excel、数据库等）  
• 跨平台、跨语言兼容性好  
• 无安全风险  
缺点：  
• 只能存储字符串和数字，不能直接存储复杂对象  
• 需要手动做类型转换（读取后字符串要转回 float/int）  
• 不支持嵌套结构，需要自己设计格式  

pickle 的安全风险  
pickle 在反序列化（pickle.load()）时会执行文件中保存的任意 Python 代码。如果攻击者篡改了 pkl 文件，可以：  
1. 执行任意代码：比如删除文件、安装后门、窃取数据  
2. 读取敏感信息：访问环境变量、密钥等  
3. 拒绝服务：构造恶意数据导致程序崩溃或死循环  

这里毕竟是本地临时存储一下，所以用pickle还是很省事的！  
运行了一下，成功创建了这个__pycache__。然后进行一系列的测试。