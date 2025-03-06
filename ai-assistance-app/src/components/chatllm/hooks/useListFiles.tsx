"use client";

import to from "await-to-js";
import axios from "axios";
import { useEffect, useState } from "react";

const useListFiles = () => {
  const [data, setData] = useState<ListFilesResponseType>({
    execution_time: 0,
    pdf_files: [],
    pdf_details: [],
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string|null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    const [error, result] = await to(
      axios.get("/api/rag-pdf-list-pdfs").then((res) => res.data)
    );
    if (error) {
      setLoading(false);
      setError(error.message);
      console.log("error", error);
      return;
    }
    setData(result);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  return { data,error,loading, loadData };
};

export default useListFiles;

export interface ListFilesResponseType {
  execution_time: number;
  pdf_files: string[];
  pdf_details: PDFDetail[];
}

export interface PDFDetail {
  file_name: string;
  num_pages: number;
  file_size: number;
}
