# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_pymongo import PyMongo
import json
import model

import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

import logging
logging.basicConfig()

# 这玩意至今不知道怎么解决
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config['MONGO_DBNAME'] = 'shixiseng_interns'
mongo = PyMongo(app, config_prefix='MONGO')

# 初始化json文件的操作每小时更新一次, 但第一次必须手动进行
def init_json():
    with app.app_context():    
        m = model.MongoModel(app, mongo.db)
        m.count_intern()
        m.count_tags('tag')
        m.count_tags('company_name')
        m.count_tag_date()

# 定时启动init_json()
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=init_json,
    trigger=IntervalTrigger(hours=1),
    id='dump_json',
    name='generate json files',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def home_page():
    # 从json里读取数据
    coord_map = model.load_json(app, 'map_coord.json')
    city_list = model.load_json(app, 'city_count.json')['city_list']
    count_list = model.load_json(app, 'city_count.json')['count_list']
    city_count = model.load_json(app, 'city_count.json')['city_count']
    tags = model.load_json(app, 'count_tag.json')
    company = model.load_json(app, 'count_company_name.json')
    tag_names = [x['name'] for x in tags]
    time_list = model.load_json(app, 'time_tag.json')['time_list']
    time_tag = model.load_json(app, 'time_tag.json')['tag_time_list']

    # 含有中文的必须使用ensure_ascii=False来dump
    data = {
        'coord_map': json.dumps(coord_map, ensure_ascii=False),
        'city_list': json.dumps(city_list, ensure_ascii=False),
        'count_list': count_list,
        'city_count': json.dumps(city_count, ensure_ascii=False),
        'tags': json.dumps(tags, ensure_ascii=False),
        'company': json.dumps(company, ensure_ascii=False),
        'tag_names_list': tag_names,
        'tag_names': json.dumps(tag_names, ensure_ascii=False),
        'time_list': time_list,  # 如果需要在jinja2里循环, 就不能dump成json
        'time_tag': time_tag
    }

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
