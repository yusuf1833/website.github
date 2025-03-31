# 飞书应用配置文件
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a76c243cb9f0d00b")
    FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "NiFzCMPVTMHC75LVj9fWLYikpFyGbmSK")
    
    # 多维表格配置
    APP_TOKEN = os.environ.get("APP_TOKEN", "bascnCMLoaO7qDnUJbXcHFGTnvd")  # 飞书多维表格的应用ID
    BASE_ID = os.environ.get("BASE_ID", "VS3zbdBAVa4eMKsF1oncLLFRnIc")  # 多维表格的BASE_ID
    TABLE_ID = os.environ.get("TABLE_ID", "tblYwz3x8qr2oWBz&view=vew23wxaGz")  # 多维表格ID
    
    # Flask应用配置
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")
    DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "t")
    
    # 缓存配置（单位：秒）
    CACHE_TIMEOUT = int(os.environ.get("CACHE_TIMEOUT", 300))  # 5分钟缓存过期