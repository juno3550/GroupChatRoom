import tkinter


# 登录页面
def draw_login(self):
    # 设置主窗口标题
    self.window.title("聊天室登录界面")
    # 设置主窗口大小
    self.window.geometry("450x300")
    # 创建画布
    self.canvas = tkinter.Canvas(self.window, height=200, width=500)
    # 创建一个`Label`名为`账 号: `
    self.label_account = tkinter.Label(self.window, text='账 号')
    # 创建一个`Label`名为`密 码: `
    self.label_password = tkinter.Label(self.window, text='密 码')
    # 创建一个账号输入框,并设置尺寸
    self.input_account = tkinter.Entry(self.window, width=30)
    # 创建一个密码输入框,并设置尺寸
    self.input_password = tkinter.Entry(self.window, show='*', width=30)
    # 登录按钮
    self.login_button = tkinter.Button(self.window, command=self.verify_login, text="登 录", width=10)
    # 注册按钮
    self.register_button = tkinter.Button(self.window, command=self.register_interface, text="注 册", width=10)

    # 登录页面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=150)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=150)
    self.login_button.place(x=120, y=235)
    self.register_button.place(x=250, y=235)


# 注册界面
def draw_register(self):
    # 登录按钮销毁
    self.login_button.destroy()
    # 注册按钮销毁
    self.register_button.destroy()
    self.window.title("聊天室注册界面")
    self.window.geometry("450x300")
    # 创建画布
    self.canvas = tkinter.Canvas(self.window, height=200, width=500)
    # 创建一个"Label",名为："昵 称"
    self.label_nickname = tkinter.Label(self.window, text='昵 称')
    # 创建一个昵称输入框,并设置尺寸
    self.input_nickname = tkinter.Entry(self.window, width=30)
    # 创建注册按钮
    self.register_submit_button = tkinter.Button(self.window, command=self.verify_register, text="提交注册", width=10)
    # 创建注册按钮
    self.return_login_button = tkinter.Button(self.window, command=self.return_login_interface, text="返回登录",width=10)

    # 注册界面各个控件进行布局
    self.label_account.place(x=90, y=70)
    self.label_password.place(x=90, y=130)
    self.input_account.place(x=135, y=70)
    self.input_password.place(x=135, y=130)
    self.label_nickname.place(x=90, y=190)
    self.input_nickname.place(x=135, y=190)
    self.register_submit_button.place(x=120, y=235)
    self.return_login_button.place(x=250, y=235)


# 聊天室界面
def draw_chat(self, nickname):
    self.window.title("【%s】的聊天室界面" % nickname)
    self.window.geometry("520x560")
    # 创建frame容器
    # 放置聊天记录
    self.frmLT = tkinter.Frame(width=500, height=320)
    # 放置发送内容输入框
    self.frmLC = tkinter.Frame(width=500, height=150)
    # 放置发送按钮
    self.frmLB = tkinter.Frame(width=500, height=30)

    self.txtMsgList = tkinter.Text(self.frmLT)
    # 设置消息时间字体样式
    self.txtMsgList.tag_config('DimGray', foreground='#696969', font=("Times", "11"))
    # 设置自己的消息字体样式
    self.txtMsgList.tag_config('DarkTurquoise', foreground='#00CED1', font=("Message", "13"), spacing2=5)
    # 设置其它人的消息字体样式
    self.txtMsgList.tag_config('Black', foreground='#000000', font=("Message", "13"), spacing2=5)

    self.txtMsg = tkinter.Text(self.frmLC)
    # 触发键盘的回车按键事件，发送消息
    self.txtMsg.bind("<KeyPress-Return>", self.send_msg_event)
    self.btnSend = tkinter.Button(self.frmLB, text='发送', width=12, command=self.send_msg)
    # 创建空的Label在左边占个位置，便于发送按钮靠右
    self.labSend = tkinter.Label(self.frmLB, width=55)

    # 窗口布局
    self.frmLT.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    self.frmLC.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    self.frmLB.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # 固定大小
    self.frmLT.grid_propagate(0)
    self.frmLC.grid_propagate(0)
    self.frmLB.grid_propagate(0)

    self.labSend.grid(row=0, column=0)
    # 发送按钮布局
    self.btnSend.grid(row=0, column=1)
    self.txtMsgList.grid()
    self.txtMsg.grid()

    # WM_DELETE_WINDOW 不能改变，这是捕获命令
    self.window.protocol('WM_DELETE_WINDOW', self.on_closing)