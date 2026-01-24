#!/usr/bin/env python3
import json
import urllib.request
import time

def get_all_models():
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
    
    api_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search?task=Text%20Generation'
    
    req = urllib.request.Request(
        api_url,
        headers={
            'Authorization': f'Bearer {api_token}'
        }
    )
    
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('success'):
            models = data.get('result', [])
            return models
        else:
            print(f"Error: {data.get('errors', [])}")
            return []

def test_model(model_id):
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
    
    try:
        start_time = time.time()
        
        messages = [
            {
                'role': 'system',
                'content': '你是一个友好的 AI 助手，使用中文回答问题。'
            },
            {
                'role': 'user',
                'content': '你好'
            }
        ]
        
        api_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_id}'
        
        req = urllib.request.Request(
            api_url,
            data=json.dumps({
                'messages': messages,
                'max_tokens': 50,
                'temperature': 0.7
            }).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            elapsed_time = time.time() - start_time
            
            if response_data.get('success'):
                result = response_data.get('result', {})
                usage = result.get('usage', {})
                
                return {
                    'success': True,
                    'response_time': elapsed_time,
                    'usage': usage
                }
            else:
                return {
                    'success': False,
                    'error': response_data.get('errors', [])
                }
                
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'error': f"HTTP {e.code}: {e.reason}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == '__main__':
    print("获取所有可用的 Workers AI 模型...")
    print("="*80)
    
    models = get_all_models()
    
    print(f"\n找到 {len(models)} 个文本生成模型\n")
    
    print("模型列表:")
    print("-"*80)
    
    for i, model in enumerate(models, 1):
        name = model.get('name', 'Unknown')
        desc = model.get('description', 'N/A')
        properties = model.get('properties', [])
        
        context_window = None
        for prop in properties:
            if prop.get('property_id') == 'context_window':
                context_window = prop.get('value')
                break
        
        print(f"{i}. {name}")
        print(f"   描述: {desc[:100]}{'...' if len(desc) > 100 else ''}")
        if context_window:
            print(f"   上下文窗口: {context_window}")
        print()
    
    print("="*80)
    print("\n开始测试模型...")
    print("="*80)
    
    tested_models = []
    
    for i, model in enumerate(models[:10], 1):  # 只测试前 10 个模型
        model_id = model.get('name')
        model_name = model.get('name')
        
        print(f"\n[{i}/{min(10, len(models))}] 测试: {model_name}")
        
        result = test_model(model_id)
        
        if result['success']:
            response_time = result['response_time']
            usage = result['usage']
            total_tokens = usage.get('total_tokens', 0)
            
            print(f"   ✅ 成功 - 响应时间: {response_time:.2f}s, Token: {total_tokens}")
            
            tested_models.append({
                'name': model_name,
                'description': model.get('description', ''),
                'context_window': context_window,
                'response_time': response_time,
                'total_tokens': total_tokens,
                'success': True
            })
        else:
            print(f"   ❌ 失败 - {result['error']}")
            
            tested_models.append({
                'name': model_name,
                'description': model.get('description', ''),
                'context_window': context_window,
                'success': False,
                'error': result['error']
            })
        
        time.sleep(0.5)
    
    print("\n" + "="*80)
    print("测试结果汇总")
    print("="*80)
    
    successful = [m for m in tested_models if m['success']]
    failed = [m for m in tested_models if not m['success']]
    
    print(f"\n✅ 成功的模型 ({len(successful)}):")
    for model in successful:
        print(f"   - {model['name']} ({model['response_time']:.2f}s, {model['total_tokens']} tokens)")
    
    print(f"\n❌ 失败的模型 ({len(failed)}):")
    for model in failed:
        print(f"   - {model['name']} ({model['error']})")
    
    print("\n" + "="*80)
    print(f"总计: {len(successful)}/{len(tested_models)} 个模型测试成功")
    print("="*80)
    
    print("\n推荐的模型（按响应时间排序）:")
    print("-"*80)
    
    sorted_models = sorted(successful, key=lambda x: x['response_time'])
    for i, model in enumerate(sorted_models[:5], 1):
        print(f"{i}. {model['name']}")
        print(f"   响应时间: {model['response_time']:.2f}s")
        print(f"   Token 使用: {model['total_tokens']}")
        print(f"   描述: {model['description'][:80]}{'...' if len(model['description']) > 80 else ''}")
        print()