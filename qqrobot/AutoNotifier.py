import requests
import re
import Utils as utils
import time


class AutoNotifier:

    def __init__(self, mid):
        self._attr = {
            "mid": mid
        }

    def get_room_info(self):
        api = "https://api.bilibili.com/x/space/acc/info"
        url = utils.url_arg_add(url=api, attr=self._attr)
        return utils.get_api_dict(url=url)

    def is_live_on(self):
        dic = self.get_room_info()
        referer = ("data", "live_room", "liveStatus")
        result = utils.extract_info(dic=dic, referers=referer)

        if result == 1:
            return True
        return False

    def get_room_descrip(self):
        dic = self.get_room_info()
        title_refer = ("data", "live_room", "title")
        name_refer = ("data", "name")
        url_refer = ("data", "live_room", "url")
        attr = {
            "直播标题": utils.extract_info(dic=dic, referers=title_refer),
            "链接": utils.extract_info(dic=dic, referers=url_refer)
        }
        prefix = "来活了，来活了\n" + utils.extract_info(dic=dic, referers=name_refer) + "居然开播了!\n"

        return utils.generate_descrip(prefix=prefix, attr=attr)




