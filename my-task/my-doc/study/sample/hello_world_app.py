"""
简单的Python Flask Hello World应用
用于演示Docker容器化部署
"""

from flask import Flask, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    """主页路由"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'''
    <html>
        <head>
            <title>Python Docker Hello World</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; }}
                .info {{ background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .time {{ color: #666; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐳 Hello, Docker World!</h1>
                <p>这是一个运行在Docker容器中的Python Flask应用。</p>
                
                <div class="info">
                    <h3>应用信息：</h3>
                    <ul>
                        <li><strong>Python版本：</strong> 3.10</li>
                        <li><strong>Web框架：</strong> Flask</li>
                        <li><strong>容器化：</strong> Docker</li>
                        <li><strong>当前时间：</strong> <span class="time">{current_time}</span></li>
                    </ul>
                </div>
                
                <p>
                    <a href="/health">健康检查</a> | 
                    <a href="/info">系统信息</a>
                </p>
            </div>
        </body>
    </html>
    '''

@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'message': 'Hello World应用运行正常',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/info')
def system_info():
    """系统信息端点"""
    return jsonify({
        'python_version': '3.10',
        'framework': 'Flask',
        'container': 'Docker',
        'environment': os.environ.get('FLASK_ENV', 'development'),
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'port': 8080
    })

if __name__ == '__main__':
    print("🚀 启动Hello World应用...")
    print("📍 访问地址: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)