#!/usr/bin/env python3
"""
测试 Google Gemini API Key 的有效性
"""

import requests
import json

def test_gemini_api():
    """测试 Gemini API Key"""
    print("=" * 70)
    print("Testing Google Gemini API Key")
    print("=" * 70)
    
    # 从配置文件中获取 API Key
    api_key = "AIzaSyCHXQsENnN8ilwrdWqDartcHOvptRsqetA"
    
    print(f"Configuration:")
    print(f"  API Key: {api_key[:10]}...")
    print()
    
    # 构建测试请求
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    print(f"Testing URL: {api_url}")
    print()
    
    # 测试数据
    test_data = {
        "contents": [{
            "role": "user",
            "parts": [{"text": "你好，测试 API Key"}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 256
        }
    }
    
    print("Sending request...")
    
    try:
        response = requests.post(
            api_url,
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and data["candidates"]:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print("✅ API Key Test Passed")
                print(f"✅ AI Response: {text[:100]}...")
                return True
            else:
                print("❌ Unexpected response format")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            try:
                error_data = response.json()
                print("Error Details:")
                print(json.dumps(error_data, indent=2, ensure_ascii=False))
            except:
                print("Error Response:", response.text)
            return False
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_api()
    print("\n" + "=" * 70)
