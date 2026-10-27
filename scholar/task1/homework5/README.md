#**HOMEWORK5**  
##**代码介绍**  
终于做到作业五了啊...  
我先从我的服务器上导出了运行日志啊，重命名为access.log。  
#log_analyzer.py
*用正则表达式设计带分组的模块*  
|写法|含义|
|:---:|:---:|
|(?P<ip>\S+)|匹配非空白字符，即IP的特点|
|\s+\S+\s+\S+\s+|匹配日志中的占位符和空格|
|\[(?P<time>[^\]]+)\]|不要[]，匹配时间|
|\s+"(?P<method>\S+)|提取请求方法|
|\s+(?P<url>\S+)|提取URL路径|
|\s+\S+|匹配这个HTTP/1.1"|
|\s+(?P<status>\d{3})|提取状态码|
|\s+(?P<bytes>\d+)|提取响应字节数|

正则表达式还是需要多练习啊...写这个代码的时候，我尚且不太会使用正则表达式啊，然后让AI生成了相应的正则表达式的写法。  
在这次作业文件夹里面，我加了一个，额额，学习正则表达式的，表格？参见regex.md。  

用map和lambda将bytes_list的元素全都转化成整数，方便直接就能实现运算了（求和，平均之类的）。  
用map和lambda把这个状态码只保留第一位，后面的全部替换成'xx'，这里面只在意第一个字符，所以这样写，更方便后面的分类。  

统计每个ip的错误请求次数，这里建了一个字典，键是ip，值是错误请求次数。划分标准正是'4xx'/'5xx'。输出TOP5就是直接用的快排。  

使用set找不同呐，这里先用建morning_ips和afternoon_ips两个集合，morning_ips-afternoon_ips就是只在上午出现过的，afternoon_ips-morning_ips就是只在下午出现过的，二者取交集，就是上下午都出现过的。  

脱敏处理这一步，正则表达式匹配到原有的ip，然后用sub()替换，写入新文件即可。  

*最后一步生成分析报告*  
原来做的一些伏笔有用了，把byte_list的全部元素转化成整数，很方便算总流量啊。  
独立ip数应该也是使用set。其他的都是简单的数学运算了。  

##**加分项**
我用 tkinter 做了一个超级简陋的 GUI。  

tkinter 是 Python 自带的 GUI 库。基本思路是：
1.  `tk.Tk()` 创建主窗口
2.  `tk.Frame()` 创建容器，用来组织其他组件
3.  `tk.Entry()` 文本输入框
4.  `tk.Button()` 按钮，点击触发函数
5.  `tk.Text()` 多行文本框，用来显示结果
6.  `.pack()` 方法把组件放到窗口里

我主要在上面放个文件选择框，中间放个文本框，下面放个按钮。点按钮就调用analyze_file()，把报告塞进文本框里显示。

核心代码其实就这几行：
```python
root=tk.Tk()
entry=tk.Entry()
text=tk.Text()
button=tk.Button(text='开始分析',command=run)
root.mainloop()#启动事件循环（跟AI学的）
```
##**思考题**
**会失效啊**。。。（悲）
我这里的用于匹配request的正则表达式是  \s+["＂](?P<request>[^"＂]*)["＂]  
我想要得到的request的格式是形如这样的:＂GET /sample.html HTTP/1.1＂  
那要是ULR里面包含["＂]，那肯定会直接歇菜。这是一个反例。  
另外一个反例，要是ULR里面有连续的空格，或者制表符，换行符，那还是不行。原因是如下：  
＂GET /sample  a.html HTTP/1.1＂->GET,sample,a.html,HTTP/1.1->  
掐头去尾，留下了sample,a.html->sample a.html，这就失真了啊555...  

想一个解决方案出来。  
修改这里的正则表达式：  
```python
         r'\s+"(?P<request>.+)"'
```
然后给request.split()来个参数' '，固定按照单空格划分。
```python
def split_request(request):
    parts=request.split(' ')
    if not parts:
        return '','',''
    if len(parts)==1:
        return parts[0],'',''
    if HTTP_VERSION.fullmatch(parts[-1]):
        return parts[0],' '.join(parts[1:-1]),parts[-1]
    return parts[0],' '.join(parts[1:]),''
```
