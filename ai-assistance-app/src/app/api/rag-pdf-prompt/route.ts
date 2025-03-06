/* eslint-disable @typescript-eslint/no-explicit-any */
import axios from 'axios';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Extract the question from the URL search params
    const searchParams = request.nextUrl.searchParams;
    const question = searchParams.get('question');
    
    if (!question) {
      return NextResponse.json(
        { error: 'Question parameter is required' },
        { status: 400 }
      );
    }
    
    // Construct the external API URL with the question parameter
    const apiUrl = `http://localhost/rag-pdf-prompt?question=${encodeURIComponent(question)}`;
    
    // Call the external API
    const response = await axios.get(apiUrl);
    
    // Return the response data
    return NextResponse.json(response.data, { status: 200 });
    
  } catch (error: any) {
    console.error('Error generating prompt:', error);
    
    // Handle error response
    let statusCode = 500;
    let errorMessage = 'An error occurred while generating the prompt';
    
    if (error.response) {
      statusCode = error.response.status;
      errorMessage = error.response.data?.message || errorMessage;
    }
    
    return NextResponse.json(
      {
        error: errorMessage,
        details: error.message
      },
      { status: statusCode }
    );
  }
}
