from app import app


# ToDo: 在欢迎页面加入简易使用说明。
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

# ToDo: 制作简易的用户交互界面

