/* eslint-disable @typescript-eslint/no-explicit-any */
import appConfig from '@/common/config';
import axios from 'axios';
import { NextResponse } from 'next/server';

const resetUrl = `${appConfig.apiBaseUrl}/rag-pdf-reset`;

export async function POST() {
  try {
    // Make POST request to reset PDF database
    const response = await axios.post(resetUrl);
    
    // Return success response with data from external API
    return NextResponse.json({
      message: 'PDF database reset successfully',
      apiResponse: response.data
    }, { status: 200 });
    
  } catch (error: any) {
    console.error('Error resetting PDF database:', error);
    
    // Handle error response
    let statusCode = 500;
    let errorMessage = 'An error occurred while resetting the PDF database';
    
    if (error.response) {
      statusCode = error.response.status;
      errorMessage = error.response.data?.message || errorMessage;
    }
    
    return NextResponse.json({
      error: errorMessage,
      details: error.message
    }, { status: statusCode });
  }
}
