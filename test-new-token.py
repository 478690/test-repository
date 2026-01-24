#!/usr/bin/env python3
import urllib.request
import json

def test_new_token():
    api_token = '63lOCOxo7FqbBL6rvRMUb0LnaVwS5_lrODi-vn2c'
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    model = '@cf/meta/llama-3-8b-instruct'
    
    print("=" * 70)
    print("Testing New Workers AI API Token")
    print("=" * 70)
    print()
    
    print("Configuration:")
    print(f"  Account ID: {account_id}")
    print(f"  Model: {model}")
    print(f"  Token: {api_token[:20]}...")
    print()
    
    api_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}'
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
    
    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(api_data).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}'
            }
        )
        
        print("Sending request...")
        with urllib.request.urlopen(req) as response:
            print(f"✅ Response Status: {response.status} {response.reason}")
            print()
            
            response_data = json.loads(response.read().decode('utf-8'))
            
            if 'result' in response_data and 'response' in response_data['result']:
                ai_response = response_data['result']['response']
                print(f"✅ AI Response: {ai_response}")
                print()
                print("=" * 70)
                print("✅ New API Token is working correctly!")
                print("=" * 70)
                return True
            else:
                print("❌ Unexpected response format")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
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
        print("❌ API Token Test Failed")
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
    success = test_new_token()
    
    if success:
        print()
        print("Next Steps:")
        print("1. Deploy the application")
        print("2. Test the deployed app")
        print("3. All AI models should work correctly")
    else:
        print()
        print("Troubleshooting:")
        print("1. Check if the token is correct")
        print("2. Verify account ID")
        print("3. Ensure Workers AI is enabled")