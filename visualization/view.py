# -*- coding: utf-8 -*-
from flask import Flask, render_template
import json
import os

import logging
logging.basicConfig()

app = Flask(__name__, instance_relative_config=True)


def load_json(app, filename):
    filename = os.path.join(app.static_folder, filename)
    with open(filename, 'r') as json_data:
        return json.load(json_data)

@app.route('/')
def home_page():
    tag_names = [x['name'] for x in load_json(app, 'count_tag.json')]

    data = {
        'coord_map': load_json(app, 'map_coord.json'),
        'city_list': load_json(app, 'city_count.json')['city_list'],
        'count_list': load_json(app, 'city_count.json')['count_list'],
        'city_count': load_json(app, 'city_count.json')['city_count'],
        'tags': load_json(app, 'count_tag.json'),
        'company': load_json(app, 'count_company_name.json'),
        'tag_names_list': tag_names,
        'tag_names': json.dumps(tag_names, ensure_ascii=False),
        'time_list': load_json(app, 'time_tag.json')['time_list'],  # 如果需要在jinja2里循环, 就不能dump成json
        'time_tag': load_json(app, 'time_tag.json')['tag_time_list']
    }

    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
