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

    const formData = await request.formData();
    const audioFile = formData.get('audio');
    const model = formData.get('model') || '@cf/openai/whisper';
    
    if (!audioFile) {
      return new Response(JSON.stringify({ error: 'No audio file provided' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const accountId = env.CLOUDFLARE_ACCOUNT_ID;
    const apiToken = env.CLOUDFLARE_API_TOKEN;
    
    if (!accountId || !apiToken) {
      throw new Error('Cloudflare credentials not configured');
    }
    
    const audioData = await audioFile.arrayBuffer();
    
    const apiUrl = `https://api.cloudflare.com/client/v4/accounts/${accountId}/ai/run/${model}`;
    
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiToken}`
      },
      body: audioData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.errors?.[0]?.message || 'STT API request failed');
    }

    const data = await response.json();
    const transcription = data.result?.text || data.text || '';
    
    return new Response(JSON.stringify({ 
      text: transcription 
    }), {
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('STT Error:', error);
    return new Response(JSON.stringify({ 
      error: 'Speech-to-text failed',
      details: error.message 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}