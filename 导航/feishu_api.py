# 飞书API交互模块

import requests
import json
import time
from config import Config

class FeishuAPI:
    def __init__(self):
        self.app_id = Config.FEISHU_APP_ID
        self.app_secret = Config.FEISHU_APP_SECRET
        self.app_token = Config.APP_TOKEN  # 保留APP_TOKEN以兼容旧代码
        self.base_id = Config.BASE_ID  # 使用新的BASE_ID
        self.table_id = Config.TABLE_ID.split('&')[0]  # 提取表格ID，去除view参数
        self.view_id = None
        # 检查TABLE_ID是否包含view参数
        if '&view=' in Config.TABLE_ID:
            self.view_id = Config.TABLE_ID.split('&view=')[1]
        self.tenant_access_token = None
        self.token_expire_time = 0
        self.cache = {}
        self.cache_time = {}
        self.cache_timeout = Config.CACHE_TIMEOUT
    
    def _get_tenant_access_token(self):
        """获取飞书tenant_access_token"""
        # 检查现有token是否过期
        if self.tenant_access_token and time.time() < self.token_expire_time:
            return self.tenant_access_token
            
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload)
            response_data = response.json()
            
            if response_data.get("code") == 0:
                self.tenant_access_token = response_data.get("tenant_access_token")
                # 设置过期时间（提前5分钟过期，以防边界情况）
                self.token_expire_time = time.time() + response_data.get("expire") - 300
                return self.tenant_access_token
            else:
                print(f"获取tenant_access_token失败: {response_data}")
                return None
        except Exception as e:
            print(f"获取tenant_access_token异常: {str(e)}")
            return None
    
    def get_table_records(self, use_cache=True):
        """获取多维表格数据"""
        # 检查缓存
        cache_key = f"table_records_{self.table_id}"
        if use_cache and cache_key in self.cache and time.time() - self.cache_time.get(cache_key, 0) < self.cache_timeout:
            return self.cache[cache_key]
            
        token = self._get_tenant_access_token()
        if not token:
            return {"error": "获取授权失败"}
        
        # 根据飞书API文档构建正确的API路径
        # 多维表格API文档: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/list
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.base_id}/tables/{self.table_id}/records"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # 添加分页参数，确保获取所有记录
        params = {
            'page_size': 100  # 每页记录数，最大值为100
        }
        
        # 如果有视图ID，添加到参数中
        if self.view_id:
            params['view_id'] = self.view_id
        
        try:
            print(f"请求飞书API: {url}")
            print(f"请求参数: base_id={self.base_id}, table_id={self.table_id}, view_id={self.view_id}")
            response = requests.get(url, headers=headers, params=params)
            response_data = response.json()
            
            if response_data.get("code") == 0:
                result = response_data.get("data", {})
                # 更新缓存
                self.cache[cache_key] = result
                self.cache_time[cache_key] = time.time()
                return result
            else:
                print(f"获取表格数据失败: {response_data}")
                return {"error": f"获取表格数据失败: {response_data.get('msg')}"}
        except Exception as e:
            print(f"获取表格数据异常: {str(e)}")
            return {"error": f"获取表格数据异常: {str(e)}"}
    
    def get_formatted_data(self, use_cache=True):
        """获取格式化后的数据，适合前端展示"""
        records_data = self.get_table_records(use_cache=use_cache)
        
        if "error" in records_data:
            return {"error": records_data["error"]}
            
        items = []
        # 默认分类列表
        default_categories = [
            "AI应用", "AI模型", "AI社区", "IOT应用", "工作应用", 
            "AI办公", "AI编程", "AI产品经理", "AI写作", "其他"
        ]
        categories = set(default_categories)
        
        for record in records_data.get("items", []):
            fields = record.get("fields", {})
            
            # 提取必要字段
            title = fields.get("标题", "")
            url = fields.get("链接地址", "")
            # 确保URL是字符串类型
            if isinstance(url, dict) and "text" in url:
                url = url.get("text", "")
            elif isinstance(url, dict) and "link" in url:
                url = url.get("link", "")
            elif not isinstance(url, str):
                url = str(url) if url else ""
            category = fields.get("分类", "未分类")
            description = fields.get("描述", "")
            icon = fields.get("图标", "")
            
            # 只有标题和链接都存在时才添加
            if title and url:
                item = {
                    "id": record.get("record_id", ""),
                    "title": title,
                    "url": url,
                    "category": category,
                    "description": description,
                    "icon": icon
                }
                items.append(item)
                categories.add(category)
        
        return {
            "items": items,
            "categories": sorted(list(categories))
        }