#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.request
import os

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="..", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                message = data.get('message', '')
                model = data.get('model', '@cf/meta/llama-3-8b-instruct')
                history = data.get('history', [])
                
                if not message:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'error': 'Invalid message'})
                    self.wfile.write(response.encode('utf-8'))
                    return

                print(f"Received message: {message}")
                print(f"Model: {model}")
                print(f"History length: {len(history)}")
                print("Calling Cloudflare AI API...")
                
                api_url = f'https://api.cloudflare.com/client/v4/accounts/30fdf13d5bb71a81bc6f7c732f244a72/ai/run/{model}'
                
                messages = [
                    {
                        'role': 'system',
                        'content': '你是一个友好的 AI 助手，使用中文回答用户的问题。你可以使用 Markdown 格式来组织回答，包括代码块、列表等。'
                    }
                ]
                
                for msg in history:
                    if msg.get('role') in ['user', 'assistant']:
                        messages.append({
                            'role': msg['role'],
                            'content': msg['content']
                        })
                
                messages.append({
                    'role': 'user',
                    'content': message
                })
                
                api_data = {
                    'messages': messages,
                    'max_tokens': 2048,
                    'temperature': 0.7
                }
                
                req = urllib.request.Request(
                    api_url,
                    data=json.dumps(api_data).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer fbRWRPmxK-zJyg9QfhCP-JZBar8ZjSjKuMBkvYFP'
                    }
                )
                
                try:
                    with urllib.request.urlopen(req) as response:
                        response_data = json.loads(response.read().decode('utf-8'))
                        ai_response = response_data.get('result', {}).get('response', '')
                        
                        print(f"AI Response: {ai_response[:100]}...")
                        
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        response = json.dumps({'response': ai_response.strip()})
                        self.wfile.write(response.encode('utf-8'))
                        
                except Exception as e:
                    print(f"API Error: {str(e)}")
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = json.dumps({'error': f'AI processing failed: {str(e)}'})
                    self.wfile.write(response.encode('utf-8'))
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': f'Server error: {str(e)}'})
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'Not found'})
            self.wfile.write(response.encode('utf-8'))

if __name__ == '__main__':
    PORT = 8000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print(f"Open http://localhost:{PORT} in your browser")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
