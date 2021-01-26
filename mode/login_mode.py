from db.user_info_util import user_util
import json


# 登录逻辑
def login(self, data_dict):
    """
    :param self: 连接对象
    :param data_dict: 客户端的请求消息
    """
    username = data_dict["username"].strip()
    password = data_dict["password"].strip()
    # 服务器端的响应消息
    data = {}
    # 账号密码不能为空
    if username and password:
        code, msg, nickname = login_check(username, password)
    elif not username:
        code = "003"
        msg = "登录用户名不能为空"
    elif not password:
        code = "004"
        msg = "登录密码不能为空"
    # 登录成功，将连接对象以及昵称加到users中，便于后续遍历发送消息
    if code == "000":
        # 在全局变量users中新增用户信息
        self.users[self] = nickname
        data["nickname"] = nickname
    data["type"] = "login"
    data["code"] = code
    data["msg"] = msg
    data = json.dumps(data)
    self.sendLine(data.encode("utf-8"))


# 登录校验逻辑
def login_check(username, password):
    # 通过用户名到数据库获取用户信息
    user_info = user_util.user_check(username)
    # 未查到该用户信息，代表未注册
    if len(user_info) == 0:
        data = ("001", "账号【%s】未注册，请先进行注册！" % username, None)
    # 密码错误
    elif password != user_info[0][1]:
        data = ("002", "密码有误，请重新输入！", None)
    # 正常登录
    else:
        # 获取昵称
        nickname = user_info[0][2]
        data = ("000", "账号【%s】登录成功！" % username, nickname)
    return data