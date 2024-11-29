// 检查键是否以.jpg或.png结尾
const isImageFile = (key) => {
  return key.endsWith('.jpg') || key.endsWith('.png');
};

// 检查请求是否包含预共享的密钥
const hasValidHeader = (request, env) => {
  return request.headers.get('X-Custom-Auth-Key') === env.AUTH_KEY_SECRET;
};

function authorizeRequest(request, env, key) {
  switch (request.method) {
    case 'PUT':
    case 'DELETE':
      return hasValidHeader(request, env);
    case 'GET':
      return isImageFile(key);
    default:
      return false;
  }
}

// 定义CORS头
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET,HEAD,POST,OPTIONS,PUT,DELETE',
  'Access-Control-Allow-Headers': 'Content-Type, X-Custom-Auth-Key',
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    // 处理OPTIONS预检请求
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders,
      });
    }

    if (!authorizeRequest(request, env, key)) {
      return new Response('Forbidden', { status: 403, headers: corsHeaders });
    }

    switch (request.method) {
      case 'PUT':
        await env.MY_BUCKET.put(key, request.body);
        return new Response(`Put ${key} successfully!`, { headers: corsHeaders });
      case 'GET':
        const object = await env.MY_BUCKET.get(key);

        if (object === null) {
          return new Response('Object Not Found', { status: 404, headers: corsHeaders });
        }

        const headers = new Headers(corsHeaders);
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);

        return new Response(object.body, {
          headers,
        });
      case 'DELETE':
        await env.MY_BUCKET.delete(key);
        return new Response('Deleted!', { headers: corsHeaders });

      default:
        return new Response('Method Not Allowed', {
          status: 405,
          headers: {
            ...corsHeaders,
            'Allow': 'PUT, GET, DELETE',
          },
        });
    }
  },
};