import { GoogleGenerativeAI } from "@google/generative-ai";

const GEMINI_API_KEY = "AIzaSyDF7RdGg3HZFryFwZC3jmJTDQsSPBdVo30";


const genAI = new GoogleGenerativeAI(GEMINI_API_KEY);

export async function POST(req) {
  const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
  const { prompt } = await req.json();

  const result = await model.generateContentStream(prompt); // ใช้ generateContentStream

  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of result.stream) {
        const text = chunk.text();
        controller.enqueue(new TextEncoder().encode(text));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { "Content-Type": "text/event-stream" },
  });

//   const result = await model.generateContent(prompt);
//   const response = await result.response;
//   const text = response.text();

//   return NextResponse.json({ result: text });
}