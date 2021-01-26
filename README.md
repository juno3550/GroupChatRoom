# GroupChatRoom
带图形界面的群聊聊天室

Chat 包：
* server.py：服务器端执行代码（TCP服务器，根据客户端消息调用mode包的注册、登录、聊天功能）
* client.py：客户端执行代码（连接服务器端，进行注册、登录、聊天）
* client_draw.py：客户端图形界面绘制

mode 包：
* chat_mode.py：封装服务器端的聊天逻辑
* login_mode.py：封装服务器端的登录逻辑
* register_mode.py：封装服务器端的注册逻辑

db 包：
* user_info_util.py：基于mysql_util查询或新增用户信息
* mysql_util.py：封装mysql基础操作
