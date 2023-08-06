# 消息中心, 避免代码的强耦合性, 支持多线程

### zmsgcentre是什么
> zmsgcentre是一个消息中心, 整个程序所有的模块和函数引用都不需要直接调用了, 而是通过消息中心进行转发, 极大的降低代码耦合性

### 为什么需要降低代码耦合性
> 在开发大型程序的时候难免会出现代码的强耦合性, 这是一个危险的设计, 假设你在维护你的程序时, 将某个函数名或参数改变了, 那么所有调用这个函数的代码都必须同时更改, 如果是少数则改代码很简单.
+ Q: 如果是几十个甚至上百上千个地方引用了这个函数怎么办?
+ A: 你告诉我你时间多没关系慢慢改.
+ Q: 万一忘记了一两处没改怎么办?
+ A: ctrl+f全局替换就行了.
+ Q: 如果你的函数名是多用的呢, 如: 函数名为'AA', 或者某个函数名为'AAX', 某一处字符串为'AABC', 你还能淡定么?
+ A: 正则表达式替换...
+ Q: 新的函数名或参数是否会和其他函数产生冲突, 你的任何一处代码更改, 需花费10倍以上的时间来评估整个程序的健壮性, 更改后多个模块之间是否会冲突, 出现隐藏bug如何调试
+ A: emmmmm.....

### 如何使用zmsgcentre
使用zmsgcentre你需要明白sender角色, receiver角色以及msg_tag
+ sender可以理解为一个广播电台.
+ msg_tag就是广播电台的频率
+ receiver就是接收电台消息的接收器

### 它有什么优点
+ 一次发送广播可以被多个接收器接收.
+ 线程安全.
+ 支持标签级别线程锁.
+ 允许在接收器回调函数中创建和销毁接收器, 销毁消息标签.
+ 理解简单, 无需消息订阅系统那么复杂的创建topic和消费者观念.
+ 使用方便, 发送者和接受器只需要一行代码定义, 不影响代码阅读性, 让代码逻辑更简单
+ 代码开源, 精简, 整个模块只有3.5kb.

###  一个简单的实例
```python
import zmsgcentre # 导入zmsgcentre模块

def receiver_func(a):
    print(a)

zmsgcentre.create_receiver('test_tag', receiver_func) # 创建一个接收器, 接收消息标签为'test_tag'的内容
zmsgcentre.send('test_tag', '广播数据') # 发送广播到'test_tag'
```

### 多模块实例
+ manager.py

```python
import zmsgcentre

import test_A
import test_B

def send(data):
    return zmsgcentre.send('test_tag', data) #发送广播到'test_tag'

if __name__ == '__main__':
    result = send('主模块发送来的消息')
    print(result) # send返回一个列表, 这个列表包含所有接收器的返回值(无序), 无接收器返回一个空列表
```

+ test_A.py

```python
import zmsgcentre

def receiver_func_a(data):
    print(data)
    return 'test_A已收到'

zmsgcentre.create_receiver('test_tag', receiver_func_a) # 创建接收器, 指定消息标签, 绑定回调函数
```

+ test_B.py

```python
import zmsgcentre

def receiver_func_b(data):
    print(data)
    return 'test_B已收到'

zmsgcentre.create_receiver('test_tag', receiver_func_b) # 创建接收器, 指定消息标签, 绑定回调函数
```

### 使用装饰器简化代码
+ manager.py

```python
import zmsgcentre

import test_A
import test_B

@zmsgcentre.sender('test_tag') # 创建广播器, 指定广播的消息标签, 绑定广播入口为send函数
def send(data):
    pass # 无需任何代码, 写了也不会执行这里的代码, 因为没必要.

if __name__ == '__main__':
    result = send('主模块发送来的消息')
    print(result)
```

+ test_A.py

```python
import zmsgcentre

@zmsgcentre.receiver('test_tag') # 创建接收器, 指定消息标签, 绑定回调函数
def receiver_func_a(data):
    print(data)
    return 'test_A已收到'
```

+ test_B.py

```python
import zmsgcentre

@zmsgcentre.receiver('test_tag') # 创建接收器, 指定消息标签, 绑定回调函数
def receiver_func_b(data):
    print(data)
    return 'test_B已收到'
```
###### 注: 即使使用了装饰器定义了一个接收器, 仍然可以主动调用它, 如上可以不通过消息中心直接调用receiver_func_b

### 接收器优先级
``` python
import zmsgcentre

# priority表示优先级, 你可以简单理解为接收器到广播器的距离, 数字越小越先收到消息, 数字相等的接收器收到消息顺序随机
@zmsgcentre.receiver('test_tag', priority=999)
def receiver_func(a):
    print(a)
```

### 更新日志
发布时间|发布版本|发布说明
--|:--:|---
19-01-10 | 2.0.0 | <li>新增了接收器优先级</li> <li>优化了接收器函数中创建和销毁接收器的逻辑, 用户不需要再去判断是否强制使用线程来创建销毁接收器</li> <li>优化了多线程安全</li> <li>更改了所有函数名</li>
18-10-05 | 1.0.3 | 这是v1版本的最后一版, 将不再更新, 请使用最新版本

- - -
##### 本项目仅供所有人学习交流使用, 禁止用于商业用途
