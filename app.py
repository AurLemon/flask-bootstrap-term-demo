import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo

# 初始化 Flask 应用
app = Flask(__name__, static_folder='static')

# SQLite 数据库
db_dir = './database'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, "sqlite.db")
full_db_path = os.path.abspath(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{full_db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 用户表模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # 用户ID（UUID等）
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))  # 注册时间
    password = db.Column(db.String(100), nullable=False)  # 密码
    apply_status = db.Column(db.Integer, nullable=False)  # 申请状态
    is_admin = db.Column(db.Boolean, default=False)  # 是否为管理员

    def __repr__(self):
        return f"<User {self.username}>"

# 新闻表模型
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 自动增长的ID
    title = db.Column(db.String(200), nullable=False)  # 新闻标题
    content = db.Column(db.Text, nullable=False)  # 新闻内容
    author = db.Column(db.String(100), nullable=False)  # 作者
    image_url = db.Column(db.String(200))  # 图片URL
    publish_date = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))  # 发布时间
    is_published = db.Column(db.Boolean, default=False)  # 是否发布
    is_deleted = db.Column(db.Boolean, default=False)  # 是否删除
    details_content = db.Column(db.Text)  # 详细内容
    view_count = db.Column(db.Integer, default=0)  # 查看次数

    def __repr__(self):
        return f"<News {self.title}>"

# 自动创建数据库和表
def create_tables():
    print(" * Creating all tables...")
    with app.app_context():
        db.create_all()
    print(" * Tables created!")

# API 响应格式化函数
def api_response(is_success, data=None):
    status = 'success' if is_success else 'error'
    time = datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    
    response = {
        'status': status,
        'time': time,
        'data': data
    }
    
    return jsonify(response)

# API：查看所有用户
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_data = []
    for user in users:
        formatted_reg_date = user.reg_date.strftime('%Y-%m-%d %H:%M:%S')

        user_info = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "reg_date": formatted_reg_date,
            "apply_status": user.apply_status,
            "is_admin": user.is_admin
        }
        user_data.append(user_info)

    return api_response(True, user_data)

# API：查看所有新闻
@app.route("/api/news", methods=["GET"])
def get_news():
    news_list = News.query.all()

    news_data = []
    
    for news in news_list:
        formatted_publish_date = news.publish_date.strftime('%Y-%m-%d %H:%M:%S')

        news_info = {
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "image_url": news.image_url,
            "author": news.author,
            "publish_date": formatted_publish_date,
            "view_count": news.view_count
        }

        news_data.append(news_info)

    return api_response(True, news_data)

# API：查看热门新闻
@app.route("/api/news/hot", methods=["GET"])
def get_hot_news():
    daily_hots = News.query.order_by(News.view_count.desc()).limit(3).all()
    recent_release = News.query.order_by(News.publish_date.desc()).limit(3).all()

    daily_hots_data = []
    for news in daily_hots:
        formatted_publish_date = news.publish_date.strftime('%Y-%m-%d %H:%M:%S')
        daily_hots_data.append({
            "id": news.id,
            "title": news.title,
            "author": news.author,
            "publish_date": formatted_publish_date,
            "view_count": news.view_count
        })

    recent_release_data = []
    for news in recent_release:
        formatted_publish_date = news.publish_date.strftime('%Y-%m-%d %H:%M:%S')
        recent_release_data.append({
            "id": news.id,
            "title": news.title,
            "author": news.author,
            "publish_date": formatted_publish_date,
            "view_count": news.view_count
        })

    return api_response(True, {
        "daily_hots": daily_hots_data,
        "recent_release": recent_release_data
    })

# API：查看新闻
@app.route("/api/news/<int:id>", methods=["GET"])
def get_news_by_id(id):
    news = News.query.get(id)
    if not news:
        return api_response(False, {"message": "News not found"})
    
    formatted_publish_date = news.publish_date.strftime('%Y-%m-%d %H:%M:%S')  # 格式化日期为 'yyyymmdd hhmmss'
    news_data = {
        "id": news.id,
        "title": news.title,
        "author": news.author,
        "publish_date": formatted_publish_date,
        "view_count": news.view_count,
        "content": news.content,
        "image_url": news.image_url,
        "is_published": news.is_published,
        "is_deleted": news.is_deleted,
        "details_content": news.details_content
    }

    return api_response(True, news_data)

# 捕获所有非API请求并返回index.html
@app.route("/<path:path>")
def catch_all(path):
    if path.startswith("api/"):
        return jsonify({"message": "API response"})
    
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
