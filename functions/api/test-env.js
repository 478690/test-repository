export async function onRequest(context) {
  const { env } = context;
  
  return new Response(JSON.stringify({
    message: 'Environment variables test',
    env_vars: {
      hasAccountId: !!env.CLOUDFLARE_ACCOUNT_ID,
      hasApiToken: !!env.CLOUDFLARE_API_TOKEN,
      hasAiGatewayToken: !!env.AI_GATEWAY_TOKEN,
      hasGoogleGeminiKey: !!env.GOOGLE_GEMINI_API_KEY,
      accountIdLength: env.CLOUDFLARE_ACCOUNT_ID ? env.CLOUDFLARE_ACCOUNT_ID.length : 0,
      apiTokenLength: env.CLOUDFLARE_API_TOKEN ? env.CLOUDFLARE_API_TOKEN.length : 0
    }
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
}