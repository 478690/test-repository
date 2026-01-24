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

    const { text, model } = await request.json();
    
    if (!text || typeof text !== 'string') {
      return new Response(JSON.stringify({ error: 'Invalid text' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const accountId = env.CLOUDFLARE_ACCOUNT_ID;
    const apiToken = env.CLOUDFLARE_API_TOKEN;
    
    if (!accountId || !apiToken) {
      throw new Error('Cloudflare credentials not configured');
    }

    const selectedModel = model || '@cf/deepgram/aura-2-en';
    
    const apiUrl = `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/${selectedModel}`;
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiToken}`
      },
      body: JSON.stringify({
        text: text
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.errors?.[0]?.message || 'TTS API request failed');
    }

    const audioData = await response.arrayBuffer();
    
    return new Response(audioData, {
      headers: {
        'Content-Type': 'audio/mpeg',
        'Content-Length': audioData.byteLength.toString()
      }
    });

  } catch (error) {
    console.error('TTS Error:', error);
    return new Response(JSON.stringify({ 
      error: 'Text-to-speech failed',
      details: error.message 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}