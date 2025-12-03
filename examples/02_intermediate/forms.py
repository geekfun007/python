"""
Flask 进阶示例 1: 表单处理和验证
Flask Intermediate Example 1: Form Handling and Validation

演示使用 WTForms 进行表单处理和验证。
Demonstrates form handling and validation using WTForms.
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# 模拟数据库
users_db = []
posts_db = []


# ============================================
# 表单验证辅助函数
# ============================================

def validate_email(email):
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """验证密码强度"""
    if len(password) < 8:
        return False, "密码至少需要8个字符"
    if not re.search(r'[A-Z]', password):
        return False, "密码需要包含至少一个大写字母"
    if not re.search(r'[a-z]', password):
        return False, "密码需要包含至少一个小写字母"
    if not re.search(r'[0-9]', password):
        return False, "密码需要包含至少一个数字"
    return True, "密码强度合格"


# ============================================
# 主页
# ============================================

@app.route('/')
def index():
    """主页 - 显示所有表单示例"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask 表单示例</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .form-link {
                display: block;
                padding: 15px;
                margin: 10px 0;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .form-link:hover {
                background: #2980b9;
            }
            .flash-message {
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 Flask 表单处理示例</h1>
            <h2>Form Handling Examples</h2>
            
            {% with messages = get_flashed_messages() %}
                {% if messages %}
                    {% for message in messages %}
                    <div class="flash-message">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <a href="/register" class="form-link">👤 用户注册表单 (Registration Form)</a>
            <a href="/contact" class="form-link">📧 联系表单 (Contact Form)</a>
            <a href="/survey" class="form-link">📊 调查问卷 (Survey Form)</a>
            <a href="/users" class="form-link">📋 查看注册用户 (View Users)</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 用户注册表单
# ============================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        agree_terms = request.form.get('agree_terms')
        
        errors = []
        
        # 验证用户名
        if not username:
            errors.append('用户名不能为空')
        elif len(username) < 3:
            errors.append('用户名至少需要3个字符')
        elif any(user['username'] == username for user in users_db):
            errors.append('用户名已存在')
        
        # 验证邮箱
        if not email:
            errors.append('邮箱不能为空')
        elif not validate_email(email):
            errors.append('邮箱格式不正确')
        elif any(user['email'] == email for user in users_db):
            errors.append('邮箱已被注册')
        
        # 验证密码
        if not password:
            errors.append('密码不能为空')
        else:
            is_valid, msg = validate_password(password)
            if not is_valid:
                errors.append(msg)
        
        # 验证确认密码
        if password != confirm_password:
            errors.append('两次输入的密码不一致')
        
        # 验证协议
        if not agree_terms:
            errors.append('请同意用户协议')
        
        if errors:
            error_html = '<br>'.join(errors)
            flash(f'注册失败：<br>{error_html}', 'error')
        else:
            # 保存用户
            user = {
                'id': len(users_db) + 1,
                'username': username,
                'email': email,
                'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            users_db.append(user)
            flash(f'✅ 注册成功！欢迎 {username}', 'success')
            return redirect(url_for('users'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户注册</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"],
            input[type="email"],
            input[type="password"] {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
            }
            input[type="text"]:focus,
            input[type="email"]:focus,
            input[type="password"]:focus {
                outline: none;
                border-color: #3498db;
            }
            .checkbox-group {
                display: flex;
                align-items: center;
            }
            .checkbox-group input {
                margin-right: 10px;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #2980b9;
            }
            .flash {
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
            .flash.error {
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
            .flash.success {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
            .password-strength {
                margin-top: 5px;
                font-size: 12px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>👤 用户注册</h1>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message | safe }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="username">用户名 *</label>
                    <input type="text" id="username" name="username" required 
                           placeholder="至少3个字符" value="{{ request.form.get('username', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱 *</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="your@email.com" value="{{ request.form.get('email', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="password">密码 *</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="至少8个字符，包含大小写字母和数字">
                    <div class="password-strength">
                        密码要求：至少8个字符，包含大小写字母和数字
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">确认密码 *</label>
                    <input type="password" id="confirm_password" name="confirm_password" required 
                           placeholder="再次输入密码">
                </div>
                
                <div class="form-group checkbox-group">
                    <input type="checkbox" id="agree_terms" name="agree_terms" required>
                    <label for="agree_terms" style="font-weight: normal;">
                        我同意用户协议和隐私政策 *
                    </label>
                </div>
                
                <button type="submit">注册</button>
            </form>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 联系表单
# ============================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """联系表单"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        errors = []
        
        if not name:
            errors.append('姓名不能为空')
        if not email:
            errors.append('邮箱不能为空')
        elif not validate_email(email):
            errors.append('邮箱格式不正确')
        if not subject:
            errors.append('主题不能为空')
        if not message:
            errors.append('消息不能为空')
        elif len(message) < 10:
            errors.append('消息至少需要10个字符')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            flash(f'✅ 感谢您的消息，{name}！我们会尽快回复您。', 'success')
            # 这里可以发送邮件或保存到数据库
            return redirect(url_for('index'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>联系我们</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }
            input[type="text"],
            input[type="email"],
            select,
            textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-size: 14px;
                font-family: Arial, sans-serif;
            }
            textarea {
                resize: vertical;
                min-height: 120px;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background: #229954;
            }
            .flash {
                padding: 15px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
            .flash.error {
                background: #f8d7da;
                color: #721c24;
            }
            .flash.success {
                background: #d4edda;
                color: #155724;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>📧 联系我们</h1>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST">
                <div class="form-group">
                    <label for="name">姓名 *</label>
                    <input type="text" id="name" name="name" required 
                           value="{{ request.form.get('name', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱 *</label>
                    <input type="email" id="email" name="email" required 
                           value="{{ request.form.get('email', '') }}">
                </div>
                
                <div class="form-group">
                    <label for="subject">主题 *</label>
                    <select id="subject" name="subject" required>
                        <option value="">请选择...</option>
                        <option value="general">一般咨询</option>
                        <option value="support">技术支持</option>
                        <option value="feedback">反馈建议</option>
                        <option value="other">其他</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="message">消息 *</label>
                    <textarea id="message" name="message" required 
                              placeholder="请输入您的消息...">{{ request.form.get('message', '') }}</textarea>
                </div>
                
                <button type="submit">📤 发送消息</button>
            </form>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


# ============================================
# 调查问卷
# ============================================

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    """调查问卷表单"""
    if request.method == 'POST':
        # 获取表单数据
        age_group = request.form.get('age_group')
        experience = request.form.get('experience')
        skills = request.form.getlist('skills')  # 多选框
        rating = request.form.get('rating')
        comments = request.form.get('comments', '').strip()
        
        # 保存到 session
        session['survey'] = {
            'age_group': age_group,
            'experience': experience,
            'skills': skills,
            'rating': rating,
            'comments': comments,
            'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        flash('✅ 感谢您完成调查问卷！', 'success')
        return redirect(url_for('survey_result'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>调查问卷</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .form-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .form-group {
                margin-bottom: 25px;
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                color: #555;
            }
            .radio-group, .checkbox-group {
                margin-left: 10px;
            }
            .radio-group label, .checkbox-group label {
                font-weight: normal;
                margin: 8px 0;
                display: flex;
                align-items: center;
            }
            input[type="radio"], input[type="checkbox"] {
                margin-right: 10px;
            }
            select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
                resize: vertical;
            }
            button {
                width: 100%;
                padding: 12px;
                background: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background: #8e44ad;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>📊 开发者调查问卷</h1>
            <p>请花几分钟时间完成这份问卷</p>
            
            <form method="POST">
                <div class="form-group">
                    <label>年龄段 *</label>
                    <select name="age_group" required>
                        <option value="">请选择...</option>
                        <option value="18-25">18-25</option>
                        <option value="26-35">26-35</option>
                        <option value="36-45">36-45</option>
                        <option value="46+">46+</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>编程经验 *</label>
                    <div class="radio-group">
                        <label><input type="radio" name="experience" value="beginner" required> 初学者 (< 1年)</label>
                        <label><input type="radio" name="experience" value="intermediate"> 中级 (1-3年)</label>
                        <label><input type="radio" name="experience" value="advanced"> 高级 (3-5年)</label>
                        <label><input type="radio" name="experience" value="expert"> 专家 (5年以上)</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>掌握的技能 (可多选) *</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" name="skills" value="python"> Python</label>
                        <label><input type="checkbox" name="skills" value="flask"> Flask</label>
                        <label><input type="checkbox" name="skills" value="django"> Django</label>
                        <label><input type="checkbox" name="skills" value="javascript"> JavaScript</label>
                        <label><input type="checkbox" name="skills" value="react"> React</label>
                        <label><input type="checkbox" name="skills" value="sql"> SQL</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>对 Flask 的评分 *</label>
                    <div class="radio-group">
                        <label><input type="radio" name="rating" value="5" required> ⭐⭐⭐⭐⭐ 非常好</label>
                        <label><input type="radio" name="rating" value="4"> ⭐⭐⭐⭐ 很好</label>
                        <label><input type="radio" name="rating" value="3"> ⭐⭐⭐ 一般</label>
                        <label><input type="radio" name="rating" value="2"> ⭐⭐ 需要改进</label>
                        <label><input type="radio" name="rating" value="1"> ⭐ 不满意</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>其他意见或建议</label>
                    <textarea name="comments" rows="5" placeholder="请输入您的意见..."></textarea>
                </div>
                
                <button type="submit">📤 提交问卷</button>
            </form>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template)


@app.route('/survey/result')
def survey_result():
    """显示调查结果"""
    survey_data = session.get('survey', {})
    
    if not survey_data:
        flash('请先完成调查问卷', 'error')
        return redirect(url_for('survey'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>问卷结果</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 700px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .result-container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .result-item {
                margin: 15px 0;
                padding: 15px;
                background: #f8f9fa;
                border-left: 4px solid #9b59b6;
                border-radius: 5px;
            }
            .result-item strong {
                color: #555;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div class="result-container">
            <h1>✅ 问卷提交成功！</h1>
            <p>感谢您的参与。以下是您提交的信息：</p>
            
            <div class="result-item">
                <strong>年龄段:</strong> {{ survey.age_group }}
            </div>
            
            <div class="result-item">
                <strong>编程经验:</strong> {{ survey.experience }}
            </div>
            
            <div class="result-item">
                <strong>掌握的技能:</strong> {{ survey.skills | join(', ') }}
            </div>
            
            <div class="result-item">
                <strong>评分:</strong> {{ '⭐' * survey.rating|int }}
            </div>
            
            {% if survey.comments %}
            <div class="result-item">
                <strong>意见建议:</strong><br>
                {{ survey.comments }}
            </div>
            {% endif %}
            
            <div class="result-item">
                <strong>提交时间:</strong> {{ survey.submitted_at }}
            </div>
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, survey=survey_data)


# ============================================
# 查看用户列表
# ============================================

@app.route('/users')
def users():
    """显示所有注册用户"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户列表</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #3498db;
                color: white;
            }
            tr:hover {
                background: #f5f5f5;
            }
            .empty-state {
                text-align: center;
                padding: 40px;
                color: #999;
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #3498db;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📋 注册用户列表</h1>
            
            {% if users %}
            <p>共有 {{ users | length }} 位注册用户</p>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户名</th>
                        <th>邮箱</th>
                        <th>注册时间</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.registered_at }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                <h2>📭 暂无注册用户</h2>
                <p>请先<a href="/register">注册</a>一个账户</p>
            </div>
            {% endif %}
            
            <a href="/" class="back-link">← 返回首页</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(template, users=users_db)


if __name__ == '__main__':
    print("🚀 Starting Flask Forms Example...")
    print("📍 访问 http://127.0.0.1:5000/")
    print("\n提示：在生产环境中，请使用 WTForms 库进行表单处理")
    print("安装: pip install Flask-WTF")
    app.run(debug=True, host='0.0.0.0', port=5000)
