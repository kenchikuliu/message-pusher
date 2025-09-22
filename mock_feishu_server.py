#!/usr/bin/env python3
"""
模拟飞书webhook服务器
用于测试Claude Code集成功能
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class MockFeishuHandler(BaseHTTPRequestHandler):
    """模拟飞书webhook处理器"""

    def do_POST(self):
        """处理POST请求（飞书webhook）"""
        try:
            # 读取请求内容
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            # 解析JSON数据
            try:
                data = json.loads(post_data.decode('utf-8'))
                print(f"\n[MOCK FEISHU] 收到webhook消息:")
                print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  内容: {json.dumps(data, ensure_ascii=False, indent=2)}")

                # 模拟飞书成功响应
                response = {"StatusCode": 0, "StatusMessage": "success"}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))

                print(f"[MOCK FEISHU] 响应: 200 OK")

            except json.JSONDecodeError:
                print(f"[MOCK FEISHU] 无效的JSON数据: {post_data}")
                self.send_response(400)
                self.end_headers()

        except Exception as e:
            print(f"[MOCK FEISHU] 处理错误: {str(e)}")
            self.send_response(500)
            self.end_headers()

    def log_message(self, format, *args):
        """禁用默认日志"""
        pass

def start_mock_server(port=8080):
    """启动模拟服务器"""
    server = HTTPServer(('localhost', port), MockFeishuHandler)
    print(f"[MOCK FEISHU] 服务器启动在 http://localhost:{port}")
    print(f"[MOCK FEISHU] 模拟飞书webhook URL: http://localhost:{port}/webhook")
    print(f"[MOCK FEISHU] 等待接收消息...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[MOCK FEISHU] 服务器停止")
        server.shutdown()

if __name__ == "__main__":
    start_mock_server()