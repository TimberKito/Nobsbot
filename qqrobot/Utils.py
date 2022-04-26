import requests
import time
import json
import os


def url_arg_add(url, attr):

    """
    :param url: original url without any attributes
    :param attr: the attributes wanted to be added after the original url
    :return: a url with parameters
    """

    url_edited = url
    url_edited += "?"

    for key, value in attr.items():
        url_edited += str(key) + "=" + str(value) + "&"

    url_edited = url_edited[:-1]
    print(url_edited)
    return url_edited


def get_api_dict(url):

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",

    }

    js = requests.get(url, headers=headers)

    return js.json()


def extract_info(dic, referers):
    """
    :param dic: dictionary provided
    :param referers: a tuple, consists of a path to what interested
    :return:
    """
    for referer in referers:
        dic = dic[referer]
    return dic


def group_send(gid, text=None, url=None):
    time.sleep(3)
    if text:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, text))
    if url:
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:image,' r'file=' + url + r']'))


def generate_descrip(prefix="", attr=None, suffix=""):
    descrip = prefix
    for key, value in attr.items():
        descrip += str(key) + ":" + str(value) + "\n"
    descrip += suffix
    return descrip


def write_json(path, data):
    with open(path, 'w') as f:
        return json.dump(data, f)


def file_overwrite(path, filename, file, gid):
    if filename not in os.listdir(path="."):
        os.mkdir(path="./" + filename)
    if str(gid) + ".json" not in os.listdir(path=file):
        write_json(path=path, data=[])