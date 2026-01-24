#!/usr/bin/env python3
import urllib.request
import json
import sys

def test_ai_gateway_with_token():
    ai_gateway_token = 'jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI'
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    model = '@cf/meta/llama-3-8b-instruct'
    
    print("=" * 70)
    print("AI Gateway Configuration Test")
    print("=" * 70)
    print()
    
    print("Step 1: Testing AI Gateway URL Format")
    print("-" * 70)
    
    test_urls = [
        f'https://gateway.ai.cloudflare.com/v1/{account_id}/ai/run/{model}',
        f'https://gateway.ai.cloudflare.com/v1/{account_id}/workers-ai/{model}',
        f'https://gateway.ai.cloudflare.com/v1/{account_id}/{model}'
    ]
    
    for i, url in enumerate(test_urls, 1):
        print(f"\nTest {i}: {url}")
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps({
                    'messages': [{'role': 'user', 'content': 'test'}],
                    'max_tokens': 10
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {ai_gateway_token}'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"  ✅ Status: {response.status}")
                if response.status == 200:
                    print(f"  🎉 This URL format works!")
                    print()
                    print("=" * 70)
                    print("✅ AI Gateway Configuration Successful!")
                    print("=" * 70)
                    print()
                    print("Working URL:", url)
                    print()
                    print("Next Steps:")
                    print("1. Update application to use this URL format")
                    print("2. Deploy application")
                    print("3. Test with real requests")
                    return url
        except urllib.error.HTTPError as e:
            print(f"  ❌ Status: {e.code} - {e.reason}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print()
    print("=" * 70)
    print("❌ All URL formats failed")
    print("=" * 70)
    print()
    print("This means AI Gateway needs to be configured in Cloudflare Dashboard.")
    print()
    print("Required Actions:")
    print("1. Visit: https://dash.cloudflare.com/30fdf13d5bb71a81bc6f7c732f244a72/ai-gateway")
    print("2. Create AI Gateway")
    print("3. Configure routes")
    print("4. Get the correct URL format from dashboard")
    print()
    return None

if __name__ == '__main__':
    result = test_ai_gateway_with_token()
    
    if result:
        print("\n✅ AI Gateway is ready to use!")
        print(f"URL: {result}")
    else:
        print("\n❌ AI Gateway requires manual configuration in dashboard")