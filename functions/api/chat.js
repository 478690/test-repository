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

    let response;
    let provider;

    if (model.startsWith('gemini-')) {
      response = await callGeminiAPI(message, model, history, env);
      provider = 'Google Gemini';
    } else {
      response = await callCloudflareAI(message, model, history, env);
      provider = 'Cloudflare Workers AI';
    }

    return new Response(JSON.stringify({ 
      response: response,
      provider: provider
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

async function callCloudflareAI(message, model, history, env) {
  const accountId = env.CLOUDFLARE_ACCOUNT_ID;
  const apiToken = env.CLOUDFLARE_API_TOKEN;
  const aiGatewayUrl = env.AI_GATEWAY_URL;
  
  if (!accountId || !apiToken) {
    throw new Error('Cloudflare credentials not configured');
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
  return data.result?.response || data.response || '';
}

async function callGeminiAPI(message, model, history, env) {
  const apiKey = env.GOOGLE_GEMINI_API_KEY;
  
  if (!apiKey) {
    throw new Error('Google Gemini API key not configured');
  }

  const modelMap = {
    'gemini-2.5-pro': 'gemini-2.5-pro',
    'gemini-2.0-flash': 'gemini-2.0-flash',
    'gemini-1.5-pro': 'gemini-1.5-pro'
  };

  const selectedModel = modelMap[model] || 'gemini-2.0-flash';
  
  const contents = [
    {
      role: 'user',
      parts: [
        {
          text: '你是一个友好的 AI 助手，使用中文回答用户的问题。你可以使用 Markdown 格式来组织回答，包括代码块、列表等。'
        }
      ]
    }
  ];

  if (history && Array.isArray(history)) {
    history.forEach(msg => {
      if (msg.role === 'user') {
        contents.push({
          role: 'user',
          parts: [{ text: msg.content }]
        });
      } else if (msg.role === 'assistant') {
        contents.push({
          role: 'model',
          parts: [{ text: msg.content }]
        });
      }
    });
  }

  contents.push({
    role: 'user',
    parts: [{ text: message }]
  });

  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${selectedModel}:generateContent?key=${apiKey}`;

  const response = await fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      contents: contents,
      generationConfig: {
        temperature: 0.7,
        maxOutputTokens: 2048
      }
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error?.message || 'Gemini API request failed');
  }

  const data = await response.json();
  return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
}