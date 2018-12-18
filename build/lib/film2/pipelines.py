# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#

import json
import os
import requests


class JsonPipeline(object):
    def __init__(self):
        self.file = open('meinv.txt', 'w')

    def process_item(self, item, spider):
        v = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(v)
        self.file.write('\n')
        self.file.flush()
        # print('-----')
        return item


class FilePipeline(object):

    def process_item(self, item, spider):
        response = requests.get(item['url'], stream=True)
        dir_name=str(item['name']).strip().split("(")[0]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        file_name = '%s.jpg' % (item['name'])
        with open(os.path.join(dir_name, file_name), mode='wb') as f:
            f.write(response.content)
        # print('ok')
        return item


