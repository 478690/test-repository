#!/usr/bin/env python3
import json
import urllib.request

def get_multimodal_models():
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
    
    api_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/models/search'
    
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

if __name__ == '__main__':
    print("查询 Workers AI 多模态模型...")
    print("="*80)
    
    models = get_multimodal_models()
    
    multimodal_keywords = ['vision', 'image', 'audio', 'tts', 'speech', 'video', 'multimodal', 'multimodality']
    
    multimodal_models = []
    for model in models:
        name = model.get('name', '').lower()
        description = model.get('description', '').lower()
        
        is_multimodal = any(keyword in name or keyword in description for keyword in multimodal_keywords)
        
        if is_multimodal:
            multimodal_models.append(model)
    
    print(f"\n找到 {len(multimodal_models)} 个多模态模型\n")
    
    print("多模态模型列表:")
    print("-"*80)
    
    for i, model in enumerate(multimodal_models, 1):
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
        
        capabilities = []
        if 'vision' in name or 'vision' in desc:
            capabilities.append('视觉/图像')
        if 'audio' in name or 'tts' in name or 'speech' in name:
            capabilities.append('语音/TTS')
        if 'video' in name or 'video' in desc:
            capabilities.append('视频')
        if 'multimodal' in desc:
            capabilities.append('多模态')
        
        if capabilities:
            print(f"   能力: {', '.join(capabilities)}")
        print()
    
    print("="*80)
    print(f"总计: {len(multimodal_models)} 个多模态模型")
    print("="*80)
    
    if len(multimodal_models) > 0:
        print("\n⚠️ 注意:")
        print("   Workers AI 的多模态模型主要用于:")
        print("   - 图像理解 (Vision)")
        print("   - 语音合成 (TTS)")
        print("   - 多模态输入 (图像+文本)")
        print()
        print("   但是:")
        print("   - 不支持语音识别 (STT/ASR)")
        print("   - 不支持视频生成")
        print("   - 不支持图像生成")
        print()
        print("   如需这些功能，建议使用:")
        print("   - OpenAI API (Whisper for STT, DALL-E for image generation)")
        print("   - Google Cloud (Speech-to-Text, Text-to-Speech)")
        print("   - Azure Speech Services")
    else:
        print("\n❌ 未找到多模态模型")
        print("   当前 Workers AI 主要提供文本生成模型")