from db.user_info_util import user_util
import json


# 注册逻辑
def register(self, data_dict):
    """
    :param self: 连接对象
    :param data_dict: 客户端的请求消息
    """
    username = data_dict["username"].strip()
    password = data_dict["password"].strip()
    nickname = data_dict["nickname"].strip()
    # 服务器端的响应消息
    data = {}
    # 三者均不为空才能走注册校验
    if username and password and nickname:
        code, msg = register_check(username, password, nickname)
    elif not username:
        code = "002"
        msg = "注册账号不能为空"
    elif not password:
        code = "003"
        msg = "注册密码不能为空"
    elif not nickname:
        code = "004"
        msg = "注册昵称不能为空"
    if code == "000":
        self.users[self] = nickname
        data["nickname"] = nickname

    data["type"] = "register"
    data["code"] = code
    data["msg"] = msg
    data = json.dumps(data)
    self.sendLine(data.encode("utf-8"))


# 注册校验
def register_check(username, password, nickname):
    user_info = user_util.user_check(username)
    if len(user_info) > 0:
        data = ("001", "账号【%s】已被注册过" % user_info)
    else:
        user_util.user_insert(username, password, nickname)
        data = ("000", "账号【%s】注册成功，点击'确定'进入聊天页面" % username)
    return data
