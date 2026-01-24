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

                print("Received message: {}".format(message))
                print("Model: {}".format(model))
                print("History length: {}".format(len(history)))
                
                if model.startswith('gemini-'):
                    print("Calling Google Gemini API...")
                    ai_response = self.call_gemini_api(message, model, history)
                    provider = 'Google Gemini'
                else:
                    print("Calling Cloudflare AI API...")
                    ai_response = self.call_cloudflare_ai(message, model, history)
                    provider = 'Cloudflare Workers AI'
                
                print("AI Response: {}...".format(ai_response[:100]))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'response': ai_response, 'provider': provider})
                self.wfile.write(response.encode('utf-8'))
                        
            except Exception as e:
                print("Error: {}".format(str(e)))
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Server error: {}'.format(str(e))})
                self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'Not found'})
            self.wfile.write(response.encode('utf-8'))

    def call_cloudflare_ai(self, message, model, history):
        ai_gateway_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
        api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
        account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
        
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
        
        try:
            api_url = 'https://gateway.ai.cloudflare.com/v1/{}/ai/run/{}'.format(account_id, model)
            auth_token = ai_gateway_token
            print("Trying AI Gateway: {}".format(api_url))
            
            req = urllib.request.Request(
                api_url,
                data=json.dumps(api_data).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(auth_token)
                }
            )
            
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                print("AI Gateway success!")
                return response_data.get('result', {}).get('response', '')
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print("AI Gateway not configured (403), falling back to direct API...")
            else:
                raise
        except Exception as e:
            print("AI Gateway error: {}, falling back to direct API...".format(str(e)))
        
        api_url = 'https://api.cloudflare.com/client/v4/accounts/{}/ai/run/{}'.format(account_id, model)
        auth_token = api_token
        print("Using direct API: {}".format(api_url))
        
        req = urllib.request.Request(
            api_url,
            data=json.dumps(api_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(auth_token)
            }
        )
        
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            print("Direct API success!")
            return response_data.get('result', {}).get('response', '')

    def call_gemini_api(self, message, model, history):
        api_key = 'AIzaSyCHXQsENnN8ilwrdWqDartcHOvptRsqetA'
        
        model_map = {
            'gemini-2.5-pro': 'gemini-2.5-pro',
            'gemini-2.0-flash': 'gemini-2.0-flash',
            'gemini-1.5-pro': 'gemini-1.5-pro'
        }
        
        selected_model = model_map.get(model, 'gemini-2.0-flash')
        
        contents = [
            {
                'role': 'user',
                'parts': [
                    {
                        'text': '你是一个友好的 AI 助手，使用中文回答用户的问题。你可以使用 Markdown 格式来组织回答，包括代码块、列表等。'
                    }
                ]
            }
        ]
        
        for msg in history:
            if msg.get('role') == 'user':
                contents.append({
                    'role': 'user',
                    'parts': [{'text': msg['content']}]
                })
            elif msg.get('role') == 'assistant':
                contents.append({
                    'role': 'model',
                    'parts': [{'text': msg['content']}]
                })
        
        contents.append({
            'role': 'user',
            'parts': [{'text': message}]
        })
        
        api_url = 'https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}'.format(selected_model, api_key)
        
        req = urllib.request.Request(
            api_url,
            data=json.dumps({
                'contents': contents,
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 2048
                }
            }).encode('utf-8'),
            headers={
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            return response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

if __name__ == '__main__':
    PORT = 8000
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        print("Open http://localhost:{} in your browser".format(PORT))
        print("Press Ctrl+C to stop server")
        httpd.serve_forever()
