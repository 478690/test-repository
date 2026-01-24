#!/usr/bin/env python3
import json
import urllib.request
import time

def test_model(model_id, test_type='text'):
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    api_token = 'yuQYV5OLqM6FD6x017d1K_9OxtJF2ytnGU2kJ3y6'
    
    try:
        start_time = time.time()
        
        api_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model_id}'
        
        if test_type == 'text':
            req = urllib.request.Request(
                api_url,
                data=json.dumps({
                    'messages': [
                        {'role': 'user', 'content': '你好'}
                    ],
                    'max_tokens': 50
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_token}'
                }
            )
        elif test_type == 'tts':
            req = urllib.request.Request(
                api_url,
                data=json.dumps({
                    'text': '你好，这是一个测试'
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_token}'
                }
            )
        elif test_type == 'image':
            req = urllib.request.Request(
                api_url,
                data=json.dumps({
                    'prompt': 'A beautiful sunset over mountains',
                    'num_steps': 20
                }).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_token}'
                }
            )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            elapsed_time = time.time() - start_time
            
            if test_type == 'tts':
                return {
                    'success': True,
                    'response_time': elapsed_time,
                    'type': 'audio'
                }
            elif test_type == 'image':
                response_data = json.loads(response.read().decode('utf-8'))
                return {
                    'success': True,
                    'response_time': elapsed_time,
                    'type': 'image',
                    'data': response_data
                }
            else:
                response_data = json.loads(response.read().decode('utf-8'))
                if response_data.get('success'):
                    return {
                        'success': True,
                        'response_time': elapsed_time,
                        'type': 'text'
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
    print("测试多模态模型...")
    print("="*80)
    
    multimodal_models = [
        {
            'id': '@cf/myshell-ai/melotts',
            'name': 'MeloTTS',
            'type': 'tts',
            'desc': '多语言语音合成'
        },
        {
            'id': '@cf/deepgram/aura-2-es',
            'name': 'Aura-2 ES',
            'type': 'tts',
            'desc': '西班牙语语音合成'
        },
        {
            'id': '@cf/openai/whisper',
            'name': 'Whisper',
            'type': 'stt',
            'desc': '语音识别'
        },
        {
            'id': '@cf/deepgram/nova-3',
            'name': 'Nova-3',
            'type': 'stt',
            'desc': '语音识别'
        },
        {
            'id': '@cf/deepgram/aura-1',
            'name': 'Aura-1',
            'type': 'tts',
            'desc': '语音合成'
        },
        {
            'id': '@cf/deepgram/aura-2-en',
            'name': 'Aura-2 EN',
            'type': 'tts',
            'desc': '英语语音合成'
        },
        {
            'id': '@cf/black-forest-labs/flux-1-schnell',
            'name': 'FLUX.1 Schnell',
            'type': 'image',
            'desc': '图像生成'
        },
        {
            'id': '@cf/bytedance/stable-diffusion-xl-lightning',
            'name': 'SDXL Lightning',
            'type': 'image',
            'desc': '快速图像生成'
        },
        {
            'id': '@cf/stabilityai/stable-diffusion-xl-base-1.0',
            'name': 'SDXL Base',
            'type': 'image',
            'desc': '图像生成'
        },
        {
            'id': '@cf/black-forest-labs/flux-2-klein-4b',
            'name': 'FLUX.2 Klein',
            'type': 'image',
            'desc': '快速图像生成'
        },
        {
            'id': '@cf/black-forest-labs/flux-2-dev',
            'name': 'FLUX.2 Dev',
            'type': 'image',
            'desc': '高质量图像生成'
        },
        {
            'id': '@cf/runwayml/stable-diffusion-v1-5-img2img',
            'name': 'SD v1.5 img2img',
            'type': 'image',
            'desc': '图像到图像'
        },
        {
            'id': '@cf/leonardo/lucid-origin',
            'name': 'Lucid Origin',
            'type': 'image',
            'desc': '图像生成'
        }
    ]
    
    tested_models = []
    
    for i, model in enumerate(multimodal_models, 1):
        model_id = model['id']
        model_name = model['name']
        model_type = model['type']
        
        print(f"\n[{i}/{len(multimodal_models)}] 测试: {model_name} ({model_type})")
        
        if model_type == 'stt':
            print(f"   ⏭️  跳过 - 需要音频文件输入")
            tested_models.append({
                'id': model_id,
                'name': model_name,
                'type': model_type,
                'success': None,
                'note': '需要音频文件输入'
            })
            continue
        
        result = test_model(model_id, test_type=model_type)
        
        if result['success']:
            response_time = result['response_time']
            
            print(f"   ✅ 成功 - 响应时间: {response_time:.2f}s")
            
            tested_models.append({
                'id': model_id,
                'name': model_name,
                'type': model_type,
                'success': True,
                'response_time': response_time
            })
        else:
            print(f"   ❌ 失败 - {result['error']}")
            
            tested_models.append({
                'id': model_id,
                'name': model_name,
                'type': model_type,
                'success': False,
                'error': result['error']
            })
        
        time.sleep(0.5)
    
    print("\n" + "="*80)
    print("测试结果汇总")
    print("="*80)
    
    successful = [m for m in tested_models if m['success']]
    failed = [m for m in tested_models if m['success'] is False]
    skipped = [m for m in tested_models if m['success'] is None]
    
    print(f"\n✅ 成功的模型 ({len(successful)}):")
    for model in successful:
        print(f"   - {model['name']} ({model['type']}) - {model['response_time']:.2f}s")
    
    print(f"\n❌ 失败的模型 ({len(failed)}):")
    for model in failed:
        print(f"   - {model['name']} ({model['type']}) - {model['error']}")
    
    print(f"\n⏭️  跳过的模型 ({len(skipped)}):")
    for model in skipped:
        print(f"   - {model['name']} ({model['type']}) - {model['note']}")
    
    print("\n" + "="*80)
    print(f"总计: {len(successful)}/{len(tested_models)} 个模型测试成功")
    print("="*80)
    
    print("\n可用的多模态模型:")
    print("-"*80)
    
    tts_models = [m for m in successful if m['type'] == 'tts']
    image_models = [m for m in successful if m['type'] == 'image']
    
    if tts_models:
        print("\n🎤 语音合成 (TTS):")
        for model in tts_models:
            print(f"   - {model['name']} ({model['response_time']:.2f}s)")
    
    if image_models:
        print("\n🖼️  图像生成:")
        for model in image_models:
            print(f"   - {model['name']} ({model['response_time']:.2f}s)")
    
    if skipped:
        print("\n🎧 语音识别 (STT) - 需要音频文件:")
        for model in skipped:
            print(f"   - {model['name']}")