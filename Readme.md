## 调试助手使用帮助

### 直接使用

如果不需要进行功能扩展，只需要使用`dist`目录下的内容即可。在启动前需要对`config/config.yaml` 进行配置。

数据保存目录默认在`/dist/data_save`下, 数据以`csv`的格式保存。

### 接收数据格式

+ 默认以空格来区分不同字段的数据,数据类型为 `float` 型的字符串

```python
<data1> <data2> <data3> <data4>
```
### 开发环境安装
> 如需要进行二次开发才需要安装此环境

最好使用`python3.6`及以上的python版本。

```python
pip install -r requirements.txt
```

### 待实现功能

+ 将通信协议与代码分离，实现用户自定义通信协议！
+ 实现数据收发窗口

