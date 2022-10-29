
my-mac mysql5.7 第一次启动过程

安装到可以使用
1. 检查是否存在mysq  mysql --version
2. brew命令行安装  brew install mysql@5.7 
  # 安装成功时，可以看见安装目录，复制下来
3. 配置全局变量 
  open .zshrc 文件 配置文件可能是 .bash_profile
  添加
  # mysql5.7 
  export PATH=$PATH:/opt/homebrew/opt/mysql@5.7/bin
  加载资源 source .zshrc
4. 安装成功时，提示执行 mysql_secure_installation
5. 第四步，可能会执行失败，此时，需要先启动mysql
  启动命令: 
  mysql.server start
  mysql -h localhost -u root -p # 第一次不用输入密码，直接按回车键进入
  输入 use mysql; ，修改root的密码：
  update user set authentication_string=password('新密码') where user='root';
  更新 flush privileges;
  退出：quit;
  再次重启mysql： mysql.server start
  测试是否成功就是是否登陆成功咯 mysql -u root -p 此时就可以输入新密码了
  # 第5步，参考资料 https://www.cnblogs.com/winton-nfs/p/12956811.html


  新建数据库时
  选择字符集 utf8 -- utf8-8 unicode
  排序规则 utf8_general_ci

## 美多商城
  
  ### 数据库导入
  进入到指定文件夹下
  执行 mysql -uroot -p meiduo < dump.sql 
  输入mysql 密码  回车，成功则推出命令行

  此数据库中用户名密码是[users_user表]  admin  admin123
  其他用户的密码是  8个1

  ### 添加虚拟环境
  pycharm -> perfermance -> 

  ### 安装依赖
  pip install -r re



  数据库问题一
  1. 支持中文内容输入

  在navicat 中操作数据库
  1. 新建数据库
  2. 在数据库中 新建表
  3. 定义表字段、定义
  4. 更新表字段、定义
  5. 导出表，数据库
  6. 复制一张表
  7. 将a数据库，复制到b数据库中 ？【数据传输功能】
    将线下的数据库拷贝到线上

pycharm 快捷键
F8 断点跳过，直接到达下一个断点处
查看所有快捷键 可以导入其他编辑器的快捷键 keymap
有些快捷键同 android studio


