# 网址导航网站（飞书多维表格驱动）

> 版本 1.0.0 | 2024年1月

一个简洁优雅的网址导航网站，采用苹果设计风格，数据来源于飞书多维表格。

## 版本特性

- 基于飞书多维表格的数据驱动，实现内容的灵活管理
- 采用苹果设计风格，提供优雅的用户界面
- 支持深色/浅色主题自动切换
- 响应式布局，完美适配各种设备
- 分类筛选功能，快速定位所需内容
- 支持自定义网站图标和描述

## 功能特点

- 动态导航菜单管理
- 网站内容分类卡片式显示：标题、描述等
- 深色/浅色主题切换
- 响应式设计
- 分类筛选

## 技术栈

- 前端：HTML, CSS, JavaScript
- UI框架：Tailwind CSS
- 图标库：Font Awesome
- 字体：Google Fonts (Noto Sans SC, Noto Serif SC)
- 数据源：飞书多维表格 API

## 项目结构

```
/
├── static/             # 静态资源
│   ├── css/            # CSS 文件
│   ├── js/             # JavaScript 文件
│   └── img/            # 图片资源
├── templates/          # HTML 模板
├── app.py              # Flask 应用主文件
├── config.py           # 配置文件
├── feishu_api.py       # 飞书 API 交互
└── README.md           # 项目说明
```

## 安装与使用

1. 克隆项目

2. 安装依赖
   ```
   pip install -r requirements.txt
   ```

3. 配置飞书应用信息
   在 `config.py` 中填入您的飞书应用信息

4. 运行应用
   ```
   python app.py
   ```

5. 访问网站
   打开浏览器访问 `http://localhost:5000`

## 飞书配置

1. 创建飞书应用
   - 获取应用凭证（App ID 和 App Secret）
   - 开启多维表格权限：`bitable:record:read`

2. 创建多维表格
   - 创建包含以下字段的表格：
     * 标题
     * 链接地址
     * 分类
     * 描述（可选）
     * 图标（可选）

## 项目维护

如需帮助或报告问题，请提供以下信息：
1. 完整的错误信息
2. 飞书应用配置截图
3. 多维表格的结构说明

## Vercel部署指南

本应用已配置好可以一键部署到Vercel。按照以下步骤操作：

1. 在GitHub上创建仓库并上传代码
   ```
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repository-url
   git push -u origin main
   ```

2. 登录Vercel并导入项目
   - 访问[Vercel](https://vercel.com)并登录
   - 点击"New Project"
   - 选择您刚刚创建的GitHub仓库
   - 保留默认设置，Vercel会自动检测Flask应用

3. 配置环境变量
   - 在项目设置中，找到"Environment Variables"
   - 添加以下环境变量：
     * `FEISHU_APP_ID`: 您的飞书应用ID
     * `FEISHU_APP_SECRET`: 您的飞书应用密钥
     * `APP_TOKEN`: 多维表格的应用ID
     * `BASE_ID`: 多维表格的BASE_ID
     * `TABLE_ID`: 多维表格ID
     * `SECRET_KEY`: Flask密钥(任意字符串)
     * `DEBUG`: False (生产环境)

4. 部署
   - 点击"Deploy"按钮
   - Vercel会自动构建和部署您的应用
   - 完成后，您可以通过提供的URL访问您的网址导航网站

5. 绑定自定义域名（可选）
   - 在项目设置中，找到"Domains"
   - 添加您的自定义域名并按照指示完成DNS配置