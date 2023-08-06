# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2017/9/29 0029
import os
import json
import xlrd
import chardet
from demo_xml import demo_xml
try:
    import csv
except:
    pass
__author__ = 'huohuo'
if __name__ == "__main__":
    pass


class File:

    def __init__(self, base_dir=''):
        self.__description__ = '文件相关， 包括读文件，写文件， 下载文件'
        self.base_dir = base_dir

    def read(self, file_name, sheet_name='', read_type='r', dict_name='', to_json=True, **kwargs):
        file_type = file_name.split('.')[-1]
        url = os.path.join(self.base_dir, dict_name, file_name)
        if os.path.exists(url) is False:
            print 'File not exists, %s. Please check.' % url
            return None
        if file_type in ['xlsx', 'xls']:
            data = xlrd.open_workbook(url)
            return data.sheet_by_name(sheet_name)

        f = open(url, read_type)
        text = f.read()
        f.close()
        if file_type in ['csv', 'tsv'] or 'sep' in kwargs:
            encoding = chardet.detect(text)['encoding']
            sep = ',' if file_type == 'csv' else '\t'
            if 'sep' in kwargs:
                sep = kwargs['sep']
            delimiter = {'delimiter': sep}
            f = open(url, read_type)
            csv.register_dialect('my_dialect', **delimiter)
            cons = csv.reader(f, 'my_dialect')
            items = []
            keys = next(cons)
            for c in cons:
                if to_json:
                    item = {}
                    for i in range(len(keys)):
                        item[keys[i]] = c[i].decode(encoding).encode('utf-8')
                    items.append(item)
                else:
                    items.append([x.decode(encoding).encode('utf-8') for x in c])
            csv.unregister_dialect('my_dialect')
            return items
        if file_type == 'json':
            return json.loads(text)
        return text

    def read_message(self, file_name, file_type='json', sheet_name='', read_type='r', developer='huohuo', message='success'):
        error_message = u'【开发者】：%s\n' % developer
        error_message += u'【文件类型】：%s\n' % file_type
        if file_type in ['xlsx', 'xls']:
            error_message += u'【sheet_name】：%s\n' % sheet_name
        error_message += u'【消息】：%s\n' % message
        error_message += u'【文件名】：\n%s\n' % file_name

    def write(self, file_name, data):
        file_type = file_name.split('.')[-1]
        url = os.path.join(self.base_dir, file_name)
        f = open(url, "w")
        if file_type == 'json':
            try:
                f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
            except:
                f.write(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=True))
        else:
            f.write(data)
        f.close()
        return 5

    def download(self, pkg_parts, file_name):
        temp_data = demo_xml.replace('<pkg:part id="pkg_parts"></pkg:part>', pkg_parts)
        temp_data = temp_data.replace('\n', '')
        return self.write(file_name, temp_data)

    def get_file_list(self, sample_type, pre=''):
        file_list = []
        folder_list = []
        full_path = os.path.join(self.base_dir, pre)
        for file_name in os.listdir(full_path):
            path_file = os.path.join(full_path, file_name)
            file_dict = {
                'text': file_name,
                'url': path_file,
                'dir_path': os.path.dirname(path_file),
                'full_path': file_name,
                'relative_path': os.path.relpath(path_file, self.base_dir)
            }
            if os.path.isdir(path_file):
                file_dict["type"] = "文件夹"
                file_dict["size"] = None
                folder_list.append(file_dict)
            elif os.path.isfile(path_file):
                file_dict["type"] = self.get_file_type(sample_type, file_name)
                try:
                    file_size = os.path.getsize(path_file)
                    file_dict["size"] = self.get_file_size(file_size)
                except Exception, e:
                    file_dict["size"] = ''
                    pass
                    # print file_path
                    # print e.args
                if file_dict["type"] != "":
                    file_list.append(file_dict)
        folder_list.sort()
        file_list.sort()
        return {'data':{'folder': folder_list, 'file': file_list}}

    def get_file_size(self, size):
        if size > 1024 ** 3:
            return '%.02fGB' % (float(size) / 1024 ** 3)
        elif size > 1024 ** 2:
            return '%.02fMB' % (float(size) / 1024 ** 2)
        elif size > 1024:
            return '%0.2fKB' % (float(size) / 1024)
        else:
            return '%0.2fB' % (float(size))

    def get_file_item(self, basi_dir, dirpath, relative_path, is_relative):
        item = {}
        full_path = os.path.join(dirpath, relative_path)
        file_url = full_path
        file_text = relative_path
        if is_relative:
            file_url = full_path.replace(basi_dir, "")
            file_text = relative_path.replace(full_path, '')
        file_array = dirpath.replace(basi_dir, "").split(os.sep)
        item['full_path'] = full_path
        item["url"] = file_url.strip()
        item["text"] = file_text.strip()
        item["len"] = len(file_array)
        item["array"] = file_array
        return item

    def get_file_type(self, sample_type, file_name):
        postfix = ['.%s' % sample_type]
        file_type = sample_type
        if sample_type == 'vcf':
            postfix.append('.%s.gz' % sample_type)
        elif sample_type == "fastq":
            if file_name.endswith('.bed'):
                file_type = 'bed'
                postfix = ['.bed']
            else:
                postfix.extend(['.fq', '.fq.gz', '.fastq.gz'])
        for p in postfix:
            if file_name.endswith(p):
                return file_type
        return ''

    def is_fastq(self, file_name):
        postfix = ['.fastq', '.fq', '.fastq.gz', '.fq.gz']
        for p in postfix:
            if file_name.endswith(p):
                return True
        return False

    # 对文件进行排序 返回值大于零，则交换x、y,否则不交换
    def compare_file(self, x, y):
        '''
        原则：
        1. 文件夹在前
        2. fastq 在前 bed 在后
        3. 子文件夹嵌套层数越多越靠前
        '''
        if x['type'] == '文件夹' and y['type'] != '文件夹':
            return -1
        if y['type'] == '文件夹' and x['type'] != '文件夹':
            return 1
        if x['type'] == 'bed' and y['type'] == 'fastq':
            if x['text'][:3] == y['text'][:3]:
                return 1
        if x['len'] != y['len']:
            return y['len'] - x['len']
        return cmp(x['url'], y['url'])