安装虚拟环境 [参考资料](https://zhuanlan.zhihu.com/p/137624513)
第1步 ：安装virtualenv和virtualenvwrapper

``` pip3.6 需要依据不同python版本使用
# 可以创建虚拟环境
pip3.6 install -i https://mirrors.aliyun.com/pypi/simple virtualenv 
# 可以通过workon全局命令管理(尽量不要在虚拟环境文件夹内的位置去执行此命令) 各个虚拟环境
pip3.6 install -i https://mirrors.aliyun.com/pypi/simple virtualenvwrapper
```

第2步，创建管理虚拟环境的根目录
  - 首先，我想创建一个统一管理虚拟环境的目录，这样的话，以后所有的虚拟环境全部放到这个文件夹下面统一管理。( 这个文件夹也就是 WORKON_HOME 对应的参数，在下一步中要被一起添加进环境变量)
  - 这里我将这个虚拟环境的根文件夹设置在/Documents(文稿)文件夹内，( 一般设置在用户根目录，就是 在终端 输入 cd ~ 的目录 )

```
cd Documents  # 进入文稿目录
mkdir python_envs  # 在文稿目录下创建了一个统一管理虚拟环境的目录
```
  - 以后你想要在这个目录下创建虚拟环境，你就需要cd Documents/python_envs然后通过 virtualenv 环境名 或者 mkvirtualenv 环境名(没生效) 来创建虚拟环境

第3步，配置环境变量
  - 查找python3和virtualenvwrapper.sh的安装位置 ，用which命令查找
  ```
  注：如果你使用，which python3命令查到的只是快捷方式的路径/usr/local/bin/python3.6，你需要知道的是，这并不是源文件所在的目录。
具体的，自己安装的python3的安装位置一般是/Library/Frameworks/Python.framework/Versions/3.6
  ```

  ```
  which python3
# 一般来说，得到的结果是 /usr/local/bin/python3
which virtualenvwrapper.sh
# 一般来说，得到的结果是 /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh
  ```

- 然后配置成环境变量
```
export WORKON_HOME='/Users/你的用户名/Documents/python_envs'
# 上面是我想创建的地址的位置 可根据自己的需要调整
export VIRTUALENVWRAPPER_PYTHON='/Library/Frameworks/Python.framework/Versions/3.6/bin/python3'
source /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh
```
  - 此处有个坑点需要注意
    - 把virtualenvwrapper.sh执行一下
    ``` 注意 . 后面有个空格
    . /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh
    ```

    ``` 加载全局配置
    source ~/.zshrc
    或者 source ~/.bash_profile
    ```

第4-1步，创建并进入虚拟环境 [Python创建、退出虚拟环境](https://blog.csdn.net/weixin_43463712/article/details/90210108)
```
首先:
cd Documents/python_envs

# 方式1:(全局生效)
mkvirtualenv envname01  # 创建完毕会自动进入该虚拟环境

# 方式2: (好使)
virtualenv envname02
workon envname02  # 进入该虚拟环境

# 方式3:
virtualenv envname03
cd envname03
source bin/activate  # 激活并进入虚拟环境
```

```额外补充
# 退出虚拟环境 
deactivate
# 查看虚拟环境中安装了哪些包
pip3.6 list
# 查看虚拟环境 是在退出虚拟环境的情况下查看的
workon
# 选择进入某个虚拟环境
workon myvenv
# 用它一次性通过在别的机器上或虚拟环境里，将文件里列出的第三方库安装起来。只需要使用命令
pip3.6 install -r requirements.txt
# 创建虚拟环境： $ virtualenv -p /usr/bin/python2.7  my_venv
# 启动虚拟环境： $ source my_venv/bin/activate　
# 退出虚拟环境： $ deactivate　
# 删除虚拟环境（原来就是直接删除对应的文件夹即可）： $ rm –r my_venv
# 卸载包 pip3.6 uninstall backage_name
# 切换虚拟环境：workon envname02  # 这里写你要去的虚拟环境的文件夹名

# 使用豆瓣源加速安装某虚拟环境内的包 （进入虚拟环境内，可统一使用pip指令）
# pip install -i https://pypi.douban.com/simple 包名

# 在某个虚拟环境内，查看已经安装的虚拟包
# pip list

# 指定python版本创建虚拟环境
# mkvirtualenv -p /usr/bin/python3.7 virtualName
# mkvirtualenv --python=/usr/bin/python3.7 virtualName

# 为虚拟环境安装模块：pip install 模块名  |  pip3 install 模块名
# 为虚拟环境卸载模块：pip uninstall 模块名  |  pip3 uninstall 模块名
# 查看虚拟环境里安装了哪些包：lssitepackages  |  pip list  |  pip3 list
# 进入|退出 该虚拟环境的Python环境 python  |  exit()
# 复制虚拟环境：cpvirtualenv env1 env2  # 前面的是原文件 后面的拷贝后的新文件
      # ///   Copying env1 as env2...
# 删除虚拟环境：rmvirtualenv env2
```

第4-2步，配置虚拟环境内的包
  - 按照项目需求用 pip install 包名 或者 pip3 install 包名
  - 注意！不要加sudo，否则会安装到系统环境中，而不是安装到虚拟环境中
  ```
  pip3.6 install flask
  pip3.6 install django
  pip3.6 install Scipy 
  ```

第4-3步，退出环境
  deactivate


pip3.6 install -i https://pypi.douban.com/simple/ django
pip install -i https://pypi.douban.com/simple/ mysqlclient --no-cache-dir
pip install -i https://pypi.douban.com/simple/ pillow # 图片处理

# 批量安装依赖包
pip install -r requirements.txt 

linux 下安装虚拟环境
# 安装虚拟环境 sudo apt-get install python-virtualenv
# 创建一个虚拟环境名为py2: virtualenv py2
# 进入此虚拟环境 cd py2
# 启动虚拟环境 source bin/activate


[原始项目源码](https://github.com/liyaopinner/MxShop)

