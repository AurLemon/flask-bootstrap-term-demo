import os
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import timedelta
from datetime import datetime
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename
import uuid

# 初始化 Flask 应用
app = Flask(__name__, static_folder='static')

# SQLite 数据库配置
db_dir = './database'
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

db_path = os.path.join(db_dir, "sqlite.db")
full_db_path = os.path.abspath(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{full_db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置文件上传目录
UPLOAD_FOLDER = './upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = set()    # 不限制文件类型
app.config['MAX_CONTENT_LENGTH'] = None     # 不限制大小

db = SQLAlchemy(app)

# 加密解密 Token 的 Secret Key
app.config['SECRET_KEY'] = 'AURLEMON'

# 用户表模型
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)                                         # 用户ID（UUID等）
    first_name = db.Column(db.String(50), nullable=False)                                   # 名字
    last_name = db.Column(db.String(50), nullable=False)                                    # 姓氏
    username = db.Column(db.String(50), unique=True, nullable=False)                        # 用户名
    reg_date = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))      # 注册时间
    password = db.Column(db.String(100), nullable=False)                                    # 密码
    apply_status = db.Column(db.Integer, nullable=False)                                    # 申请状态
    is_admin = db.Column(db.Boolean, default=False)                                         # 是否为管理员

    def __repr__(self):
        return f"<User {self.username}>"

# 新闻表模型
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                            # 自动增长的ID
    title = db.Column(db.String(200), nullable=False)                                       # 新闻标题
    content = db.Column(db.Text, nullable=False)                                            # 新闻内容
    author = db.Column(db.String(100), nullable=False)                                      # 作者
    image_url = db.Column(db.String(200))                                                   # 图片URL
    publish_date = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))  # 发布时间
    is_published = db.Column(db.Boolean, default=False)                                     # 是否发布
    is_deleted = db.Column(db.Boolean, default=False)                                       # 是否删除
    details_content = db.Column(db.Text)                                                    # 详细内容
    view_count = db.Column(db.Integer, default=0)                                           # 查看次数

    def __repr__(self):
        return f"<News {self.title}>"

# 文件表模型
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                            # 自动增长的ID
    original_filename = db.Column(db.String(200), nullable=False)                           # 原始文件名
    stored_filename = db.Column(db.String(200), nullable=False)                             # 存储的文件名（随机生成）
    size = db.Column(db.Integer, nullable=False)                                            # 文件大小
    file_type = db.Column(db.String(50), nullable=False)                                    # 文件类型
    upload_date = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Asia/Shanghai')))   # 上传时间

    def __repr__(self):
        return f"<File {self.original_filename}>"

# Token 表模型    
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)  # 用户ID
    token = db.Column(db.String(512), unique=True, nullable=False)  # 存储的Token
    expiration = db.Column(db.DateTime, nullable=False)  # Token过期时间

    def __repr__(self):
        return f"<Token {self.token}>"

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

# 生成 Token
def generate_token(user):
    payload = {
        'user_id': user.id,
        'is_admin': user.is_admin,
        'exp': datetime.now(ZoneInfo('Asia/Shanghai')) + timedelta(hours=1)
    }
    
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    
    new_token = Token(user_id=user.id, token=token, expiration=payload['exp'])
    db.session.add(new_token)
    db.session.commit()
    
    return token

# 验证 Token    
def verify_token(raw_token):
    def get_token_from_header(raw_token):
        if raw_token.startswith("Bearer "):
            return raw_token[7:]
        return raw_token
    
    raw_token = get_token_from_header(raw_token)
    
    try:
        token_entry = db.session.query(Token).filter_by(token=raw_token).first()
        
        if not token_entry:
            return {"message": "Token not found!"}, 404
        
        if token_entry.expiration.tzinfo is None:
            token_entry_expiration = token_entry.expiration.replace(tzinfo=ZoneInfo('Asia/Shanghai'))
        else:
            token_entry_expiration = token_entry.expiration

        current_time = datetime.now(ZoneInfo('Asia/Shanghai'))

        if token_entry_expiration < current_time:
            db.session.delete(token_entry)
            db.session.commit()
            return {"message": "Token expired", "expires": token_entry_expiration}, 401

        payload = jwt.decode(raw_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload

    except jwt.ExpiredSignatureError:
        return {"message": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"message": "Invalid token"}, 400

# API：登录
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or user.password != password:
        return api_response(False, {"message": "Invalid username or password"})

    token = generate_token(user)
    
    return api_response(True, {"token": token})

# API：获取用户信息
@app.route("/api/user/info", methods=["GET"])
def get_user_info():
    token = request.headers.get('Authorization')
    
    if not token:
        return api_response(False, {"message": "Token is missing"})
    
    try:
        payload = verify_token(token)
        
        if not payload:
            return api_response(False, {"message": "Invalid or expired token"})
        
        if isinstance(payload, dict) and 'user_id' in payload:
            user_id = payload['user_id']
        else:
            raise ValueError("Invalid payload format")
        
        user = User.query.get(user_id)
        
        if not user:
            return api_response(False, {"message": "User not found"})
        
        user_info = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "reg_date": user.reg_date.strftime('%Y-%m-%d %H:%M:%S'),
            "apply_status": user.apply_status,
            "is_admin": user.is_admin
        }
        
        return api_response(True, user_info)

    except ValueError as ve:
        return api_response(False, {"message": str(ve)})
    except Exception as e:
        return api_response(False, {"message": f"An error occurred: {str(e)}"})

