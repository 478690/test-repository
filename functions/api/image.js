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

    const { prompt, model } = await request.json();
    
    if (!prompt || typeof prompt !== 'string') {
      return new Response(JSON.stringify({ error: 'Invalid prompt' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const accountId = env.CLOUDFLARE_ACCOUNT_ID;
    const apiToken = env.CLOUDFLARE_API_TOKEN;
    
    if (!accountId || !apiToken) {
      throw new Error('Cloudflare credentials not configured');
    }

    const selectedModel = model || '@cf/black-forest-labs/flux-1-schnell';
    
    const apiUrl = `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/${selectedModel}`;
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiToken}`
      },
      body: JSON.stringify({
        prompt: prompt,
        num_steps: 20,
        guidance_scale: 7.5
      })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.errors?.[0]?.message || 'Image generation API request failed');
    }

    const imageData = await response.arrayBuffer();
    
    return new Response(imageData, {
      headers: {
        'Content-Type': 'image/png',
        'Content-Length': imageData.byteLength.toString()
      }
    });

  } catch (error) {
    console.error('Image Generation Error:', error);
    return new Response(JSON.stringify({ 
      error: 'Image generation failed',
      details: error.message 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}