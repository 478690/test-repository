#!/usr/bin/env python3
import urllib.request
import json

def test_ai_gateway():
    ai_gateway_token = 'jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI'
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    model = '@cf/meta/llama-3-8b-instruct'
    
    api_url = f'https://gateway.ai.cloudflare.com/v1/{account_id}/ai/run/{model}'
    
    messages = [
        {
            'role': 'system',
            'content': '你是一个友好的 AI 助手，使用中文回答用户的问题。'
        },
        {
            'role': 'user',
            'content': '你好，请用一句话介绍你自己。'
        }
    ]
    
    api_data = {
        'messages': messages,
        'max_tokens': 100,
        'temperature': 0.7
    }
    
    print(f"Testing AI Gateway...")
    print(f"URL: {api_url}")
    print(f"Model: {model}")
    
    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(api_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ai_gateway_token}'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            print(f"\n✅ Success!")
            print(f"Response: {response_data.get('result', {}).get('response', '')}")
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.code} - {e.reason}")
        print(f"This might mean:")
        print("1. AI Gateway is not properly configured in Cloudflare dashboard")
        print("2. The token does not have correct permissions")
        print("3. The route is not set up correctly")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Cloudflare AI Gateway Configuration Test")
    print("=" * 60)
    print()
    
    success = test_ai_gateway()
    
    print()
    print("=" * 60)
    if success:
        print("✅ AI Gateway is working correctly!")
        print("You can now use it in your application.")
    else:
        print("❌ AI Gateway configuration needs attention.")
        print("Please check the Cloudflare dashboard and follow the configuration steps.")
    print("=" * 60)