const OLLAMA_API_URL = "http://122.155.209.179:11434"

// Handler สำหรับ reverse proxy
const ollamaReverseProxy = async ({ request }: { request: Request }) => {
  try {
    // แปลง request body เป็น JSON
    const body = await request.json()
    
    // สร้าง fetch request ไปยัง Ollama API
    const response = await fetch(`${OLLAMA_API_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      },
      body: JSON.stringify(body),
      // @ts-ignore
      duplex: 'half' // สำหรับ streaming support
    })

    // สร้าง streaming response
    return new Response(response.body, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      }
    })
  } catch (error: any) {
    console.error("Proxy Error:", error.message)
    return new Response(
      JSON.stringify({
        name: error.name,
        message: error.message
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json'
        }
      }
    )
  }
}

export default ollamaReverseProxy