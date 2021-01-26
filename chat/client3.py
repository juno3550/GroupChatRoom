import tkinter
from tkinter import messagebox
import json
import time
import threading
import select
from socket import *
import traceback
from chat import client_draw


class Client:

    # 配置连接
    def connect(self):
        # 创建socket
        self.s = socket(AF_INET, SOCK_STREAM)
        # 服务器端和客户端均在同个机器上运行
        remote_host = gethostname()
        # 设置端口号
        port = 1200
        # 发起连接
        self.s.connect((remote_host, port))
        print("从%s成功连接到%s" % (self.s.getsockname(), self.s.getpeername()))
        return self.s

    # 监听（接收）消息
    def receive(self, s):
        # 需要监控的对象列表
        self.my = [s]
        while 1:
            print("监听中...")

            # 实参:
            # 第1个实参 r_list：可读的对象，监听两种事件 -- 新客户端连接与客户端发送消息
            # 第2个实参：可写的对象（本例不用)
            # 第3个实参：出现异常的对象（本例不用）
            # 这三个参数内容都是被操作系统监控的，即select.select()会执行系统内核代码
            # 1）当有事件发生时，立马往下执行代码；否则阻塞监控10秒
            # 2）若监控10秒了仍无事件发生，才往下执行
            rl, wl, error = select.select(self.my, [], [], 10)
            # 返回值：
            # rl：监听某个文件描述符是否发生了读的事件（1. 有client进行连接；2. client给server发了数据）
            #       rl列表一开始为空，只有当s发生事件了（如首先收到连接请求），才会将s加到rl中
            # wl：监听某个文件描述符是否发生了写的事件（如server给client发了数据）
            # error：监听某个文件描述符是否发生了异常事件
            # 如果发生事件的对象是客户端连接对象，则代表收到服务器端数据
            if s in rl:
                try:
                    data = s.recv(1024).decode("utf-8")
                    data_dict = json.loads(data)
                    # 根据服务器端返回的type值，执行不同逻辑
                    type = data_dict["type"]
                    # 登录逻辑
                    if type == "login":
                        # 登录成功，跳转聊天页面
                        if "000" == data_dict["code"]:
                            nickname = data_dict["nickname"]
                            self.chat_interface(nickname)
                        # 登录失败，获取失败信息
                        else:
                            messagebox.showinfo(title="登录提示", message=data_dict["msg"])
                    # 注册逻辑
                    elif type == "register":
                        # 注册成功，跳转聊天页面
                        if "000" == data_dict["code"]:
                            nickname = data_dict["nickname"]
                            messagebox.showinfo(title="进入聊天室", message=data_dict["msg"])
                            self.chat_interface(nickname)
                        # 注册失败
                        else:
                            messagebox.showinfo(title="注册提示", message=data_dict["msg"])
                    # 聊天逻辑
                    elif type == "chat":
                        message = data_dict["message"]
                        nickname = data_dict["nickname"]
                        isMy = data_dict["isMy"]
                        chat_time = " " + nickname + "\t" + time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n"
                        # 聊天页面，显示发送人及发送时间
                        self.txtMsgList.insert(tkinter.END, chat_time, "DimGray")
                        # 如果是自己发的消息，字体使用'DarkTurquoise'
                        if "yes" == isMy:
                            self.txtMsgList.insert(tkinter.END, " " + message + "\n\n", 'DarkTurquoise')
                        # 如果是别人发的消息，字体使用'Black'
                        else:
                            self.txtMsgList.insert(tkinter.END, " " + message + "\n\n", 'Black')
                        # 插入消息时，自动滚动到底部
                        self.txtMsgList.see(tkinter.END)
                except (ConnectionAbortedError, ConnectionResetError):
                    # 将连接对象从监听列表去掉
                    self.my.remove(s)
                    print("客户端发生连接异常，与服务器端断开连接")
                    traceback.print_exc()
                    s.close()
                except Exception as e:
                    print("客户端发生了其它异常: ")
                    traceback.print_exc()
                    s.close()

    # 进入注册页面
    def register_interface(self):
        client_draw.draw_register(self)

    # 进入聊天页面
    def chat_interface(self, nickname):
        client_draw.draw_chat(self, nickname)

    # 返回登录页面
    def return_login_interface(self):
        # 将不需要的控件先销毁
        self.label_nickname.destroy()
        self.input_nickname.destroy()
        self.label_password.destroy()
        self.input_password.destroy()
        client_draw.draw_login(self)

    # 获取输入框内容，进行注册验证
    def verify_register(self):
        username = self.input_account.get()
        password = self.input_password.get()
        nickname = self.input_nickname.get()
        try:
            register_data = {}
            register_data["type"] = "register"
            register_data["username"] = username
            register_data["password"] = password
            register_data["nickname"] = nickname
            # 将dict类型转为json字符串，便于网络传输
            data = json.dumps(register_data)
            self.s.send(data.encode("utf-8"))
        except:
            traceback.print_exc()

    # 获取输入框内容，进行登录校验
    def verify_login(self):
        account = self.input_account.get()
        password = self.input_password.get()
        try:
            login_data = {}
            login_data["type"] = "login"
            login_data["username"] = account
            login_data["password"] = password
            data = json.dumps(login_data)
            self.s.send(data.encode('utf-8'))
        except:
            traceback.print_exc()

    # 获取输入框内容，发送消息
    def send_msg(self):
        message = self.txtMsg.get('0.0', tkinter.END).strip()
        if not message:
            messagebox.showinfo(title='发送提示', message="发送内容不能为空，请重新输入")
            return
        self.txtMsg.delete('0.0', tkinter.END)
        try:
          chat_data = {}
          chat_data["type"] = "chat"
          chat_data["message"] = message
          data = json.dumps(chat_data)
          self.s.send(data.encode('utf-8'))
        except:
          traceback.print_exc()

    # 发送消息事件
    def send_msg_event(self, event):
        # 如果捕捉到键盘的回车按键，触发消息发送
        if event.keysym == 'Return':
            self.send_msg()

    # 聊天页面，点击右上角退出时执行
    def on_closing(self):
        if messagebox.askokcancel("退出提示", "是否离开聊天室？"):
            self.window.destroy()


def main():
    chatRoom = Client()
    client = chatRoom.connect()
    t = threading.Thread(target=chatRoom.receive, args=(client,))  # 创建一个线程，监听消息
    t.start()
    # 创建主窗口,用于容纳其它组件
    chatRoom.window = tkinter.Tk()
    # 登录界面控件创建、布局
    client_draw.draw_login(chatRoom)
    # 进入事件（消息）循环
    tkinter.mainloop()

if __name__ == "__main__":
    main()