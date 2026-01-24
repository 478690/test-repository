export async function onRequest(context) {
  const { request, env } = context;
  
  try {
    if (request.method !== 'POST') {
      return new Response(JSON.stringify({ error: 'Method not allowed' }), {
        status: 405,
        headers: { 
          'Content-Type': 'application/json',
          'Allow': 'POST'
        }
      });
    }

    const { message, model, history } = await request.json();
    
    if (!message || typeof message !== 'string') {
      return new Response(JSON.stringify({ error: 'Invalid message' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const accountId = env.CLOUDFLARE_ACCOUNT_ID;
    const apiToken = env.CLOUDFLARE_API_TOKEN;
    const aiGatewayUrl = env.AI_GATEWAY_URL;
    
    if (!accountId || !apiToken) {
      return new Response(JSON.stringify({ error: 'Cloudflare credentials not configured' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const selectedModel = model || '@cf/meta/llama-3-8b-instruct';
    
    const messages = [
      {
        role: 'system',
        content: '你是一个友好的 AI 助手，使用中文回答用户的问题。你可以使用 Markdown 格式来组织回答，包括代码块、列表等。'
      }
    ];

    if (history && Array.isArray(history)) {
      history.forEach(msg => {
        if (msg.role === 'user' || msg.role === 'assistant') {
          messages.push({
            role: msg.role === 'user' ? 'user' : 'assistant',
            content: msg.content
          });
        }
      });
    }

    messages.push({
      role: 'user',
      content: message
    });

    let apiUrl;
    let headers = {
      'Content-Type': 'application/json'
    };

    if (aiGatewayUrl) {
      apiUrl = aiGatewayUrl;
      headers['Authorization'] = `Bearer ${apiToken}`;
      headers['cf-aig-authorization'] = `Bearer ${apiToken}`;
    } else {
      apiUrl = `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/${selectedModel}`;
      headers['Authorization'] = `Bearer ${apiToken}`;
    }

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        model: selectedModel,
        messages: messages,
        max_tokens: 2048,
        temperature: 0.7
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.errors?.[0]?.message || 'API request failed');
    }

    const data = await response.json();
    const aiResponse = data.result?.response || data.response || '';
    
    return new Response(JSON.stringify({ 
      response: aiResponse.trim(),
      gateway: aiGatewayUrl ? 'enabled' : 'disabled'
    }), {
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('AI Error:', error);
    return new Response(JSON.stringify({ 
      error: 'AI processing failed',
      details: error.message 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}