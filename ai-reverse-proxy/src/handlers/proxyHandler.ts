import { Elysia } from 'elysia';
const API_URL = "http://122.155.209.179"

export const proxyHandler = new Elysia()
  .all('*', async ({ request, set }) => {
    try {
      const targetUrl = new URL(request.url);
      const apiRequest = new Request(
        `${API_URL}${targetUrl.pathname}${targetUrl.search}`,
        {
          method: request.method,
          headers: request.headers,
          body: ['GET', 'HEAD'].includes(request.method) ? undefined : await request.blob(),
        }
      );

      console.log(`Proxying request to: ${API_URL}${targetUrl.pathname}${targetUrl.search}`);
      
      const response = await fetch(apiRequest);
      const responseBody = await response.blob();

      // Copy all headers from the response
      response.headers.forEach((value, key) => {
        set.headers[key] = value;
      });

      set.status = response.status;
      
      return responseBody;
    } catch (error:any) {
      console.error('Proxy error:', error);
      set.status = 500;
      return { error: 'Proxy server error', message: error.message };
    }
  });
