// functions/api/chat.js
// Cloudflare Workers 函数处理 AI 对话请求

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

    const { message } = await request.json();
    
    if (!message || typeof message !== 'string') {
      return new Response(JSON.stringify({ error: 'Invalid message' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const response = await env.AI.run('@cf/meta/llama-2-7b-chat-int8', {
      prompt: `你是一个友好的 AI 助手，使用中文回答用户的问题。\n\n用户：${message}\n\n助手：`,
      max_tokens: 512,
      temperature: 0.7,
      top_p: 0.9
    });

    let aiResponse = response.response || '';
    aiResponse = aiResponse.trim();

    return new Response(JSON.stringify({ response: aiResponse }), {
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