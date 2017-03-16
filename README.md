# Scrapy爬虫数据可视化

详见[我的blog](http://xxuan.me/2017-03-13-mongodb-flask-echarts-data-visualize.html)

## 安装 (Ubuntu 14.04/16.04)

1. apscheduler
[apscheduler官方文档](http://apscheduler.readthedocs.io/en/3.3.1/userguide.html)

 ```bash
$ pip install apscheduler
```

2. mongodb & pymongo

 [mongodb官方文档](https://docs.mongodb.com/getting-started/shell/tutorial/install-mongodb-on-ubuntu/), [pymongo官方文档](https://api.mongodb.com/python/current/installation.html)

 ```bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
# Ubuntu 14.04
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list
# Ubuntu 16.04
$ echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.4.list

$ sudo apt-get update
$ sudo apt-get install -y mongodb-org

# pymongo
$ python -m pip install pymongo
```

3. flask & flask-pymongo
[flask中文文档](http://docs.jinkan.org/docs/flask/), [flask-pymongo官方文档](http://www.pythondoc.com/flask-pymongo/)

 ```bash
$ sudo pip install Flask # 推荐使用virtualenv, 这里懒得用了
$ pip install Flask-PyMongo
```

## 测试

`cd`到git目录下

```bash
$ sudo service mongod start # 启动mongod (其实不用, 因为已经预加载了json)
$ python visualization/view.py
```

进入`127.0.0.1:5000`下预览吧
