"""
Flask 基础示例 5: 静态文件服务
Flask Basic Example 5: Static Files

演示如何在 Flask 中处理静态文件（CSS、JavaScript、图片等）。
Demonstrates how to serve static files (CSS, JavaScript, images) in Flask.
"""

from flask import Flask, render_template_string, url_for, send_from_directory
import os

app = Flask(__name__)

# 创建静态文件目录
static_dir = os.path.join(os.path.dirname(__file__), 'static')
os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
os.makedirs(os.path.join(static_dir, 'images'), exist_ok=True)

# 创建示例 CSS 文件
css_content = '''
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #333;
}

.container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

h1 {
    color: #667eea;
    border-bottom: 3px solid #667eea;
    padding-bottom: 10px;
}

.feature {
    background: #f8f9fa;
    padding: 15px;
    margin: 15px 0;
    border-left: 4px solid #667eea;
    border-radius: 5px;
}

button {
    background: #667eea;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin: 10px 5px;
}

button:hover {
    background: #764ba2;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.image-demo {
    text-align: center;
    margin: 20px 0;
}

.demo-image {
    max-width: 100%;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
'''

# 创建示例 JavaScript 文件
js_content = '''
// Flask 静态文件 JavaScript 示例
console.log('✅ JavaScript file loaded successfully!');

// DOM 加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM Content Loaded');
    
    // 显示欢迎消息
    showWelcomeMessage();
    
    // 添加按钮点击事件
    setupButtonHandlers();
});

function showWelcomeMessage() {
    const now = new Date();
    const hour = now.getHours();
    let greeting = '';
    
    if (hour < 12) {
        greeting = '早上好 (Good Morning)';
    } else if (hour < 18) {
        greeting = '下午好 (Good Afternoon)';
    } else {
        greeting = '晚上好 (Good Evening)';
    }
    
    console.log(`👋 ${greeting}!`);
}

function setupButtonHandlers() {
    // 为所有按钮添加点击事件
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function(e) {
            // 如果按钮没有特定的 onclick，显示一个消息
            if (!this.hasAttribute('onclick')) {
                showNotification('按钮被点击了！(Button clicked!)');
            }
        });
    });
}

function changeColor() {
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.querySelector('h1').style.color = randomColor;
    showNotification(`颜色已改变为 ${randomColor}`);
}

function showAlert() {
    alert('🎉 这是一个来自外部 JavaScript 文件的提示！\\n\\nThis is an alert from external JavaScript file!');
}

function showNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // 3秒后移除通知
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 动态加载统计
window.addEventListener('load', function() {
    console.log('🎨 All resources loaded including images and CSS');
    console.log(`📊 Total scripts: ${document.scripts.length}`);
    console.log(`🎨 Total stylesheets: ${document.styleSheets.length}`);
});
'''

# 写入文件
with open(os.path.join(static_dir, 'css', 'style.css'), 'w', encoding='utf-8') as f:
    f.write(css_content)

with open(os.path.join(static_dir, 'js', 'app.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)


@app.route('/')
def index():
    """演示静态文件的使用"""
    template = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask 静态文件示例</title>
        
        <!-- 引入外部 CSS -->
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
        
        <!-- 内联 CSS 添加动画 -->
        <style>
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Flask 静态文件示例 📁</h1>
            <h2>Static Files Example</h2>
            
            <div class="feature">
                <h3>📋 什么是静态文件？</h3>
                <p>静态文件是不需要服务器处理就能直接提供给客户端的文件，包括：</p>
                <ul>
                    <li><strong>CSS</strong> - 样式表文件</li>
                    <li><strong>JavaScript</strong> - 脚本文件</li>
                    <li><strong>Images</strong> - 图片文件 (PNG, JPG, SVG, etc.)</li>
                    <li><strong>Fonts</strong> - 字体文件</li>
                    <li><strong>其他资源</strong> - PDF, 视频, 音频等</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🎨 当前页面使用的静态文件</h3>
                <ul>
                    <li><strong>CSS:</strong> <code>{{ url_for('static', filename='css/style.css') }}</code></li>
                    <li><strong>JavaScript:</strong> <code>{{ url_for('static', filename='js/app.js') }}</code></li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🔧 url_for() 函数</h3>
                <p>Flask 提供 <code>url_for()</code> 函数来生成静态文件的 URL：</p>
                <pre><code>&lt;link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"&gt;
&lt;script src="{{ url_for('static', filename='js/app.js') }}"&gt;&lt;/script&gt;
&lt;img src="{{ url_for('static', filename='images/logo.png') }}"&gt;</code></pre>
                
                <p><strong>优势：</strong></p>
                <ul>
                    <li>自动处理路径</li>
                    <li>支持不同的部署环境</li>
                    <li>便于维护和重构</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🎮 JavaScript 交互示例</h3>
                <p>这些按钮使用外部 JavaScript 文件中的函数：</p>
                <button onclick="changeColor()">🎨 改变标题颜色</button>
                <button onclick="showAlert()">💬 显示提示</button>
                <button onclick="location.href='/api'">📦 查看 API 示例</button>
            </div>
            
            <div class="feature">
                <h3>📂 默认静态文件夹结构</h3>
                <pre><code>your_app/
├── app.py
├── static/              ← Flask 默认静态文件夹
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── logo.png
└── templates/
    └── index.html</code></pre>
            </div>
            
            <div class="feature">
                <h3>⚙️ 自定义静态文件夹</h3>
                <p>可以在创建 Flask 应用时自定义静态文件夹：</p>
                <pre><code>app = Flask(__name__, 
           static_folder='assets',    # 自定义文件夹名
           static_url_path='/assets') # 自定义 URL 路径</code></pre>
            </div>
            
            <div class="feature">
                <h3>🚀 生产环境建议</h3>
                <ul>
                    <li>使用 CDN 加速静态资源加载</li>
                    <li>启用 Gzip 压缩</li>
                    <li>设置合适的缓存策略</li>
                    <li>使用 Nginx 或 Apache 直接服务静态文件</li>
                    <li>压缩和合并 CSS/JS 文件</li>
                </ul>
            </div>
        </div>
        
        <!-- 引入外部 JavaScript -->
        <script src="{{ url_for('static', filename='js/app.js') }}"></script>
        
        <!-- 内联 JavaScript -->
        <script>
            console.log('✅ 页面加载完成！');
            console.log('📊 Static folder:', "{{ url_for('static', filename='') }}");
        </script>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/api')
def api_demo():
    """API 端点返回 JSON"""
    return {
        'message': '这是一个 API 端点',
        'static_files': {
            'css': url_for('static', filename='css/style.css', _external=True),
            'js': url_for('static', filename='js/app.js', _external=True),
        },
        'tip': '在生产环境中，建议使用 Nginx 等服务器直接服务静态文件'
    }


# 自定义静态文件服务（高级用法）
@app.route('/files/<path:filename>')
def custom_static(filename):
    """
    自定义静态文件端点
    可以添加额外的逻辑，如访问控制、日志记录等
    """
    return send_from_directory(static_dir, filename)


if __name__ == '__main__':
    print("🚀 Starting Flask Static Files Example...")
    print(f"📁 Static folder: {static_dir}")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n静态文件 URLs:")
    print(f"  CSS: http://127.0.0.1:5000/static/css/style.css")
    print(f"  JS:  http://127.0.0.1:5000/static/js/app.js")
    app.run(debug=True, host='0.0.0.0', port=5000)
