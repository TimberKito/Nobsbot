import Utils as utils
import random
import json
import os
import re


def generate_dict(path):
    with open(path, 'r') as f:
        return json.load(f)


class What2Eat:

    def __init__(self, mes, gid, filename):
        self._path = "./" + filename + "/" + str(gid) + ".json"
        file = "./" + filename
        utils.file_overwrite(self._path, filename, file, gid)
        self._mes = mes
        self._data = generate_dict(self._path)  # outer is a list, inner is a dict
        self._gid = gid
        self._filename = filename

    def random_pick(self):
        print(self._data)
        if self._data:
            choice = random.choice(self._data)
            text = utils.generate_descrip(prefix="恭喜你抽中了:\n", attr=choice, suffix="不满意还可以再来一次哦")
            utils.group_send(gid=self._gid, text=text)
        else:
            text = "目前目录里还没有任何东西捏..!"
            utils.group_send(gid=self._gid, text=text)

    def append_choice(self, choice):
        pattern = re.search(r'(?<=' + choice + ')(.*)', self._mes)
        pattern = pattern.group(0)
        if pattern == "":
            text = "添加的东西不可以是空的哦!"
            utils.group_send(self._gid, text=text)
            return None

        dic = {"名称": pattern}
        self._data.append(dic)  # in the form of "添加选择:xxxx"
        utils.write_json(path=self._path, data=self._data)

        text = "添加成功!"
        utils.group_send(self._gid, text=text)

    def get_all(self):
        text = ""
        for item in self._data:
            text += utils.generate_descrip(prefix="", attr=item, suffix="")
        utils.group_send(self._gid, text=text)

    def delete(self, choice):
        pattern = re.search(r'(?<=' + choice + ')(.*)', self._mes)
        pattern = pattern.group(0)

        for index in range(len(self._data)):
            if self._data[index]['名称'] == pattern:  # 删除选择xxx
                self._data.pop(index)
                utils.write_json(path=self._path, data=self._data)
                return None
        text = "未找到需要删除的对象!"
        utils.group_send(self._gid, text=text)

    def mode_select(self):

        trans = {
            "takeaway": "外卖",
            "shopstreet": "商业街"
        }

        choice = re.search(r'(?<=' + trans[self._filename] + ')(.*)', self._mes)
        choice = choice.group(0)

        if choice.find("添加选择") != -1:
            self.append_choice("添加选择")
        elif choice.find("吃啥") != -1:
            self.random_pick()
        elif choice.find("删除选择") != -1:
            self.delete("删除选择")
        elif choice.find("查看全部选择") != -1:
            self.get_all()

        return None

