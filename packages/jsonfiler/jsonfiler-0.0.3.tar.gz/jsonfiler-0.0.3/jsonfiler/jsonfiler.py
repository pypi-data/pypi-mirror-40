"""

"""

import json
import csv
import os
import logging

def loadlines(path):
    """
    加载一行一行的txt文件
    :param path: text文件路径
    :return: json数组，如果加载失败，则返回None
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.readlines()
            return content
    except Exception as e:
        print (e)
        return None



def load(path):
    """
    加载json文件
    :param path: json文件路径
    :return: json文件的内容，如果加载失败，则返回None
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return content
    except Exception as e:
        print (e)
        return None


def dump(json_content, path, **kwargs):
    """
    写入到json文件
    :param file_list: json文件内容
    :param path: 需要写入的文件路径
    :return: 如果写入成功，则返回True，否则返回False
    """
    dir_name = os.path.dirname(path)
    if dir_name == "." or dir_name == "":
        pass
    elif not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if path[-5:] != '.json':
        print ("必须导出成json文件.")
        return False
    #当json中有中文字符串时，需要在open时加上encoding=‘utf-8'，dump时加上ensure_ascii=False，
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            if 'indent' in kwargs:
                json.dump(json_content, f, indent=int(kwargs['indent']), ensure_ascii=False)
            else:
                json.dump(json_content, f, ensure_ascii=False)
            return True
    except Exception as e:
        print (e)
        return True

def dumplines(json_list, path, **kwargs):
    """
    写入到json文件
    :param file_list: 以列表存在的json文件
    :param path: 需要写入的文件路径
    :return: 如果写入成功，则返回True，否则返回False
    """
    dir_name = os.path.dirname(path)
    if dir_name == "." or dir_name == "":
        pass
    elif not os.path.exists(dir_name):
        os.makedirs(dir_name)

    if type(json_list) != type([]):
        print("导出内容必须是list.")
        return False
    
    #当json中有中文字符串时，需要在open时加上encoding=‘utf-8'，dump时加上ensure_ascii=False，
    try:
        with open(path, "w", encoding="utf-8", newline='') as f:
            for word in json_list:
                f.write(str(word)+"\n")
            return True
    except Exception as e:
        print (e)
        return True


def main():
    dumplines(["line1","line2"],"test.dat")

if __name__ == '__main__':
     main()

