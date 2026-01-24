#!/usr/bin/env python3
import urllib.request
import json

def test_ai_gateway_detailed():
    ai_gateway_token = 'jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI'
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    model = '@cf/meta/llama-3-8b-instruct'
    
    print("=" * 70)
    print("AI Gateway Detailed Diagnostic")
    print("=" * 70)
    print()
    
    print("Configuration:")
    print(f"  Account ID: {account_id}")
    print(f"  Model: {model}")
    print(f"  Token: {ai_gateway_token[:20]}...")
    print()
    
    api_url = f'https://gateway.ai.cloudflare.com/v1/{account_id}/ai/run/{model}'
    print(f"Testing URL: {api_url}")
    print()
    
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
    
    print("Request Data:")
    print(json.dumps(api_data, indent=2, ensure_ascii=False))
    print()
    
    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(api_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ai_gateway_token}'
            }
        )
        
        print("Sending request...")
        with urllib.request.urlopen(req) as response:
            print(f"✅ Response Status: {response.status} {response.reason}")
            print()
            
            response_data = json.loads(response.read().decode('utf-8'))
            print("Response Data:")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            print()
            
            if 'result' in response_data and 'response' in response_data['result']:
                print(f"✅ AI Response: {response_data['result']['response']}")
                print()
                print("=" * 70)
                print("✅ AI Gateway is working correctly!")
                print("=" * 70)
                return True
            else:
                print("❌ Unexpected response format")
                return False
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error: {e.code} - {e.reason}")
        print()
        
        try:
            error_body = json.loads(e.read().decode('utf-8'))
            print("Error Details:")
            print(json.dumps(error_body, indent=2, ensure_ascii=False))
        except:
            error_body = e.read().decode('utf-8')
            print(f"Error Body: {error_body}")
        
        print()
        print("=" * 70)
        print("❌ AI Gateway Configuration Issues")
        print("=" * 70)
        print()
        print("Possible causes:")
        print("1. AI Gateway is not created in Cloudflare dashboard")
        print("2. Route is not configured for this model")
        print("3. Token does not have correct permissions")
        print("4. Account ID is incorrect")
        print()
        print("Required Actions:")
        print("1. Visit: https://dash.cloudflare.com/30fdf13d5bb71a81bc6f7c732f244a72/ai-gateway")
        print("2. Create AI Gateway (if not exists)")
        print("3. Configure route for model: " + model)
        print("4. Verify token permissions")
        print()
        print("=" * 70)
        return False
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("=" * 70)
        print("❌ Unexpected Error")
        print("=" * 70)
        return False

if __name__ == '__main__':
    test_ai_gateway_detailed()