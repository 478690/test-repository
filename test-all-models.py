#!/usr/bin/env python3
import json
import urllib.request
import time

class ModelTester:
    def __init__(self):
        self.account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
        self.api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
        self.google_api_key = 'AIzaSyCHXQsENnN8ilwrdWqDartcHOvptRsqetA'
        
        self.cloudflare_models = [
            '@cf/meta/llama-3-8b-instruct',
            '@cf/meta/llama-3-70b-instruct',
            '@cf/mistral/mistral-7b-instruct-v0.2'
        ]
        
        self.gemini_models = [
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-1.5-pro'
        ]
        
        self.test_message = "你好，请用一句话介绍你自己。"
    
    def test_cloudflare_model(self, model):
        print(f"\n{'='*60}")
        print(f"测试模型: {model}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            
            messages = [
                {
                    'role': 'system',
                    'content': '你是一个友好的 AI 助手，使用中文回答问题。'
                },
                {
                    'role': 'user',
                    'content': self.test_message
                }
            ]
            
            api_url = f'https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{model}'
            
            req = urllib.request.Request(
                api_url,
                data=json.dumps({
                    'messages': messages,
                    'max_tokens': 100,
                    'temperature': 0.7
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_token}'
                }
            )
            
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                elapsed_time = time.time() - start_time
                
                if response_data.get('success'):
                    result = response_data.get('result', {})
                    ai_response = result.get('response', '')
                    usage = result.get('usage', {})
                    
                    print(f"✅ 状态: 成功")
                    print(f"⏱️  响应时间: {elapsed_time:.2f} 秒")
                    print(f"📊 Token 使用:")
                    print(f"   - 输入: {usage.get('prompt_tokens', 0)}")
                    print(f"   - 输出: {usage.get('completion_tokens', 0)}")
                    print(f"   - 总计: {usage.get('total_tokens', 0)}")
                    print(f"\n💬 AI 回复:")
                    print(f"   {ai_response[:200]}{'...' if len(ai_response) > 200 else ''}")
                    
                    return {
                        'model': model,
                        'success': True,
                        'response_time': elapsed_time,
                        'usage': usage,
                        'response': ai_response
                    }
                else:
                    print(f"❌ 状态: 失败")
                    print(f"错误: {response_data.get('errors', [])}")
                    return {
                        'model': model,
                        'success': False,
                        'error': response_data.get('errors', [])
                    }
                    
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP 错误: {e.code} - {e.reason}")
            return {
                'model': model,
                'success': False,
                'error': f"HTTP {e.code}: {e.reason}"
            }
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return {
                'model': model,
                'success': False,
                'error': str(e)
            }
    
    def test_gemini_model(self, model):
        print(f"\n{'='*60}")
        print(f"测试模型: {model}")
        print(f"{'='*60}")
        
        try:
            start_time = time.time()
            
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
                            'text': '你是一个友好的 AI 助手，使用中文回答问题。'
                        }
                    ]
                },
                {
                    'role': 'user',
                    'parts': [
                        {
                            'text': self.test_message
                        }
                    ]
                }
            ]
            
            api_url = f'https://generativelanguage.googleapis.com/v1beta/models/{selected_model}:generateContent?key={self.google_api_key}'
            
            req = urllib.request.Request(
                api_url,
                data=json.dumps({
                    'contents': contents,
                    'generationConfig': {
                        'temperature': 0.7,
                        'maxOutputTokens': 100
                    }
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                elapsed_time = time.time() - start_time
                
                if 'candidates' in response_data and len(response_data['candidates']) > 0:
                    candidate = response_data['candidates'][0]
                    ai_response = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
                    usage_metadata = response_data.get('usageMetadata', {})
                    
                    print(f"✅ 状态: 成功")
                    print(f"⏱️  响应时间: {elapsed_time:.2f} 秒")
                    print(f"📊 Token 使用:")
                    print(f"   - 输入: {usage_metadata.get('promptTokenCount', 0)}")
                    print(f"   - 输出: {usage_metadata.get('candidatesTokenCount', 0)}")
                    print(f"   - 总计: {usage_metadata.get('totalTokenCount', 0)}")
                    print(f"\n💬 AI 回复:")
                    print(f"   {ai_response[:200]}{'...' if len(ai_response) > 200 else ''}")
                    
                    return {
                        'model': model,
                        'success': True,
                        'response_time': elapsed_time,
                        'usage': usage_metadata,
                        'response': ai_response
                    }
                else:
                    print(f"❌ 状态: 失败")
                    print(f"错误: {response_data}")
                    return {
                        'model': model,
                        'success': False,
                        'error': response_data
                    }
                    
        except urllib.error.HTTPError as e:
            print(f"❌ HTTP 错误: {e.code} - {e.reason}")
            return {
                'model': model,
                'success': False,
                'error': f"HTTP {e.code}: {e.reason}"
            }
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return {
                'model': model,
                'success': False,
                'error': str(e)
            }
    
    def test_all_models(self):
        print("\n" + "="*60)
        print("开始测试所有模型")
        print("="*60)
        
        results = {
            'cloudflare': [],
            'gemini': []
        }
        
        print("\n📡 测试 Cloudflare Workers AI 模型")
        print("="*60)
        
        for model in self.cloudflare_models:
            result = self.test_cloudflare_model(model)
            results['cloudflare'].append(result)
            time.sleep(1)
        
        print("\n\n🤖 测试 Google Gemini 模型")
        print("="*60)
        
        for model in self.gemini_models:
            result = self.test_gemini_model(model)
            results['gemini'].append(result)
            time.sleep(1)
        
        self.print_summary(results)
        
        return results
    
    def print_summary(self, results):
        print("\n\n" + "="*60)
        print("测试结果汇总")
        print("="*60)
        
        print("\n📡 Cloudflare Workers AI 模型:")
        print("-"*60)
        for result in results['cloudflare']:
            status = "✅ 成功" if result['success'] else "❌ 失败"
            print(f"{result['model']}: {status}")
            if result['success']:
                print(f"   响应时间: {result['response_time']:.2f} 秒")
                print(f"   Token 使用: {result['usage'].get('total_tokens', 0)}")
            else:
                print(f"   错误: {result['error']}")
        
        print("\n🤖 Google Gemini 模型:")
        print("-"*60)
        for result in results['gemini']:
            status = "✅ 成功" if result['success'] else "❌ 失败"
            print(f"{result['model']}: {status}")
            if result['success']:
                print(f"   响应时间: {result['response_time']:.2f} 秒")
                print(f"   Token 使用: {result['usage'].get('totalTokenCount', 0)}")
            else:
                print(f"   错误: {result['error']}")
        
        print("\n" + "="*60)
        
        successful_count = sum(1 for r in results['cloudflare'] + results['gemini'] if r['success'])
        total_count = len(results['cloudflare']) + len(results['gemini'])
        
        print(f"总计: {successful_count}/{total_count} 个模型测试成功")
        print("="*60)

if __name__ == '__main__':
    tester = ModelTester()
    results = tester.test_all_models()
    
    print("\n\n✅ 测试完成！")