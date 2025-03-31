/**
 * 网址导航网站前端交互脚本
 * 实现数据加载、分类筛选、主题切换等功能
 */

// DOM 元素
const sitesGrid = document.getElementById('sites-grid');
const categoryButtons = document.getElementById('category-buttons');
const allCategoryBtn = document.getElementById('all-category');
const themeToggle = document.getElementById('theme-toggle');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');
const noData = document.getElementById('no-data');

// 状态变量
let sites = [];
let categories = [];
let currentCategory = 'all';

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 加载数据
    loadData();
    
    // 初始化主题
    initTheme();
    
    // 绑定主题切换事件
    themeToggle.addEventListener('click', toggleTheme);
});

/**
 * 从API加载数据
 */
async function loadData() {
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // 保存数据
        sites = data.items || [];
        
        // 确保默认分类列表始终存在
        const defaultCategories = [
            "AI应用", "AI模型", "AI社区", "IOT应用", "工作应用", 
            "AI办公", "AI编程", "AI产品经理", "AI写作", "其他"
        ];
        
        // 合并API返回的分类和默认分类
        const apiCategories = data.categories || [];
        categories = [...new Set([...defaultCategories, ...apiCategories])];
        
        // 渲染分类按钮
        renderCategoryButtons();
        
        // 渲染网站卡片
        renderSites();
        
        // 显示无数据提示（如果没有数据）
        if (sites.length === 0) {
            noData.classList.remove('hidden');
        } else {
            noData.classList.add('hidden');
        }
    } catch (error) {
        showError('获取数据失败，请检查网络连接或刷新页面重试');
        console.error('加载数据错误:', error);
    } finally {
        showLoading(false);
    }
}

/**
 * 渲染分类按钮
 */
function renderCategoryButtons() {
    // 清空现有按钮
    categoryButtons.innerHTML = '';
    
    // 创建分类按钮
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'category-btn px-4 py-1.5 rounded-full text-sm font-medium';
        button.textContent = category;
        button.addEventListener('click', () => filterByCategory(category));
        categoryButtons.appendChild(button);
    });
    
    // 如果有分类，默认选中第一个分类
    if (categories.length > 0) {
        filterByCategory(categories[0]);
    } else {
        // 如果没有分类，显示所有网站
        currentCategory = '';
        renderSites();
    }
}

/**
 * 按分类筛选网站
 * @param {string} category - 分类名称
 */
function filterByCategory(category) {
    currentCategory = category;
    
    // 更新按钮样式
    const buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(btn => {
        if (btn.textContent === category) {
            btn.classList.add('bg-apple-blue', 'text-white');
            btn.classList.remove('bg-opacity-10');
        } else {
            btn.classList.remove('bg-apple-blue', 'text-white');
            btn.classList.add('bg-opacity-10');
        }
    });
    
    // 渲染筛选后的网站
    renderSites();
}

/**
 * 渲染网站卡片
 */
function renderSites() {
    // 清空现有卡片
    sitesGrid.innerHTML = '';
    
    // 筛选网站
    let filteredSites;
    if (!currentCategory || currentCategory === '') {
        filteredSites = sites;
    } else {
        filteredSites = sites.filter(site => site.category === currentCategory);
    }
    
    // 创建网站卡片
    filteredSites.forEach(site => {
        const card = document.createElement('div');
        card.className = 'site-card bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-sm hover:shadow-md dark:shadow-gray-900/30 border border-gray-100 dark:border-gray-700';
        
        // 生成图标HTML
        let iconHtml = '';
        if (site.icon) {
            // 如果有自定义图标
            iconHtml = `<img src="${site.icon}" alt="${site.title}" class="w-10 h-10 object-contain">`;
        } else {
            // 使用默认图标（首字母）
            const initial = site.title.charAt(0).toUpperCase();
            const colors = ['bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-pink-500', 'bg-yellow-500', 'bg-red-500', 'bg-indigo-500'];
            const randomColor = colors[Math.floor(Math.random() * colors.length)];
            iconHtml = `<div class="${randomColor} w-10 h-10 rounded-md flex items-center justify-center text-white font-medium text-lg">${initial}</div>`;
        }
        
        // 卡片内容
        card.innerHTML = `
            <a href="${site.url}" target="_blank" rel="noopener noreferrer" class="block p-4">
                <div class="flex items-start space-x-3">
                    <div class="flex-shrink-0">
                        ${iconHtml}
                    </div>
                    <div class="flex-1 min-w-0">
                        <h3 class="text-base font-medium text-gray-900 dark:text-white truncate">${site.title}</h3>
                        ${site.description ? `<p class="mt-1 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">${site.description}</p>` : ''}
                        <div class="mt-2 flex items-center">
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300">
                                ${site.category}
                            </span>
                        </div>
                    </div>
                </div>
            </a>
        `;
        
        sitesGrid.appendChild(card);
    });
    
    // 显示无数据提示（如果筛选后没有数据）
    if (filteredSites.length === 0) {
        const emptyMessage = document.createElement('div');
        emptyMessage.className = 'col-span-full py-12 text-center text-gray-500 dark:text-gray-400';
        emptyMessage.innerHTML = `
            <svg class="w-12 h-12 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 20h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <h3 class="text-lg font-medium">该分类下暂无网站</h3>
            <p class="mt-1">请选择其他分类或在飞书多维表格中添加数据</p>
        `;
        sitesGrid.appendChild(emptyMessage);
    }
}

/**
 * 初始化主题
 */
function initTheme() {
    // 检查本地存储中的主题设置
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // 如果有保存的主题设置或系统偏好深色模式
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
}

/**
 * 切换主题
 */
function toggleTheme() {
    if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

/**
 * 显示/隐藏加载指示器
 * @param {boolean} show - 是否显示
 */
function showLoading(show) {
    if (show) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

/**
 * 显示错误信息
 * @param {string} message - 错误信息
 */
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
}

/**
 * 隐藏错误信息
 */
function hideError() {
    errorMessage.classList.add('hidden');
}

/**
 * 刷新数据
 */
async function refreshData() {
    showLoading(true);
    hideError();
    
    try {
        const response = await fetch('/api/refresh', {
            method: 'POST'
        });
        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        // 更新数据
        sites = data.items || [];
        categories = data.categories || [];
        
        // 重新渲染
        renderCategoryButtons();
        renderSites();
        
        // 显示无数据提示（如果没有数据）
        if (sites.length === 0) {
            noData.classList.remove('hidden');
        } else {
            noData.classList.add('hidden');
        }
    } catch (error) {
        showError('刷新数据失败，请检查网络连接或重试');
        console.error('刷新数据错误:', error);
    } finally {
        showLoading(false);
    }
}