/* eslint-disable @typescript-eslint/no-explicit-any */
import appConfig from "@/common/config";
import axios from "axios";
import { NextRequest, NextResponse } from "next/server";

const url = `${appConfig.apiBaseUrl}/rag-pdf-upload-pdf`;

export async function POST(request: NextRequest) {
  try {
    // Check if the request is a valid form-data request
    const formData = await request.formData();
    const file = formData.get("file") as File;

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 });
    }

    // Check if the file is a PDF
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      return NextResponse.json(
        { error: "Only PDF files are allowed" },
        { status: 400 }
      );
    }

    // Create a new FormData instance for the API request
    const apiFormData = new FormData();
    apiFormData.append("file", file);

    // Send the file to the external API
    const response = await axios.post(url, apiFormData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    // Return the response from the external API
    return NextResponse.json(
      {
        message: "File uploaded successfully",
        fileName: file.name,
        fileSize: file.size,
        apiResponse: response.data,
      },
      { status: 200 }
    );
  } catch (error: any) {
    console.error("Error uploading file:", error);

    let statusCode = 500;
    let errorMessage = "An error occurred while uploading the file";

    if (error.response) {
      statusCode = error.response.status;
      errorMessage = error.response.data?.message || errorMessage;
    }

    return NextResponse.json(
      {
        error: errorMessage,
        details: error.message,
      },
      { status: statusCode }
    );
  }
}

// Configure the maximum size for uploads - adjust as needed
export const config = {
  api: {
    bodyParser: false, // Disable the default body parser as we're handling form data
    responseLimit: "1024mb",
  },
};
