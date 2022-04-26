import random
import time

from flask import Flask, request
import EroPic as EP
import AutoReplier as AR
from collections import deque
import threading
import AutoNotifier as AN
import Utils as utils
import What2Eat as WE


app = Flask("main")
duplicated = deque(maxlen=100)


def eropic_sender(mes, gid, *args):

    ep = EP.EroPic(mes, duplicated)
    if ep.detector():
        ep.master_start(gid)


def autoreplier_sender(mes, gid, *args):
    ar = AR.AutoReplier(mes)
    text = ar.get_answer()
    utils.group_send(gid, text=text)


def clear_deque(mes, *args):
    if mes == "清空色图缓存":
        duplicated.clear()


def live_notifier(mid, gid="761510283", *args):
    # 记住以后要更改gid这里的储存格式.目前只用在一个群
    an = AN.AutoNotifier(mid)
    while True:
        time.sleep(random.random() * 10 + 60)
        print("开始判断是否开播")
        if an.is_live_on():
            print("准备发送消息")
            time.sleep(120)
            utils.group_send(gid=gid, text=an.get_room_descrip())
            while True:
                time.sleep(random.random() * 10 + 60)
                if not an.is_live_on():
                    break


def what_2_eat(mes, gid, *args):
    if mes[:2] == "外卖":
        filename = "takeaway"
    elif mes[:3] == "商业街":
        filename = "shopstreet"
    else:
        return -1
    we = WE.What2Eat(gid=gid, mes=mes, filename=filename)
    we.mode_select()


@app.route('/', methods=["POST"])
def post_data():

    if request.get_json().get('message_type') == 'group':
        mes = request.get_json().get('message')
        gid = request.get_json().get('group_id')
        ths = ["eropic_sender", "autoreplier_sender", "clear_deque", "what_2_eat"]
        for i in range(len(ths)):
            th = threading.Thread(target=eval(ths[i]), args=(mes, gid), name="th"+str(i))
            th.start()

    return 'OK'


if __name__ == '__main__':

    mids = ["128912828", "316381099"]
    gid = "761510283"
    for i in range(len(mids)):
        th_live = threading.Thread(target=live_notifier, args=(mids[i], gid), name="Thread"+str(i))
        th_live.start()

    host = '127.0.0.1'
    port = 5701
    th_app = threading.Thread(target=app.run, args=(host, port))
    th_app.start()

