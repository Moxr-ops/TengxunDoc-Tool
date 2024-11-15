# 腾讯文档自动化控件

为了抢志愿写的

实现了定时开始自动填写收集问卷

基本上可以在1s内完成问卷填写

### 使用教程：
1、先配置好python环境

2、下载与自己浏览器版本匹配的浏览器驱动

3、相关依赖库使用pip install下载

4、在本文件夹目录下打开命令行窗口，执行：
```
python main.py
```
5、按提示操作

~~6、bug满天飞~~

~~7、自己手动填写~~

~~8、问卷光速停止收集~~

~~9、没有志愿可做~~

~~10、无法毕业（~~

### 还有几个不足之处：

需要依赖浏览器驱动，如果本库中的浏览器驱动与用户的浏览器版本不匹配，需要用户自行下载驱动

不能实现无头浏览器运行

在用户提交下拉表单类问题的答案索引时，即使超出范围也不会被判定

开始自动填写之前应该先检测问卷是否已经开放，如果还没开放应执行刷新页面等操作，以提高代码可靠性

对于只有两个选项的下拉表单类问题，当用户输入的答案索引为“1”时会填写失败，原因不详

由于代码为作者边学边写，且作者学习能力不咋地，所以代码如史如山，仅仅是能跑起来（

