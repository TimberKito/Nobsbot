import requests
import time
import re
import random


def group_send(gid, text, url=None):
    time.sleep(3)
    requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, text))
    if url:
        print("now send the pic")
        requests.get(url='http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, r'[CQ:image,' r'file=' + url + r']'))


def get_feature(url, tags, selectors, trans, gid):
    """
    :param: url
    :param: tags
    :param: selectors
    :return: a string consists of the features specifies and a url
    """
    print(url)
    menu = requests.get(url)
    desc = dict()
    descrip = ""
    url = None
    if menu.json()['data']:
        wid = None
        hei = None
        for select in selectors:
            res = menu.json()['data'][0][select]
            desc[select] = res
            if select == "uploadDate":
                res = int(res/1000)
                res = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(res))
            if select not in ['width', 'height']:
                descrip += str(trans[select]) + ":" + str(res)
            else:
                if select == 'width':
                    wid = int(res)
                if select == 'height':
                    hei = int(res)
                if wid and hei:
                    size = wid*hei*3/1024/1024
                    size = round(size, 2)
                    descrip += str(trans['size']) + ":" + str(size) + "mb"

            if select in ['author', 'title', 'uploadDate', 'size']:
                descrip += "\n"

        url = menu.json()['data'][0]['urls']['original']
    else:
        group_send(gid=gid, text="没活了，别骂了别骂了")

    return url, descrip


def get_tags(txt, url):
    result = re.search(r"(?<=来份|来点|来张)(.*?)(?=色图)", txt)
    if result:
        txt = result.group()
    else:
        txt = ''
    tags = txt.split(',')
    url += '?'
    for ind in range(len(tags)):
        if ind != len(tags)-1:
            url += 'tag=' + tags[ind] + '&'
        else:
            url += 'tag=' + tags[ind]
    return tags, url


def try_get_url(data):
    gid, txt, url, selectors, trans = data
    tags, url = get_tags(txt, url)
    print("现在的url:", url)
    setu_url, text = get_feature(url=url, tags=tags, selectors=selectors, trans=trans, gid=gid)

    result = re.search(r"(?<=/)[0-9]+(?=_)", setu_url)
    pid = result.group()

    return (setu_url, text), pid


def start(data, duplicated, retry):

    if retry <= 0:
        return None, None, None
    print(duplicated)
    print(data)

    result, pid = try_get_url(data)

    if pid in duplicated:
        return start(data, duplicated=duplicated, retry=retry-1)

    return *result, pid


class EroPic:
    """
    This Class is for grab and send the Ero Pictures
    """
    def __init__(self, txt, duplicated):
        self.url = 'https://api.lolicon.app/setu/v2'
        self.txt = txt
        self.selectors = ['pid', 'author', 'title', 'uploadDate', 'width', 'height']
        self.trans = {
            'author': '作者',
            'title': '标题',
            'pid': 'pid',
            'uploadDate': '上传日期',
            'size': '尺寸'
        }
        self.duplicated = duplicated

    def master_start(self, gid):
        retry = 4

        data = (gid, self.txt, self.url, self.selectors, self.trans)
        setu_url, text, pid = start(data, duplicated=self.duplicated, retry=retry)

        if setu_url is None:
            print("没活了，别骂了别骂了")
            text = "没活了，别骂了别骂了"
            group_send(gid=gid, text=text)
        else:
            print("我还有活，咬打火机了")
            self.duplicated.append(pid)
            group_send(gid=gid, text=text, url=setu_url)

    def private_send(self, id):
        pass

    def detector(self):
        """
        This detector is to match if the pattern got from others whether right or not.
        :return: Bool, if the pattern command matches
        """
        restr = r"来.*色图"
        if re.search(restr, self.txt):
            return True
        return False










