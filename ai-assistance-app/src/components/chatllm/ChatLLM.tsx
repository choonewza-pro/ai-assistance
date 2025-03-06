/* eslint-disable @next/next/no-async-client-component */
"use client";
import React, { useState, useEffect, useRef } from "react";
import {
  Bars3Icon,
  ChevronLeftIcon,
  ChevronRightIcon,
} from "@heroicons/react/24/solid";
import to from "await-to-js";
import axios from "axios";
import { v4 as uuidv4 } from "uuid";
import clsx from "clsx";
import DOMPurify from "dompurify";

type ChatMessage = {
  id: string;
  message: string;
  role: "user" | "prompt" | "answer";
};

const ChatLLM = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState<string>("");
  const [showLeftColumn, setShowLeftColumn] = useState(true);
  const [showRightColumn, setShowRightColumn] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

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

      const question = encodeURIComponent(input);
      const url = `https://eportfolio.ntplc.co.th/rag-pdf-prompt?question=${question}`;

      const [error, resPrompt] = await to(
        axios.get(url).then((res) => res.data)
      );
      if (error) {
        console.log("error", error);
        return;
      }

      console.log("resPrompt", resPrompt);

      const retrievedDocs:RetrievedDocType[] = resPrompt.retrieved_docs;

      const retirevedDocMap: { [key: string]: RetrievedDocType } = {};
      retrievedDocs.forEach((doc) => {
        retirevedDocMap[doc.metadata.source] = doc;
      });


      let refDocHtml = "<ul className='list-decimal'>"
      Object.keys(retirevedDocMap).forEach((key) => {
        refDocHtml += `<ol>- source: ${getFileName(key)}</ol>`
      });
      refDocHtml += "</ul><br/>"

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

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
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
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSend();
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
            className="mb-4 p-2 bg-blue-500 text-white rounded-lg"
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
                className="p-2 bg-blue-500 text-white rounded-lg"
                onClick={() => setShowLeftColumn(!showLeftColumn)}
              >
                <Bars3Icon className="w-6 h-6" />
              </button>
            )}
          </div>

          <div>
            <h1 className="text-xl font-bold text-blue-500">
              อยากอบรมหลักสูตรอะไรถามมาครับ?
            </h1>
          </div>

          
            

          <div>
            {!showRightColumn && (
              <button
                className="p-2 bg-blue-500 text-white rounded-lg"
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
                  "bg-blue-300 text-blue-900": message.role === "user",
                  "bg-gray-300 text-black": message.role === "prompt",
                  "bg-purple-300 text-purple-900": message.role === "answer",
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
              className="mb-4 p-2 bg-blue-500 text-white rounded-lg"
              onClick={() => setShowRightColumn(false)}
            >
              <ChevronRightIcon className="w-6 h-6" />
            </button>
          </div>
          <div>Right Column Content</div>
        </div>
      )}
    </div>
  );
};

export default ChatLLM;

export type RetrievedDocType = {
  content:  string;
  metadata: RetrievedDocMetadataType;
}

export type RetrievedDocMetadataType = {
  author:       string;
  creationdate: Date;
  creator:      string;
  keywords:     string;
  moddate:      Date;
  page:         number;
  page_label:   string;
  producer:     string;
  source:       string;
  subject:      string;
  title:        string;
  total_pages:  number;
}

const getFileName = (filePath: string): string => {
  const parts = filePath.split('/');
  return parts[parts.length - 1];
};