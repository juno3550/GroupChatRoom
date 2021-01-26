from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver  # 事件处理器
from twisted.internet import reactor
import json
from mode import chat_mode, login_mode, register_mode


# 每一个客户端连接都会对应一个不同的Chat对象
class Chat(LineReceiver):

    def __init__(self, users):
        # 存储所有连接用户信息的字典
        self.users = users

    # 断开连接时候自动触发，从users字典去掉连接对象
    def connectionLost(self, reason):
        if self in self.users.keys():
            # print("%s断开连接" %self.users[self])
            del self.users[self]

    # 对客户端的请求内容做处理，只要收到客户端消息，自动触发此方法
    def dataReceived(self, data):
        # 将字节数据解码成字符串
        data = data.decode('utf-8')
        data_dict = json.loads(data)
        # 根据type字段的值，进入对应的逻辑
        # 登录逻辑
        if data_dict["type"] == "login":
            login_mode.login(self, data_dict)
        # 注册逻辑
        elif data_dict["type"] == "register":
            register_mode.register(self, data_dict)
        # 聊天逻辑
        elif data_dict["type"] == "chat":
            chat_mode.chat(self, data_dict)


# 处理业务的工厂类，只会实例化一次
class ChatFactory(Factory):

    def __init__(self):
        # 有多个连接的时候，会有多个chat对象
        # self.users 在内存地址中，只有一份，所有连接对象都只使用同一个实例变量 self.users（等价于一个全局变量）
        self.users = {}
        # key: 连接对象本身；value：登录成功的用户昵称

    # 一个客户端连接会实例化一个新的Chat对象
    def buildProtocol(self, addr):
        print(type(addr), addr)
        # 返回一个处理具体业务请求的对象，参数传递了字典（存有所有连接对象）
        return Chat(self.users)


if __name__ == '__main__':
    # 设定监听端口和对象
    # 使用Tcp协议，实例化ChatFactory
    reactor.listenTCP(1200, ChatFactory())

    print ("开始进入监听状态...")
    reactor.run()  # 开始监听