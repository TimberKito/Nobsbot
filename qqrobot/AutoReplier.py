import requests
import re
import random
import time
import Utils as utils


def group_send(gid, ans):
    time.sleep(3)
    url = 'http://127.0.0.1:5700/send_group_msg?group_id={0}&message={1}'.format(gid, ans)
    requests.get(url=url)


class AutoReplier:

    def __init__(self, mes):
        self.mes = mes
        self.start_patterns = [
            "我觉得",
            "确实",
            "有道理",
            "算是",
            "行"
        ]
        self.end_patterns = [
            "？",
            "吗",
            "行不"
        ]
        self.middle_patterns = [
            "该",
            "能不能",
            "可不可以"
        ]
        self.answers = [
            "我也觉得",
            "确实",
            "的确",
            "有道理",
            "说得好"
        ]

        self.ans = random.choice(self.answers)

    def start(self, gid):
        group_send(gid, self.ans)

    def get_repeat(self):
        restr = r'^{0}|{1}$|{2}'.format('|^'.join(self.start_patterns),
                                                 '$|'.join(self.end_patterns),
                                                 '|'.join(self.middle_patterns))

        if re.search(restr, self.mes):
            return self.ans
        return None

    def get_answer(self):
        restr = r'(.+?)(吗？$|？$|吗$|\?$|吗\?$)'

        reobj = re.match(restr, self.mes)

        if reobj:
            return reobj.group(1)
        return None






