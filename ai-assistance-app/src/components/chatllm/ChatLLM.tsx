/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @next/next/no-async-client-component */
"use client";
import React, { useState, useEffect, useRef } from "react";
import {
  Bars3Icon,
  ChevronLeftIcon,
  ChevronRightIcon,
  PaperClipIcon,
  TrashIcon,
} from "@heroicons/react/24/solid";
import to from "await-to-js";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import clsx from "clsx";
import DOMPurify from "dompurify";
import useListFiles from "./hooks/useListFiles";
import DialogModal from "../modal/DialogModal";
import appConfig from "@/common/config";

type ChatMessage = {
  id: string;
  message: string;
  role: "user" | "prompt" | "answer" | "answer-status";
};

const ChatLLM = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>("");
  const [showLeftColumn, setShowLeftColumn] = useState(true);
  const [showRightColumn, setShowRightColumn] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [showModal1, setShowModal1] = useState(false);

  const { data: listFiles, error, loading, loadData } = useListFiles();

  const handleSend = async () => {
    if (input.trim()) {
      const cleanInput = DOMPurify.sanitize(input, {
        ALLOWED_TAGS: ["p", "br", "strong"],
        ALLOWED_ATTR: ["class", "style"],
      });

      setMessages((prev) => [
        ...prev,
        { id: uuidv4(), message: cleanInput, role: "user" },
      ]);
      setInput("");

      try {
        const question = encodeURIComponent(input);
        const url = `/api/rag-pdf-prompt?question=${question}`;

        const [error, resPrompt] = await to(
          axios.get(url).then((res) => res.data)
        );
        if (error) {
          console.log("error", error);
          setMessages((prev) => [
            ...prev,
            {
              id: uuidv4(),
              message: `Error generating prompt: ${error.message}`,
              role: "answer",
            },
          ]);
          return;
        }

        console.log("resPrompt", resPrompt);

        const retrievedDocs: RetrievedDocType[] = resPrompt.retrieved_docs;

        const retirevedDocMap: { [key: string]: RetrievedDocType } = {};
        retrievedDocs.forEach((doc) => {
          retirevedDocMap[doc.metadata.source] = doc;
        });

        let refDocHtml = "<ul className='list-decimal'>";
        Object.keys(retirevedDocMap).forEach((key) => {
          refDocHtml += `<ol>- source: ${getFileName(key)}</ol>`;
        });
        refDocHtml += "</ul><br/>";

        const cleanPrompt = DOMPurify.sanitize(resPrompt.prompt, {
          ALLOWED_TAGS: ["p", "br", "strong"],
          ALLOWED_ATTR: ["class", "style"],
        });
        setMessages((prev) => [
          ...prev,
          {
            id: uuidv4(),
            message: `<h1>PROMPT: </h1><div>${cleanPrompt}</div>`,
            role: "prompt",
          },
        ]);

        // Generate response using the prompt
        const response: any = await fetch("/api/generate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt: resPrompt.prompt }),
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        const answerId = uuidv4();
        setMessages((prev) => [
          ...prev,
          {
            id: answerId,
            message: `${refDocHtml}`,
            role: "answer",
          },
        ]);

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const textChunk = decoder.decode(value);

          setMessages((prev) =>
            prev.map((msg) => {
              if (msg.id === answerId) {
                return {
                  ...msg,
                  message: msg.message + textChunk,
                };
              }
              return msg;
            })
          );
        }
      } catch (error: any) {
        console.error("Error processing request:", error);
        setMessages((prev) => [
          ...prev,
          {
            id: uuidv4(),
            message: `Error: ${error.message}`,
            role: "answer",
          },
        ]);
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const file = files[0];

    // Show uploading message
    const uploadMsgId = uuidv4();
    setMessages((prev) => [
      ...prev,
      {
        id: uploadMsgId,
        message: `Uploading file: ${file.name}...`,
        role: "user",
      },
    ]);

    try {
      // Create form data for upload
      const formData = new FormData();
      formData.append("file", file);

      // Upload the file to our API endpoint
      const response = await fetch("/api/rag-pdf-upload-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Failed to upload file");
      }

      await response.json();

      // Update the message to show success
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === uploadMsgId ? { ...msg, message: `${file.name}` } : msg
        )
      );

      setMessages((prev) => [
        ...prev,
        {
          id: uuidv4(),
          message: `File uploaded successfully: ${file.name}`,
          role: "answer",
        },
      ]);

      // Refresh the file list
      loadData();
    } catch (error: any) {
      console.error("Error uploading file:", error);

      // Update the message to show error
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === uploadMsgId
            ? {
                ...msg,
                message: `Error uploading file: ${file.name}. ${error.message}`,
              }
            : msg
        )
      );
    }

    // Reset the file input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const triggerFileUpload = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleReset = async () => {
    try {
      // Show reset confirmation
      if (
        !confirm(
          "Are you sure you want to reset the PDF database? This will remove all uploaded PDFs."
        )
      ) {
        return;
      }

      // Call the reset API endpoint
      const response = await fetch("/api/rag-pdf-reset", {
        method: "POST",
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || "Failed to reset PDF database");
      }

      await response.json();

      // Add a system message about the reset
      setMessages((prev) => [
        ...prev,
        {
          id: uuidv4(),
          message: "PDF database has been reset successfully.",
          role: "answer",
        },
      ]);

      // Refresh the file list
      loadData();
    } catch (error: any) {
      console.error("Error resetting PDF database:", error);

      // Add error message
      setMessages((prev) => [
        ...prev,
        {
          id: uuidv4(),
          message: `Error resetting PDF database: ${error.message}`,
          role: "answer",
        },
      ]);
    }
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="flex h-screen bg-gray-100">
      {showLeftColumn && (
        <div className="hidden sm:block w-1/4 bg-gray-200 p-4">
          <button
            className="mb-4 p-2 bg-gray-500 text-white rounded-lg"
            onClick={() => setShowLeftColumn(false)}
          >
            <ChevronLeftIcon className="w-6 h-6" />
          </button>
          <div>Left Column Content</div>
        </div>
      )}
      <div className="flex-grow flex flex-col">
        <div className="flex justify-between p-4 bg-gray-100 border-b border-gray-300">
          <div>
            {!showLeftColumn && (
              <button
                className="p-2 bg-gray-500 text-white rounded-lg"
                onClick={() => setShowLeftColumn(!showLeftColumn)}
              >
                <Bars3Icon className="w-6 h-6" />
              </button>
            )}
          </div>

          <div>
            <h1 className="text-xl font-bold text-blue-500">
              มีอะไรให้ช่วยบ้างครับ?
            </h1>
          </div>

          <div>
            {!showRightColumn && (
              <button
                className="p-2 bg-gray-500 text-white rounded-lg"
                onClick={() => setShowRightColumn(!showRightColumn)}
              >
                <Bars3Icon className="w-6 h-6" />
              </button>
            )}
          </div>
        </div>
        <div className="flex-grow p-4 overflow-y-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={clsx("mb-4", {
                "flex justify-end": message.role === "user",
                "flex justify-start": message.role !== "user",
              })}
            >
              <div
                className={clsx("p-2 rounded-lg w-fit-content", {
                  "bg-blue-200 text-blue-900": message.role === "user",
                  "bg-gray-300 text-black": message.role === "prompt",
                  "bg-green-200 text-green-900":
                    message.role === "answer-status",
                  "bg-purple-200 text-purple-900": message.role === "answer",
                })}
              >
                <div
                  dangerouslySetInnerHTML={{
                    __html: message.message.replace(/\n/g, "<br>"),
                  }}
                />
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="p-4 bg-white border-t border-gray-300">
          <div className="flex">
            <input
              type="text"
              className="flex-grow p-2 border border-gray-300 rounded-lg text-black"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
            />
            {/* Hidden file input controlled by the paper clip button */}
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              className="hidden"
            />
            <button
              className="ml-2 p-2 bg-gray-500 text-white rounded-lg hover:bg-gray-400 cursor-pointer"
              onClick={triggerFileUpload}
              title="Upload file"
            >
              <PaperClipIcon className="w-5 h-5" />
            </button>
            <button
              className="ml-2 p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-400 cursor-pointer"
              onClick={handleSend}
            >
              Send
            </button>
          </div>
        </div>
      </div>
      {showRightColumn && (
        <div className="hidden sm:block w-1/4 bg-gray-200 p-4">
          <div className="flex justify-end">
            <button
              className="mb-4 p-2 bg-gray-500 text-white rounded-lg"
              onClick={() => setShowRightColumn(false)}
            >
              <ChevronRightIcon className="w-6 h-6" />
            </button>
          </div>
          <div className="text-black">
            <div className="flex items-center justify-between gap-2 pb-2">
              <div>Knowledge</div>
              <button
                className="p-1 bg-red-500 text-white rounded-lg hover:bg-red-400 cursor-pointer"
                onClick={handleReset}
                title="Reset PDF database"
              >
                <TrashIcon className="w-4 h-4" />
              </button>
            </div>
            <div className="grid grid-cols-1 gap-2">
              {loading && (
                <div className="border border-gray-200 rounded-md p-2 bg-white shadow">
                  Loading...
                </div>
              )}
              {error && (
                <div className="text-sm text-red-500 border border-red-200 rounded-md p-2 bg-red-50 shadow">
                  {error}
                </div>
              )}
              {listFiles.pdf_details.map((file) => (
                <a
                  href={`${appConfig.apiBaseUrl}/static/pdf_files/${file.file_name}`}
                  target="_blank"
                  key={file.file_name}
                >
                  <div
                    key={file.file_name}
                    className="border border-gray-200 rounded-md p-2 bg-white shadow"
                  >
                    <div className="text-sm">{file.file_name}</div>
                    <div className="flex gap-2">
                      <div className="text-gray-500 text-sm">
                        {(file.file_size / (1024 * 1024)).toFixed(2)} MB
                      </div>
                      <div className="text-gray-500 text-sm">
                        {file.num_pages} pages
                      </div>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>
      )}

      <DialogModal
        isOpen={showModal1}
        onClose={() => setShowModal1(false)}
        title="Dialog Title"
      >
        Dialog Content
      </DialogModal>
    </div>
  );
};

export default ChatLLM;

export type RetrievedDocType = {
  content: string;
  metadata: RetrievedDocMetadataType;
};

export type RetrievedDocMetadataType = {
  author: string;
  creationdate: Date;
  creator: string;
  keywords: string;
  moddate: Date;
  page: number;
  page_label: string;
  producer: string;
  source: string;
  subject: string;
  title: string;
  total_pages: number;
};

const getFileName = (filePath: string): string => {
  const parts = filePath.split("/");
  return parts[parts.length - 1];
};
