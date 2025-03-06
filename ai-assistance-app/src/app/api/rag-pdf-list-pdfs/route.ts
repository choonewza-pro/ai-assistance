/* eslint-disable @typescript-eslint/no-explicit-any */
import appConfig from '@/common/config';
import axios from 'axios';

const url = `${appConfig.apiBaseUrl}/rag-pdf-list-pdfs`

export async function GET() {
  try {
    // Fetch data from the specified endpoint
    const response = await axios.get(url);
    
    // Return the data as a JSON response
    return new Response(JSON.stringify(response.data), {
      headers: {
        'Content-Type': 'application/json',
      },
      status: 200,
    });
  } catch (error:any) {
    console.error('Error fetching PDF data:', error);
    
    // Return appropriate error response
    return new Response(
      JSON.stringify({
        error: 'Failed to fetch PDF data',
        message: error.message,
      }),
      {
        headers: {
          'Content-Type': 'application/json',
        },
        status: error.response?.status || 500,
      }
    );
  }
}
