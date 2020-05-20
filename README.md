## 项目介绍：
基于MySQL的学生信息管理系统搭建，能实现注册登录，增删改查一键导入导出等功能。  
拥有GUI交互界面，底层和MySQL数据库连接，在界面操作实现和MySQL之间的数据信息交互。  

## 运行准备：
+ 需要安装的第三方库：pymysql、pandas、cryptography、openpyxl（建议版本2.4.9 不可用3.0以上）、xlrd
+ 安装Mysql，且保证Mysql为开启服务状态（建议8.0以上）
+ 修改 preset.py 文件第8行括号内的  password='121031' 的 121031 修改为你自己mysql的root用户密码
+ 修改 preset.py 文件第57行括号内的 ‘密码' : ['121031'] 的 121031 修改为你自己mysql的root用户密码
+ 修改 main.py 文件第371行括号内的  password='121031' 的 121031 修改为你自己mysql的root用户密码

## 效果截图：
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/1.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/2.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/3.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/4.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/5.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/6.png)
![](https://github.com/PantsuDango/mysql_student_info/blob/master/image/7.png)
