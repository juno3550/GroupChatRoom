import json


# 聊天逻辑
def chat(self, data_dict):
    """
    :param self: 连接对象
    :param data_dict: 客户端的请求消息
    """
    message = data_dict["message"].strip()
    # 遍历所有的连接对象，群发消息
    for user in self.users.keys():
        data = {}
        data["type"] = "chat"
        # 获取当前发送消息客户端的昵称
        nickname = self.users[self]
        data["nickname"] = nickname
        # "isMy"键默认为no
        data["isMy"] = "no"
        # 如果遍历的对象与发消息客户端是同一个，则将isMy字段设为yes, 便于前端用来判断展示不同的字体样式
        if user == self:
            data["isMy"] = "yes"
        data["message"] = message
        data = json.dumps(data)
        user.sendLine(data.encode("utf-8"))