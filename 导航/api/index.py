from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_api import FeishuAPI
from config import Config

app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')
app.config.from_object(Config)
CORS(app)  # 启用CORS支持跨域请求

# 初始化飞书API
feishu_api = FeishuAPI()

@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """获取飞书多维表格数据的API接口"""
    data = feishu_api.get_formatted_data()
    return jsonify(data)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """强制刷新数据缓存的API接口"""
    data = feishu_api.get_formatted_data(use_cache=False)
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    """处理404错误"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """处理500错误"""
    return render_template('500.html'), 500

# Vercel需要这个入口点
# 这允许Vercel通过WSGI接口调用Flask应用
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# 本地开发服务器
if __name__ == '__main__':
    # 确保templates和static目录存在
    os.makedirs('../templates', exist_ok=True)
    os.makedirs('../static', exist_ok=True)
    
    # 启动应用
    app.run(host='0.0.0.0', port=8080, debug=Config.DEBUG) 