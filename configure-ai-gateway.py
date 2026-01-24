#!/usr/bin/env python3
import urllib.request
import json
import sys

class CloudflareAIGatewayConfigurator:
    def __init__(self, api_token, account_id):
        self.api_token = api_token
        self.account_id = account_id
        self.base_url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}'
        
    def make_request(self, endpoint, method='GET', data=None):
        url = f'{self.base_url}/{endpoint}'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8') if data else None,
            headers=headers,
            method=method
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"HTTP Error {e.code}: {e.reason}")
            print(f"Response: {error_body}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def list_ai_gateways(self):
        print("📋 Listing existing AI Gateways...")
        result = self.make_request('ai/gateways')
        if result and 'success' in result and result['success']:
            gateways = result.get('result', [])
            if gateways:
                print(f"Found {len(gateways)} existing gateways:")
                for gw in gateways:
                    print(f"  - {gw.get('name', 'Unknown')} (ID: {gw.get('id', 'Unknown')})")
            else:
                print("No existing gateways found.")
            return gateways
        return []
    
    def create_ai_gateway(self, name='ai-chat-gateway'):
        print(f"🚀 Creating AI Gateway: {name}")
        
        data = {
            'name': name,
            'description': 'AI Chat Application Gateway',
            'type': 'workers_ai'
        }
        
        result = self.make_request('ai/gateways', method='POST', data=data)
        
        if result and 'success' in result and result['success']:
            gateway = result.get('result', {})
            print(f"✅ AI Gateway created successfully!")
            print(f"   ID: {gateway.get('id', 'Unknown')}")
            print(f"   Name: {gateway.get('name', 'Unknown')}")
            return gateway
        else:
            print("❌ Failed to create AI Gateway")
            return None
    
    def create_route(self, gateway_id, path='*', models=None):
        print(f"🛣️  Creating route for gateway {gateway_id}...")
        
        if models is None:
            models = [
                '@cf/meta/llama-3-8b-instruct',
                '@cf/meta/llama-2-7b-chat-int8',
                '@cf/meta/llama-2-7b-chat-fp16',
                '@cf/mistral/mistral-7b-instruct-v0.2',
                '@hf/thebloke/neural-chat-7b-v3-1-awq'
            ]
        
        data = {
            'gateway_id': gateway_id,
            'path': path,
            'models': models,
            'methods': ['POST']
        }
        
        result = self.make_request(f'ai/gateways/{gateway_id}/routes', method='POST', data=data)
        
        if result and 'success' in result and result['success']:
            route = result.get('result', {})
            print(f"✅ Route created successfully!")
            print(f"   Path: {route.get('path', 'Unknown')}")
            print(f"   Models: {len(route.get('models', []))} models")
            return route
        else:
            print("❌ Failed to create route")
            return None
    
    def get_gateway_info(self, gateway_id):
        print(f"📊 Getting gateway info for {gateway_id}...")
        result = self.make_request(f'ai/gateways/{gateway_id}')
        
        if result and 'success' in result and result['success']:
            gateway = result.get('result', {})
            print(f"✅ Gateway info retrieved:")
            print(f"   Name: {gateway.get('name', 'Unknown')}")
            print(f"   ID: {gateway.get('id', 'Unknown')}")
            print(f"   Type: {gateway.get('type', 'Unknown')}")
            return gateway
        return None

def main():
    print("=" * 70)
    print("Cloudflare AI Gateway Configuration via API")
    print("=" * 70)
    print()
    
    api_token = 'fbRWRPmxK-zJyg9QfhCP-JZBar8ZjSjKuMBkvYFP'
    account_id = '30fdf13d5bb71a81bc6f7c732f244a72'
    
    configurator = CloudflareAIGatewayConfigurator(api_token, account_id)
    
    print("Step 1: Checking existing AI Gateways")
    print("-" * 70)
    existing_gateways = configurator.list_ai_gateways()
    print()
    
    print("Step 2: Creating AI Gateway")
    print("-" * 70)
    gateway = configurator.create_ai_gateway('ai-chat-gateway')
    
    if not gateway:
        print("\n❌ Failed to create AI Gateway. Exiting.")
        sys.exit(1)
    
    gateway_id = gateway.get('id')
    print()
    
    print("Step 3: Creating Route")
    print("-" * 70)
    route = configurator.create_route(gateway_id, path='*')
    
    if not route:
        print("\n❌ Failed to create route. Exiting.")
        sys.exit(1)
    
    print()
    
    print("Step 4: Getting Gateway Info")
    print("-" * 70)
    gateway_info = configurator.get_gateway_info(gateway_id)
    
    if gateway_info:
        print()
        print("=" * 70)
        print("✅ AI Gateway Configuration Complete!")
        print("=" * 70)
        print()
        print("Gateway Details:")
        print(f"  ID: {gateway_info.get('id', 'Unknown')}")
        print(f"  Name: {gateway_info.get('name', 'Unknown')}")
        print(f"  Type: {gateway_info.get('type', 'Unknown')}")
        print()
        print("API Endpoint:")
        print(f"  https://gateway.ai.cloudflare.com/v1/{account_id}")
        print()
        print("Usage:")
        print(f"  Authorization: Bearer jDGJmcyVRm_PnbueQq-NIjBfRdXvc8HqPQgbjMSI")
        print(f"  URL: https://gateway.ai.cloudflare.com/v1/{account_id}/ai/run/<model>")
        print()
        print("=" * 70)
        print("Next Steps:")
        print("1. Run: python test-ai-gateway.py")
        print("2. If successful, deploy your application")
        print("3. Your app will now use AI Gateway!")
        print("=" * 70)
    else:
        print("\n❌ Failed to get gateway info. Exiting.")
        sys.exit(1)

if __name__ == '__main__':
    main()