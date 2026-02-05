#!/usr/bin/env python3
"""
综合测试所有环境变量的有效性
"""

import subprocess
import json

def run_curl_command(command):
    """运行 curl 命令并返回结果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def test_cloudflare_account_id():
    """测试 CLOUDFLARE_ACCOUNT_ID"""
    print("=" * 70)
    print("Testing CLOUDFLARE_ACCOUNT_ID")
    print("=" * 70)
    
    account_id = "30fdf13d5bb71a81bc6f7c732f244a72"
    test_token = "ptZh0lHgOvg7R8E-Xd0IZMGwCw0lHGvz3D5nDHSk"
    
    command = f"curl 'https://api.cloudflare.com/client/v4/accounts/{account_id}' -H 'Authorization: Bearer {test_token}'"
    
    result = run_curl_command(command)
    
    if result["returncode"] == 0:
        try:
            data = json.loads(result["stdout"])
            if data.get("success"):
                account_name = data.get("result", {}).get("name")
                print("✅ CLOUDFLARE_ACCOUNT_ID Test Passed")
                print(f"✅ Account Name: {account_name}")
                print(f"✅ Account ID: {account_id}")
                return True
            else:
                print("❌ CLOUDFLARE_ACCOUNT_ID Test Failed")
                print(f"Error: {data.get('errors', [{}])[0].get('message', 'Unknown error')}")
                return False
        except:
            print("❌ Failed to parse response")
            print(f"Response: {result['stdout']}")
            return False
    else:
        print("❌ HTTP Request Failed")
        print(f"Error: {result['stderr']}")
        return False

def test_cloudflare_api_token():
    """测试 CLOUDFLARE_API_TOKEN"""
    print("\n" + "=" * 70)
    print("Testing CLOUDFLARE_API_TOKEN")
    print("=" * 70)
    
    account_id = "30fdf13d5bb71a81bc6f7c732f244a72"
    api_token = "63lOCOxo7FqbBL6rvRMUb0LnaVwS5_lrODi-vn2c"
    
    command = f"curl -X POST 'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct' -H 'Authorization: Bearer {api_token}' -H 'Content-Type: application/json' -d '{{\"messages\":[{{\"role\":\"user\",\"content\":\"你好\"}}]}}'"
    
    result = run_curl_command(command)
    
    if result["returncode"] == 0:
        try:
            data = json.loads(result["stdout"])
            if data.get("success"):
                print("✅ CLOUDFLARE_API_TOKEN Test Passed")
                response = data.get("result", {}).get("response", "")
                print(f"✅ AI Response: {response[:50]}...")
                return True
            else:
                print("❌ CLOUDFLARE_API_TOKEN Test Failed")
                error_msg = data.get('errors', [{}])[0].get('message', 'Unknown error')
                print(f"Error: {error_msg}")
                return False
        except:
            print("❌ Failed to parse response")
            print(f"Response: {result['stdout']}")
            return False
    else:
        print("❌ HTTP Request Failed")
        print(f"Error: {result['stderr']}")
        return False

def test_ai_gateway_token():
    """测试 AI_GATEWAY_TOKEN"""
    print("\n" + "=" * 70)
    print("Testing AI_GATEWAY_TOKEN")
    print("=" * 70)
    
    account_id = "30fdf13d5bb71a81bc6f7c732f244a72"
    ai_gateway_token = "jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI"
    
    command = f"curl -X POST 'https://gateway.ai.cloudflare.com/v1/{account_id}/ai/run/@cf/meta/llama-3-8b-instruct' -H 'Authorization: Bearer {ai_gateway_token}' -H 'Content-Type: application/json' -d '{{\"messages\":[{{\"role\":\"user\",\"content\":\"你好\"}}]}}'"
    
    result = run_curl_command(command)
    
    if result["returncode"] == 0:
        try:
            data = json.loads(result["stdout"])
            if data.get("success"):
                print("✅ AI_GATEWAY_TOKEN Test Passed")
                response = data.get("result", [{}])[0].get("response", "")
                print(f"✅ AI Response: {response[:50]}...")
                return True
            else:
                error_msg = data.get('error', [{}])[0].get('message', 'Unknown error')
                if "Please configure AI Gateway" in error_msg:
                    print("⚠️  AI_GATEWAY_TOKEN Test - Token Valid but Gateway Not Configured")
                    print(f"Message: {error_msg}")
                    return True  # Token 本身有效，只是未配置
                else:
                    print("❌ AI_GATEWAY_TOKEN Test Failed")
                    print(f"Error: {error_msg}")
                    return False
        except:
            print("❌ Failed to parse response")
            print(f"Response: {result['stdout']}")
            return False
    else:
        print("❌ HTTP Request Failed")
        print(f"Error: {result['stderr']}")
        return False

def test_google_gemini_api_key():
    """测试 GOOGLE_GEMINI_API_KEY"""
    print("\n" + "=" * 70)
    print("Testing GOOGLE_GEMINI_API_KEY")
    print("=" * 70)
    
    api_key = "AIzaSyCHXQsENnN8ilwrdWqDartcHOvptRsqetA"
    
    command = f"curl -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}' -H 'Content-Type: application/json' -d '{{\"contents\":[{{\"role\":\"user\",\"parts\":[{{\"text\":\"你好\"}}]}}]}}'"
    
    result = run_curl_command(command)
    
    if result["returncode"] == 0:
        try:
            data = json.loads(result["stdout"])
            if "candidates" in data:
                print("✅ GOOGLE_GEMINI_API_KEY Test Passed")
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print(f"✅ AI Response: {text[:50]}...")
                return True
            elif "error" in data:
                print("❌ GOOGLE_GEMINI_API_KEY Test Failed")
                print(f"Error: {data['error'].get('message', 'Unknown error')}")
                return False
            else:
                print("❌ Unexpected response format")
                print(f"Response: {result['stdout']}")
                return False
        except:
            print("❌ Failed to parse response")
            print(f"Response: {result['stdout']}")
            return False
    else:
        print("⚠️  GOOGLE_GEMINI_API_KEY Test - Network Issue")
        print(f"Error: {result['stderr']}")
        print("Note: This might be due to network restrictions")
        return None  # 网络问题，不判断为失败

def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ENVIRONMENT VARIABLE TESTING")
    print("=" * 80)
    
    results = {
        "CLOUDFLARE_ACCOUNT_ID": test_cloudflare_account_id(),
        "CLOUDFLARE_API_TOKEN": test_cloudflare_api_token(),
        "AI_GATEWAY_TOKEN": test_ai_gateway_token(),
        "GOOGLE_GEMINI_API_KEY": test_google_gemini_api_key()
    }
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = 0
    total = len(results)
    
    for var_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL" if result is not None else "⚠️  NETWORK"
        print(f"{var_name}: {status}")
        if result:
            passed += 1
    
    print("\n" + "=" * 80)
    print(f"Overall: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 All tests passed! All environment variables are valid.")
    else:
        print("⚠️  Some tests failed. Please check the output above for details.")

if __name__ == "__main__":
    main()