# API：更新用户密码
@app.route("/api/user/password", methods=["PUT"])
def change_password():
    token = request.headers.get('Authorization')
    
    if not token:
        return api_response(False, {"message": "Token is missing"})
    
    payload = verify_token(token)
    
    if not payload:
        return api_response(False, {"message": "Invalid or expired token"})
    
    user = User.query.get(payload['user_id'])
    
    if not user:
        return api_response(False, {"message": "User not found"})
    
    data = request.get_json()
    new_password = data.get('new_password')

    user.password = new_password
    db.session.commit()

    return api_response(True, {"message": "Password updated successfully"})

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

# API：编辑用户信息
@app.route("/api/user/<string:id>", methods=["PUT"])
def update_user(id):
    token = request.headers.get('Authorization')
    
    if not token:
        return api_response(False, {"message": "Token is missing"})
    
    payload = verify_token(token)
    
    if not payload:
        return api_response(False, {"message": "Invalid or expired token"})
    
    if not payload['is_admin']:
        return api_response(False, {"message": "Permission denied, only admins can edit users"})
    
    user = User.query.get(id)
    
    if not user:
        return api_response(False, {"message": "User not found"})
    
    data = request.get_json()
    
    first_name = data.get('first_name', user.first_name)
    last_name = data.get('last_name', user.last_name)
    username = data.get('username', user.username)
    apply_status = data.get('apply_status', user.apply_status)
    is_admin = data.get('is_admin', user.is_admin)
    
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.apply_status = apply_status
    user.is_admin = is_admin
    
    db.session.commit()

    return api_response(True, {"message": "User updated successfully", "user_info": {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "apply_status": user.apply_status,
        "is_admin": user.is_admin
    }})

# API：删除用户
@app.route("/api/user/<string:id>", methods=["DELETE"])
def delete_user(id):
    token = request.headers.get('Authorization')
    
    if not token:
        return api_response(False, {"message": "Token is missing"})
    
    payload = verify_token(token)
    
    if not payload:
        return api_response(False, {"message": "Invalid or expired token"})
    
    if not payload['is_admin']:
        return api_response(False, {"message": "Permission denied, only admins can delete users"})
    
    user = User.query.get(id)
    
    if not user:
        return api_response(False, {"message": "User not found"})
    
    db.session.delete(user)
    db.session.commit()

    return api_response(True, {"message": "User deleted successfully"})

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

@app.route("/api/news/<int:id>", methods=["GET"])
def get_news_by_id(id):
    news = News.query.get(id)
    if not news:
        return api_response(False, {"message": "News not found"})
    
    author = User.query.get(news.author)
    author_username = author.username if author else "Unknown"
    
    formatted_publish_date = news.publish_date.strftime('%Y-%m-%d %H:%M:%S')
    news_data = {
        "id": news.id,
        "title": news.title,
        "author": author_username,
        "publish_date": formatted_publish_date,
        "view_count": news.view_count,
        "content": news.content,
        "image_url": news.image_url,
        "is_published": news.is_published,
        "is_deleted": news.is_deleted,
        "details_content": news.details_content
    }

    return api_response(True, news_data)

# API：上传文件
@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return api_response(False, {"message": "No file part"})

    file = request.files['file']
    
    if file.filename == '':
        return api_response(False, {"message": "No selected file"})

    original_filename = secure_filename(file.filename)
    
    stored_filename = str(uuid.uuid4()) + os.path.splitext(original_filename)[-1]
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
    
    file.save(file_path)

    file_size = os.path.getsize(file_path)
    file_type = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else 'unknown'

    new_file = File(
        original_filename=original_filename,
        stored_filename=stored_filename,
        size=file_size,
        file_type=file_type
    )
    db.session.add(new_file)
    db.session.commit()

    return api_response(True, {"message": "File uploaded successfully", "file_info": {
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "size": file_size,
        "file_type": file_type
    }})

# API：列出已上传文件
@app.route("/api/upload/list", methods=["GET"])
def list_uploaded_files():
    files_info = []
    
    files = File.query.all()
    
    for file in files:
        files_info.append({
            "id": file.id,
            "original_filename": file.original_filename,
            "stored_filename": file.stored_filename,
            "size": file.size,
            "file_type": file.file_type,
            "upload_date": file.upload_date.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return api_response(True, files_info)

# API：删除文件
@app.route("/api/upload/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file_to_delete = File.query.get(file_id)
    
    if not file_to_delete:
        return api_response(False, {"message": "File not found"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete.stored_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(file_to_delete)
    db.session.commit()

    return api_response(True, {"message": "File deleted successfully"})

# API：文件下载
@app.route("/upload/<stored_filename>")
def uploaded_file(stored_filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], stored_filename)

# 捕获所有非 API 请求并返回 index.html 或静态文件
@app.route("/<path:path>")
def catch_all(path):
    if path.startswith('api/'):
        return jsonify({"message": "API response"})

    static_path = os.path.join(app.root_path, 'static', path)
    
    if os.path.exists(static_path):
        return send_from_directory(os.path.join(app.root_path, 'static'), path)
    
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
