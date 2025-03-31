from flask import Flask, render_template, jsonify, redirect, request
import sys
import os
from flask_cors import CORS

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_api import FeishuAPI
from config import Config

# 初始化Flask应用
app = Flask(__name__, 
            static_folder='../static', 
            template_folder='../templates')
            
# 应用配置
app.config.from_object(Config)
CORS(app)  # 启用CORS

# 初始化飞书API
feishu_api = FeishuAPI()

@app.route('/')
def home():
    """主页"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """获取飞书多维表格数据"""
    data = feishu_api.get_formatted_data()
    return jsonify(data)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """刷新数据缓存"""
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

# 本地开发服务器
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG) 