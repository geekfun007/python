"""
Flask 基础示例 3: 模板系统
Flask Basic Example 3: Template System

演示 Jinja2 模板引擎的使用，包括变量、控制结构、过滤器等。
Demonstrates Jinja2 template engine usage including variables, control structures, filters, etc.
"""

from flask import Flask, render_template_string, render_template
from datetime import datetime
import os

app = Flask(__name__)

# 创建模板目录
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(template_dir, exist_ok=True)


# ============================================
# 1. 基本模板渲染 (Basic Template Rendering)
# ============================================

@app.route('/')
def index():
    """使用 render_template_string 渲染内联模板"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 模板示例</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            a { color: #0066cc; text-decoration: none; margin-right: 15px; }
            a:hover { text-decoration: underline; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Flask 模板系统示例</h1>
        <h2>Template System Examples</h2>
        <ul>
            <li><a href="/variables">📌 变量和表达式 (Variables and Expressions)</a></li>
            <li><a href="/control">🔄 控制结构 (Control Structures)</a></li>
            <li><a href="/filters">🔧 过滤器 (Filters)</a></li>
            <li><a href="/inheritance">🧬 模板继承 (Template Inheritance)</a></li>
            <li><a href="/macros">🎯 宏 (Macros)</a></li>
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 2. 变量和表达式 (Variables and Expressions)
# ============================================

@app.route('/variables')
def variables():
    """演示模板变量的使用"""
    user = {
        'name': '张三',
        'email': 'zhangsan@example.com',
        'age': 28,
        'is_active': True,
        'roles': ['admin', 'user']
    }
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>变量示例</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .info { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            code { background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>变量和表达式 (Variables and Expressions)</h1>
        
        <div class="info">
            <h2>用户信息 (User Info)</h2>
            <p><strong>姓名:</strong> {{ user.name }}</p>
            <p><strong>邮箱:</strong> {{ user.email }}</p>
            <p><strong>年龄:</strong> {{ user.age }}</p>
            <p><strong>状态:</strong> {{ "活跃" if user.is_active else "不活跃" }}</p>
            <p><strong>角色:</strong> {{ user.roles | join(', ') }}</p>
            
            <h3>表达式计算:</h3>
            <p>明年年龄: {{ user.age + 1 }}</p>
            <p>姓名长度: {{ user.name | length }}</p>
            <p>大写姓名: {{ user.name | upper }}</p>
        </div>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template, user=user)


# ============================================
# 3. 控制结构 (Control Structures)
# ============================================

@app.route('/control')
def control():
    """演示 if/for 等控制结构"""
    users = [
        {'id': 1, 'name': '张三', 'age': 28, 'active': True},
        {'id': 2, 'name': '李四', 'age': 32, 'active': True},
        {'id': 3, 'name': '王五', 'age': 25, 'active': False},
        {'id': 4, 'name': 'Alice', 'age': 30, 'active': True},
    ]
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>控制结构</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
            th { background: #333; color: white; }
            tr:nth-child(even) { background: #f9f9f9; }
            .active { color: green; }
            .inactive { color: red; }
        </style>
    </head>
    <body>
        <h1>控制结构 (Control Structures)</h1>
        
        <h2>用户列表 (User List)</h2>
        {% if users %}
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>姓名</th>
                        <th>年龄</th>
                        <th>状态</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.age }}</td>
                        <td class="{{ 'active' if user.active else 'inactive' }}">
                            {{ "活跃" if user.active else "不活跃" }}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h3>循环变量 (Loop Variables)</h3>
            <ul>
                {% for user in users %}
                <li>
                    {{ loop.index }}. {{ user.name }}
                    {% if loop.first %} (第一个){% endif %}
                    {% if loop.last %} (最后一个){% endif %}
                    - 循环进度: {{ loop.index }}/{{ loop.length }}
                </li>
                {% endfor %}
            </ul>
        {% else %}
            <p>没有用户数据</p>
        {% endif %}
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template, users=users)


# ============================================
# 4. 过滤器 (Filters)
# ============================================

@app.route('/filters')
def filters():
    """演示 Jinja2 内置过滤器"""
    text = "Hello, Flask!"
    numbers = [1, 2, 3, 4, 5]
    items = ['apple', 'banana', 'cherry']
    now = datetime.now()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>过滤器</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .filter-example { background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #e8e8e8; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <h1>过滤器 (Filters)</h1>
        
        <div class="filter-example">
            <h3>字符串过滤器</h3>
            <p>原文: <code>{{ text }}</code></p>
            <p>大写: <code>{{ text | upper }}</code></p>
            <p>小写: <code>{{ text | lower }}</code></p>
            <p>首字母大写: <code>{{ text | capitalize }}</code></p>
            <p>标题格式: <code>{{ text | title }}</code></p>
            <p>长度: <code>{{ text | length }}</code></p>
            <p>反转: <code>{{ text | reverse }}</code></p>
        </div>
        
        <div class="filter-example">
            <h3>列表过滤器</h3>
            <p>原列表: <code>{{ numbers }}</code></p>
            <p>求和: <code>{{ numbers | sum }}</code></p>
            <p>最大值: <code>{{ numbers | max }}</code></p>
            <p>最小值: <code>{{ numbers | min }}</code></p>
            <p>长度: <code>{{ numbers | length }}</code></p>
            <p>连接: <code>{{ items | join(', ') }}</code></p>
            <p>首个元素: <code>{{ items | first }}</code></p>
            <p>最后元素: <code>{{ items | last }}</code></p>
        </div>
        
        <div class="filter-example">
            <h3>日期过滤器</h3>
            <p>当前时间: <code>{{ now }}</code></p>
            <p>格式化: <code>{{ now.strftime('%Y-%m-%d %H:%M:%S') }}</code></p>
        </div>
        
        <div class="filter-example">
            <h3>链式过滤器</h3>
            <p><code>{{ text | lower | reverse | title }}</code></p>
        </div>
        
        <div class="filter-example">
            <h3>默认值过滤器</h3>
            <p>空值处理: <code>{{ none_value | default('默认值') }}</code></p>
        </div>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template, 
                                 text=text, 
                                 numbers=numbers, 
                                 items=items, 
                                 now=now,
                                 none_value=None)


# ============================================
# 5. 模板继承 (Template Inheritance)
# ============================================

@app.route('/inheritance')
def inheritance():
    """演示模板继承"""
    # 定义基础模板
    base_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}默认标题{% endblock %}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            header { background: #333; color: white; padding: 20px; }
            nav { background: #555; padding: 10px; }
            nav a { color: white; margin-right: 15px; text-decoration: none; }
            main { max-width: 800px; margin: 20px auto; padding: 20px; }
            footer { background: #333; color: white; text-align: center; padding: 20px; margin-top: 50px; }
        </style>
    </head>
    <body>
        <header>
            <h1>{% block header %}我的网站{% endblock %}</h1>
        </header>
        
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
            <a href="/contact">联系</a>
        </nav>
        
        <main>
            {% block content %}
            <p>默认内容</p>
            {% endblock %}
        </main>
        
        <footer>
            {% block footer %}
            <p>&copy; 2024 Flask 示例</p>
            {% endblock %}
        </footer>
    </body>
    </html>
    '''
    
    # 子模板内容（模拟继承）
    content = '''
    <h2>模板继承示例</h2>
    <p>这个页面展示了模板继承的概念。</p>
    <p>子模板可以继承基础模板的结构，并覆盖特定的块（block）。</p>
    
    <h3>继承的优势：</h3>
    <ul>
        <li>减少代码重复</li>
        <li>保持页面结构一致</li>
        <li>易于维护和更新</li>
        <li>支持多级继承</li>
    </ul>
    
    <h3>Jinja2 继承语法：</h3>
    <pre><code>
{# 基础模板 base.html #}
&lt;html&gt;
  {% block content %}{% endblock %}
&lt;/html&gt;

{# 子模板 child.html #}
{% extends "base.html" %}
{% block content %}
  &lt;h1&gt;子页面内容&lt;/h1&gt;
{% endblock %}
    </code></pre>
    
    <p><a href="/">返回首页</a></p>
    '''
    
    # 将内容插入基础模板
    final_template = base_template.replace(
        '{% block content %}\n            <p>默认内容</p>\n            {% endblock %}',
        '{% block content %}\n            ' + content + '\n            {% endblock %}'
    )
    
    return render_template_string(final_template)


# ============================================
# 6. 宏 (Macros)
# ============================================

@app.route('/macros')
def macros():
    """演示宏的使用"""
    users = [
        {'name': '张三', 'role': 'admin'},
        {'name': '李四', 'role': 'user'},
        {'name': '王五', 'role': 'user'},
    ]
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>宏示例</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .user-card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .admin { background: #ffe6e6; }
            .user { background: #e6f3ff; }
        </style>
    </head>
    <body>
        <h1>宏 (Macros)</h1>
        
        {# 定义宏 - 类似函数 #}
        {% macro render_user_card(user) %}
        <div class="user-card {{ user.role }}">
            <h3>{{ user.name }}</h3>
            <p>角色: {{ user.role }}</p>
            {% if user.role == 'admin' %}
                <p>🔑 管理员权限</p>
            {% endif %}
        </div>
        {% endmacro %}
        
        <h2>用户卡片 (User Cards)</h2>
        {% for user in users %}
            {{ render_user_card(user) }}
        {% endfor %}
        
        <h3>宏的说明：</h3>
        <ul>
            <li>宏类似于函数，可以接受参数</li>
            <li>可以重复使用，减少代码重复</li>
            <li>可以在不同模板之间导入和使用</li>
            <li>支持默认参数和可变参数</li>
        </ul>
        
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template, users=users)


# ============================================
# 自定义过滤器 (Custom Filters)
# ============================================

@app.template_filter('reverse_words')
def reverse_words(text):
    """自定义过滤器：反转单词顺序"""
    return ' '.join(reversed(text.split()))


@app.route('/custom-filters')
def custom_filters():
    """演示自定义过滤器"""
    text = "Hello Flask Template System"
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>自定义过滤器</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>自定义过滤器 (Custom Filters)</h1>
        <p>原文: {{ text }}</p>
        <p>反转单词: {{ text | reverse_words }}</p>
        <p><a href="/">返回首页</a></p>
    </body>
    </html>
    '''
    return render_template_string(template, text=text)


if __name__ == '__main__':
    print("🚀 Starting Flask Template Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)
