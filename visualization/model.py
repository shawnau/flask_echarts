# -*- coding: utf-8 -*-
import json
import os


# load_json使用_byteify将所有unicode转换成string, 详见http://stackoverflow.com/questions/956867
def load_json(app, filename):
    filename = os.path.join(app.static_folder, filename)
    with open(filename, 'r') as json_data:
        return _byteify(json.load(json_data, object_hook=_byteify))


def dump_json(app, filename, outfile):
    filename = os.path.join(app.static_folder, filename)
    with open(filename, 'w') as json_data:
        json.dump(outfile, json_data)


def _byteify(data, ignore_dicts=False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


class MongoModel(object):
    """docstring for ClassName"""

    def __init__(self, app=None, db=None):
        super(MongoModel, self).__init__()
        self.db = db
        self.app = app
        self.city_list = load_json(app, 'city_list.json')
        self.map_coord = load_json(app, 'map_coord.json')

    def count_intern(self):
        interns_list = []
        for city in self.city_list:
            count = self.db.interns.find({'addr': city}).count()
            unit = {'name': city, 'value': count}
            interns_list.append(unit)
        # 生成列表之后进行倒序排序, 取前20
        sorted_list = sorted(interns_list, key=lambda k: k['value'], reverse=True)[:15]
        city_list = [x['name'] for x in sorted_list]
        count_list = [x['value'] for x in sorted_list]
        dump = {'city_list': city_list, 'count_list': count_list, 'city_count': sorted_list}
        dump_json(self.app, 'city_count.json', dump)
    
    # 根据标签名统计数据并排序, 取前20
    def count_tags(self, tag_name):
        tag_value_list = []
        tag_list = self.db.interns.distinct(tag_name)  # distinct用于统计种类
        for tag in tag_list:
            count = self.db.interns.find({tag_name: tag}).count()
            unit = {'name': tag, 'value': count}
            tag_value_list.append(unit)
        # 生成列表之后进行倒序排序, 取前20
        sorted_list = sorted(tag_value_list, key=lambda k: k['value'], reverse=True)[:15]
        dump_json(self.app, 'count_' + tag_name + '.json', sorted_list)
    
    # 根据标签名统计时间序列上的数量, 是个二维数组
    def count_tag_date(self):
        from datetime import datetime
        import pytz
        # 查找时间例子: current_interns = mongo.db.interns.find({'job_time': datetime.datetime(2017, 3, 1)}).count()
        # load得到的还要是unicode
        tags = load_json(self.app, 'count_tag.json')
        name_list = [x['name'] for x in tags]
        tag_name_list = [x for x in name_list]
        time_list = sorted(self.db.interns.distinct("job_time"))

        # FOR BUG ISSUE ONLY: 年份时间有错位, 所有18年的日期其实是17年的 #
        utc = pytz.UTC
        start = datetime(2017, 1, 1).replace(tzinfo=utc)
        now = datetime.now().replace(tzinfo=utc)
        time_list = [x for x in time_list if start <= x.replace(tzinfo=utc) <= now]
        
        # 转换为string方便表示
        str_time_list = [x.strftime('%Y/%m/%d') for x in time_list]
    
        # 按tag名添加横坐标为日期的标签count
        count_list = []
        for tag in tag_name_list:
            count_list.append([self.db.interns.find({'job_time': x, 'tag': tag}).count() for x in time_list])
        dump = {'tag_time_list': count_list, 'time_list': str_time_list}
        dump_json(self.app, 'time_tag.json', dump)
