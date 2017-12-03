# Flask+Echarts数据可视化

See [My Blog](http://xxuan.me/2017-03-13-mongodb-flask-echarts-data-visualize.html)

## Dependencis (Ubuntu 14.04/16.04)

1. flask
[flask中文文档](http://docs.jinkan.org/docs/flask/)

 ```bash
$ sudo pip install Flask
```

## Test

```bash
$ python visualization/view.py
```

进入`127.0.0.1:8080`下预览吧

---

## 关于这个repo

1. 这个看起来很fancy的repo默默成了我star最多的repo...本着尽责的态度, 决定把代码整理一下
2. repo建立之初使用了py2, 为此花了巨量精力解决中文编码/解码的问题. 现已迁移至py3, 少了无数坑. 欢迎使用py3
3. 前后端已经分离. 现在的代码很简单, 也和scrapy/mongodb无关了. 
4. 现在这个repo只是将以json格式保存的数据使用[flask](https://github.com/pallets/flask)加载到了网页上并用[Echarts](https://github.com/ecomfe/echarts)的代码渲染成图表
5. 因此使用什么样的方法获得这样的json数据就因人而异了. 请尽情使用你喜欢的手段, 无论是用json文件做缓存还是直接读取数据库. 整理成dict喂给`view.py`里的`data`就行了

## About this project
1. This repo is about loading data from json file then rendering it using [flask](https://github.com/pallets/flask) & [Echarts](https://github.com/ecomfe/echarts).
2. You can use any method to get the data, rather than using scrapy + mogodb to update static json files in this repo.