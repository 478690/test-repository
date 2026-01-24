#!/usr/bin/env python3
import json
import urllib.request
import time

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
                    'usage': usage,
                    'response': result.get('response', '')
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
    print("测试更多 Workers AI 模型...")
    print("="*80)
    
    models_to_test = [
        '@cf/google/gemma-3-12b-it',
        '@cf/qwen/qwq-32b',
        '@cf/meta/llama-3.2-11b-vision-instruct',
        '@cf/defog/sqlcoder-7b-2',
        '@cf/microsoft/phi-2',
        '@cf/qwen/qwen1.5-14b-chat-awq',
        '@cf/openchat/openchat-3.5-0106',
        '@cf/meta/llama-4-scout-17b-16e-instruct',
        '@cf/hf/google/gemma-7b-it',
    ]
    
    tested_models = []
    
    for i, model_id in enumerate(models_to_test, 1):
        print(f"\n[{i}/{len(models_to_test)}] 测试: {model_id}")
        
        result = test_model(model_id)
        
        if result['success']:
            response_time = result['response_time']
            usage = result['usage']
            total_tokens = usage.get('total_tokens', 0)
            
            print(f"   ✅ 成功 - 响应时间: {response_time:.2f}s, Token: {total_tokens}")
            
            tested_models.append({
                'id': model_id,
                'success': True,
                'response_time': response_time,
                'total_tokens': total_tokens
            })
        else:
            print(f"   ❌ 失败 - {result['error']}")
            
            tested_models.append({
                'id': model_id,
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
        print(f"   - {model['id']} ({model['response_time']:.2f}s, {model['total_tokens']} tokens)")
    
    print(f"\n❌ 失败的模型 ({len(failed)}):")
    for model in failed:
        print(f"   - {model['id']} ({model['error']})")
    
    print("\n" + "="*80)
    print(f"总计: {len(successful)}/{len(tested_models)} 个模型测试成功")
    print("="*80)
    
    print("\n推荐的模型（按响应时间排序）:")
    print("-"*80)
    
    sorted_models = sorted(successful, key=lambda x: x['response_time'])
    for i, model in enumerate(sorted_models, 1):
        print(f"{i}. {model['id']}")
        print(f"   响应时间: {model['response_time']:.2f}s")
        print(f"   Token 使用: {model['total_tokens']}")
        print()